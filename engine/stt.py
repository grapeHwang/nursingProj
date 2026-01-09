import wave
import pyaudio
import webrtcvad
from groq import Groq
import numpy as np

class SpeechToText:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        self.rate = 16000
        self.channels = 1
        self.format = pyaudio.paInt16
        self.chunk = 480
        self.vad = webrtcvad.Vad(2)
        self.p = pyaudio.PyAudio()
        self.temp_filename = "temp_recording.wav"

    def listen(self, device_index=3):
        stream = self.p.open(format=self.format,
                             channels = self.channels,
                             rate = self.rate,
                             input=True,
                             input_device_index=device_index,
                             frames_per_buffer=self.chunk)
        
        frames = []
        num_silent_frames = 0
        is_recording = False

        rms_threshold = 30
        max_silent_frames = int(0.5 / (self.chunk / self.rate))
        min_recording_frames = int(0.5 / (self.chunk / self.rate))

        
        while True:
            try : 
                data = stream.read(self.chunk, exception_on_overflow=False)
                audio_data = np.frombuffer(data, dtype=np.int16)
                rms = np.sqrt(np.mean(audio_data**2))

                is_speech = self.vad.is_speech(data, self.rate) and (rms > rms_threshold)

                if is_speech:
                    if not is_recording:
                        print("recording") 
                        is_recording= True
                    frames.append(data)
                    num_silent_frames = 0

                elif is_recording:
                    frames.append(data)
                    num_silent_frames += 1

                    if num_silent_frames > max_silent_frames:
                        if len(frames) < min_recording_frames:
                            print("ignored")
                            frames = []
                            is_recording = False
                            num_silent_frames = 0
                            continue
                        print("recorded")
                        break

                if is_recording and len(frames) > int(self.rate / self.chunk * 15):
                    print("max recording")
                    break


            except Exception as e:
                print(f"error : {e}")
                break


 
        stream.stop_stream()
        stream.close()



        if frames : 
            wf = wave.open(self.temp_filename, 'wb')
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.p.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(frames))
            wf.close()
            
            transcript = self.transcribe(self.temp_filename)
            
            return transcript
        
        return ""
    


    def transcribe(self, audio_path):
        
        with open(audio_path, "rb") as audio_file :
            transcriptions = self.client.audio.transcriptions.create(
                file = audio_file,
                model="whisper-large-v3",
                prompt="이 오디오 파일에 담긴 한국어 말을 그대로 텍스트로 받아써줘. 오직 받아쓴 내용만 출력해. 만약에 사람이 말하고 있지 않거나, 한국어로 들리지 않는다면 '...'으로 작성하면 돼",
                response_format="json",
                language="ko"
            )


        return transcriptions.text
    


