from engine import SpeechToText, ChildPatientBrain, TextToSpeech
from config import GROQ_API_KEY, GEMINI_API_KEY, ELEVENLABS_API_KEY



def main():
    try:
        stt = SpeechToText(api_key=GROQ_API_KEY)
        brain = ChildPatientBrain(api_key=GEMINI_API_KEY)
        tts = TextToSpeech(api_key=ELEVENLABS_API_KEY)
    except Exception as e:
        print("error")
        return
    

    try : 
        while True:
            user_text = stt.listen()
            
            if not user_text or user_text.strip() == "" :
                continue

            print(f"user : {user_text}")

            child_response = brain.get_response(user_text)
            print(f"patient : {child_response}")

            tts.speak(child_response)
    except KeyboardInterrupt:
        print(exit)



if __name__ == "__main__":
    main()

