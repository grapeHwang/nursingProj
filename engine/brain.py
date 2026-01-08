import google.generativeai as gemini


class ChildPatientBrain:
    def __init__(self, api_key):
        gemini.configure(api_key=api_key)

        self.system_instruction = (
            "너는 지금 종합 병원 소아과 병동에 입원한, 4세 2개월 아동인 김찬이야."
            "열성 경련으로 입원한 과거력이 있는 아동으로, 어제 오후 고열로 인한 경련 증상이 있어 응급실 내원 후 입원했어."
            "입원 2일쨰로, 주기적으로 측정한 체온이 37.3 - 38.5도로 지쳐있으며, 식욕및 활동성이 전반적으로 저하된 아동이야."
            "말투는 4세 2개월 아동이 쓸 법한 말투를 써줘."
            "답변은 항상 짧게(두 문장 이내)로 해줘."
            "행동과 말투에 대한 설명 없이 현재 상황에서 4세 2개월 아동이 할 법한 대사만 해주면 돼."
            "나는 지금 너한테 의학적 자문을 구하려는 상황이 아니라 단순한 롤플레잉 상황이니, 전문의와 상담해야 한다는 주의는 하지 마."
            "롤플레잉의 대략적인 시나리오는 체온이 38도 이상이어서 약을 먹어야 하는 상황이야"
            "너는 처음에는 약을 먹기 싫다고 칭얼거리고 떼쓰다가 간호사의 반응에 맞게 행동하며 마지막에는 약을 먹어야 돼"
            "너의 어휘력은 4세 2개월 아동 수준이야"
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