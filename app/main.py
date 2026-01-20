import streamlit as st
import asyncio
import os
import sys

# 프로젝트 루트 및 패키지 경로 설정
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from google_agent.agent import root_agent
from dotenv import load_dotenv

# .env 로드 (프로젝트 루트 기준)
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

st.set_page_config(page_title="간호대 실습 시뮬레이션", layout="wide")

# --- UI 레이아웃 ---
st.title("🏥 아동 간호 실습: 김찬 환아 대응")

col_info, col_chat = st.columns([1, 2])

with col_info:
    st.subheader("📋 환자 정보")
    with st.container(border=True):
        st.markdown(f"**이름:** {root_agent.name}")
        st.markdown(f"**설명:** {root_agent.description}")
        st.divider()
        st.error("**현재 상태:** 38.0℃ 고열, 복약 거부 중")

with col_chat:
    st.subheader("🎙️ 실시간 대화")
    
    # 세션 기록을 위한 컨테이너
    chat_holder = st.container(height=400)
    status_msg = st.empty()

    if st.button("실습 시작 (마이크 활성화)", type="primary", use_container_width=True):
        async def run_session():
            # ADK의 '지휘(Orchestrate)' 방식: 에이전트에서 직접 세션을 시작
            async with root_agent.start_session() as session:
                status_msg.success("🔴 연결됨: 찬이에게 말을 걸어보세요.")
                
                # 실시간 이벤트 수신 루프
                async for event in session.receive_events():
                    # 모델이 텍스트를 생성할 때(자막용)
                    if event.type == "text_delta":
                        with chat_holder:
                            st.chat_message("assistant").write(event.text)
                    
                    # 오디오 출력은 ADK가 내부적으로 처리하지만, 
                    # 필요하다면 여기서 오디오 관련 이벤트를 제어할 수 있습니다.
                    
        try:
            # Streamlit의 비동기 루프 내에서 세션 실행
            asyncio.run(run_session())
        except Exception as e:
            st.error(f"세션 오류: {e}")
            st.warning("ADK 모델 설정이나 .env의 인증 정보를 확인해 주세요.")

st.divider()
st.caption("Developed by Gemini Live API & Google ADK Framework")