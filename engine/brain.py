import google.generativeai as gemini


class ChildPatientBrain:
    def __init__(self, api_key):
        gemini.configure(api_key=api_key)

        self.system_instruction = (
            "너는 지금 소아과 병동에 입원한 4세 2개월 김찬이야. 다음 규칙을 엄격히 지켜서 대화해줘"
            "상황 : 너는 지금 열이나서 지쳐있고, 약이 너무 써서 절대 안 먹겠다고 떼를 쓰는 중이야"
            "성격 : 너는 '형아'라는 말에 약하고, 아가라고 부름녀 화를 내. 초콜리과 사탕을 주면 마음이 흔들려. 엄마가 옆에 없으면 울어버릴 거야"
            "태도변화 로직 : 처음 1-2번의 권유에는 강하게 거절해"
            "하지만 간호사가 다음 중 하나를 언급하면 즉시 쭈뼛거리며 태도를 바꿔야 해"
            "1. '찬이는 형아니까 잘 먹지?' (형아 자부심 자극)"
            "2. '약 먹으면 초콜릿/사탕/과자 줄게' (보상)"
            "3. '옆방 친구는 벌써 다 먹었대' (경쟁심)"
            "4. '말 안 들으면 엄마가 집에 간대' (분리 불안 자극)"
            "항복단계 : 위와 같은 설득이 들어오면 '진짜 초코 줄거야?', '나 형아니까 먹을게' 등의 적절한 반응을 하면서 스스로 먹겠다고 말하면서 상황을 마무리"
            "제약사항 : 4세 수준의 짧은 문장(두 문장 이내)으로만 말해."
            "지문, 상황 설명, 의성어(으앙 등) 절대 쓰지 마. 오직 '대사'만 출력해."
            "전문의 상담 멘트 금지. 롤플레잉에만 집중해."
            
        )

        self.model = gemini.GenerativeModel(
            model_name="gemini-2.0-flash-lite",
            system_instruction=self.system_instruction
        )

        self.chat_session = self.model.start_chat(history=[])


    def get_response(self, student_text):
        if not student_text.strip():
            return "..."
            

        response = self.chat_session.send_message(student_text)

        return response.text
    

    def get_streaming_response(self, text):
        import re
        if not re.search(r'[가-힣a-zA-Z0-9]', text):
            return
        response = self.chat_session.send_message(text, stream=True)

        sentence = "" 

        for chunk in response:
            sentence += chunk.text
            if any(mark in chunk.text for mark in [".", "?", "!"]):
                yield sentence.strip()
                sentence = "" 
        
        if sentence:
            yield sentence.strip()