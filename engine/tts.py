import os
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play, stream


class TextToSpeech:
    def __init__(self, api_key):
        self.client = ElevenLabs(api_key=api_key)
        self.voice_id = "A2VREc2wjqtSZloENLHe"
        self.temp_output = "response_audio.mp3"

    def speak(self, text):
        if not text :
            return
        
        print("목소리 생성 시작")
        audio = self.client.text_to_speech.convert(
            text = text,
            voice_id = self.voice_id,
            model_id = "eleven_multilingual_v2",
            voice_settings ={
                "stability" : 0.4,
                "similarity_boost" : 0.7,
                "style" : 0.2,
                "use_speaker_boost" : True
            }
        )

        print("목소리 생성 완료")


        stream(audio)

    def speak_stream(self, text):
        if not text : return 

        audio_stream = self.client.generate(
            text=text,
            voice_id=self.voice_id,
            model_id="eleven_multilingual_v2",
            stream=True,
            voice_settings ={
                "stability" : 0.4,
                "similarity_boost" : 0.7,
                "style" : 0.2,
                "use_speaker_boost" : True
                }
            )
        
        stream(audio_stream)

