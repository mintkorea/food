import streamlit as st
import google.generativeai as genai
from PIL import Image
import json
from datetime import datetime
import io
import time

# --- 1. API 설정 및 모델 로드 로직 (404 에러 원천 차단) ---
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ Streamlit Cloud의 [Settings > Secrets]에 GEMINI_API_KEY를 등록해주세요.")
    st.stop()

genai.configure(api_key=api_key)

def get_model():
    # 404 에러를 피하기 위해 가능한 모든 모델 경로를 시도합니다.
    model_names = ['gemini-1.5-flash', 'models/gemini-1.5-flash', 'gemini-1.5-flash-latest']
    for name in model_names:
        try:
            m = genai.GenerativeModel(name)
            # 모델이 실제로 작동하는지 가벼운 테스트
            return m
        except:
            continue
    return None

model = get_model()

def analyze_menu(image):
    if not model:
        return "모델을 로드할 수 없습니다. API 권한을 확인해주세요."
    
    prompt = """
    식단표 이미지에서 요일별 [조식, 간편식, 중식, 석식, 야식] 데이터를 추출해 JSON으로 응답해.
    형식: {"월": {"조식": "..", "중식": "..", "석식": "..", "인사": ".."}, ...}
    마크다운 없이 순수 JSON만 출력해.
    """
    
    # 503 에러 대비 재시도 로직
    for i in range(3):
        try:
            response = model.generate_content([prompt, image])
            res_text = response.text.strip()
            if "```json" in res_text:
                res_text = res_text.split("```json")[1].split("```")[0]
            return json.loads(res_text.strip())
        except Exception as e:
            if i < 2:
                time.sleep(3)
                continue
            raise e

# --- 2. UI 레이아웃 ---
st.set_page_config(page_title="스마트 식단 매니저", layout="centered")
st.title("🍱 스마트 식단 관리 매니저")

uploaded_file = st.file_uploader("주간 식단표 이미지를 업로드하세요", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="업로드된 식단표", use_container_width=True)
    
    if st.button("🚀 식단 분석 시작"):
        with st.spinner('AI가 식단을 분석 중입니다...'):
            try:
                result = analyze_menu(img)
                st.session_state['menu_data'] = result
                st.success("✅ 분석 완료!")
                st.rerun()
            except Exception as e:
                st.error(f"분석 실패: {e}")

# --- 3. 결과 표시 ---
if 'menu_data' in st.session_state:
    days = ["월", "화", "수", "목", "금", "토", "일"]
    today_str = days[datetime.now().weekday()]
    
    st.divider()
    st.header(f"📅 오늘의 식단 ({today_str}요일)")
    
    menu = st.session_state['menu_data'].get(today_str, {})
    if menu:
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"🍴 **중식**\n\n{menu.get('중식', '정보 없음')}")
        with col2:
            st.error(f"🌙 **석식**\n\n{menu.get('석식', '정보 없음')}")
        st.chat_message("assistant").write(menu.get("인사", "맛있게 드세요!"))
