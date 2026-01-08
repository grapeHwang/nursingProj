# engine/__init__.py

# 1. 각 모듈에서 핵심 클래스/함수를 가져옵니다.
from .stt import SpeechToText
from .brain import ChildPatientBrain
from .tts import TextToSpeech

# 2. 패키지 수준에서 공통으로 사용할 변수를 정의할 수도 있습니다.
__version__ = "1.0.0"
__author__ = "Nursing-Sim-Designer"

# 3. 외부에서 'from engine import *'를 했을 때 노출될 리스트를 정의합니다.
__all__ = ['SpeechToText', 'ChildPatientBrain', 'TextToSpeech']