import asyncio
import os
from dotenv import load_dotenv
from google import genai
from google.oauth2 import service_account
from .audio_device import AudioDevice
from scenarios import SCENARIOS
import random

load_dotenv()


class ChildPatientSim :
    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(
            os.getenv("GOOGLE_APPLICATION_CREDENTIALS"), 
            scopes=['https://www.googleapis.com/auth/cloud-platform'])
        self.model_id = "gemini-2.5-flash-preview-04-17"
        self.audio = AudioDevice()
        self.client = genai.Client(
            vertexai=True,
            project=os.getenv("GOOGLE_CLOUD_PROJECT"),
            location="global", #os.getenv("GOOGLE_CLOUD_LOCATION"),
            credentials=credentials)


    async def start_session(self, persona_text):
        async with self.client.aio.live.connect(
            model = self.model_id,
            config={"generation_config": {"response_modalities": ["AUDIO"]},
                    "speech_config": {
                        "voice_config": {"prebuilt_voice_config": {"voice_name": "Puck"}}
                        },
                    "system_instruction": persona_text
                    }
        )as session :
            stream = self.audio.open_stream()
            print("start simulation")


            async def send_mic_audio():
                try:
                    while True:
                        data = await asyncio.to_thread(stream.read, 512)
                        await session.send(input={"data" : data, "mime_type" : "audio/pcm"})
                except Exception as e:
                    print(f"error in sending mic audio : {e}")
            async def receive_child_audio():
                try : 
                    async for message in session.receive():
                        if message.data:
                            await asyncio.to_thread(stream.write, message.data)
                        if message.text:
                            print(f"patient : {message.text}")
                except Exception as e:
                    print(f"error in receiving audio : {e}")


            await asyncio.gather(send_mic_audio(), receive_child_audio())


def select_presona():
    key = random.choice(list(SCENARIOS.keys()))
    return key


if __name__ == "__main__":
    name = select_presona()
    print(f"name : {name}")
    prompt = SCENARIOS[name].get_system_instruction()
    sim = ChildPatientSim()
    
    try : 
        asyncio.run(sim.start_session(prompt))
    except KeyboardInterrupt :
        print("ending simulation...")