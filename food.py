import streamlit as st
import google.generativeai as genai
from PIL import Image
import json
from datetime import datetime
import io
import time

# --- 1. API 및 모델 설정 (가장 안정적인 방식) ---
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.warning("⚠️ API 키가 설정되지 않았습니다. Secrets를 확인해주세요.")
    st.stop()

genai.configure(api_key=api_key)
# 프리뷰 대신 안정화된 1.5-flash 모델을 메인으로 사용합니다.
model = genai.GenerativeModel('gemini-1.5-flash')

def analyze_menu_with_retry(image, max_retries=3):
    """서버 과부하 시 최대 3번까지 재시도하는 함수"""
    prompt = """
    이미지에서 요일별 식단 데이터를 추출해서 JSON으로 응답해줘.
    형식: {"월": {"조식": "..", "중식": "..", "석식": "..", "인사": ".."}, ...}
    반드시 마크다운 없이 순수 JSON만 응답해.
    """
    
    for i in range(max_retries):
        try:
            # 매 시도마다 상태 표시 업데이트
            with st.spinner(f'AI 분석 중... (시도 {i+1}/{max_retries})'):
                response = model.generate_content([prompt, image])
                res_text = response.text.strip()
                
                # JSON 클렌징
                if "```json" in res_text:
                    res_text = res_text.split("```json")[1].split("```")[0]
                elif "```" in res_text:
                    res_text = res_text.split("```")[1].split("```")[0]
                
                return json.loads(res_text.strip())
        except Exception as e:
            if i < max_retries - 1:
                st.write(f"⏳ 서버가 바쁩니다. 3초 후 다시 시도합니다... ({e})")
                time.sleep(3)
                continue
            else:
                raise e

# --- 2. UI 구성 ---
st.set_page_config(page_title="스마트 식단 매니저", layout="centered")
st.title("🍱 스마트 식단 관리 매니저")

uploaded_file = st.file_uploader("식단표 이미지를 업로드하세요", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="업로드된 식단표", use_container_width=True)
    
    if st.button("🚀 식단 분석 시작"):
        try:
            # 분석 시작
            menu_data = analyze_menu_with_retry(img)
            st.session_state['menu_data'] = menu_data
            st.success("✅ 분석 완료!")
            st.rerun() # 결과 즉시 표시를 위해 새로고침
        except Exception as e:
            st.error(f"❌ 여러 번 시도했으나 실패했습니다: {e}")
            st.info("Tip: 잠시 후 다시 시도하거나, 더 선명한 이미지를 사용해 보세요.")

# --- 3. 결과 표시 로직 ---
if 'menu_data' in st.session_state:
    days = ["월", "화", "수", "목", "금", "토", "일"]
    # 현재 시간 기준 요일 (서버 시간차 고려)
    today_idx = datetime.now().weekday()
    today_str = days[today_idx]
    
    st.divider()
    st.header(f"📅 오늘의 식단 ({today_str}요일)")
    
    menu = st.session_state['menu_data'].get(today_str, {})
    
    if menu:
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**🍴 중식**\n\n{menu.get('중식', '정보 없음')}")
        with col2:
            st.error(f"**🌙 석식**\n\n{menu.get('석식', '정보 없음')}")
        
        st.chat_message("assistant").write(menu.get("인사", "오늘 하루도 고생 많으셨습니다! 맛있게 드세요."))
    
    # 다른 요일 식단 확인용 익스팬더
    with st.expander("📝 전체 주간 식단 보기"):
        st.json(st.session_state['menu_data'])

    if st.button("🗑️ 초기화"):
        del st.session_state['menu_data']
        st.rerun()
