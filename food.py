import streamlit as st
from google import genai  # 라이브러리 호출 방식 변경
from PIL import Image
import json
from datetime import datetime
import io

# 1. API 및 클라이언트 설정
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("Secrets에 GEMINI_API_KEY를 등록해주세요.")
    st.stop()

# 최신 SDK 방식 적용
client = genai.Client(api_key=api_key)
# 사용자님 화면에 표시된 최신 모델명 사용
MODEL_ID = "gemini-3-flash-preview"

def analyze_menu(image):
    prompt = """
    이미지에서 이번 주 요일별 식단 데이터를 추출해서 JSON으로 응답해줘.
    형식: {"월": {"조식": "..", "중식": "..", "석식": "..", "인사": ".."}, ...}
    반드시 마크다운 없이 순수 JSON만 응답해.
    """
    # 최신 SDK 호출 규격 (화면 예제 반영)
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=[prompt, image]
    )
    res_text = response.text.strip()
    if "```json" in res_text:
        res_text = res_text.split("```json")[1].split("```")[0]
    return res_text.strip()

# --- 이하 UI 및 로직 동일 ---
st.title("🍱 스마트 식단 관리 매니저")
uploaded_file = st.file_uploader("식단표 이미지를 업로드하세요", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    img = Image.open(uploaded_file)
    if st.button("🚀 식단 분석 시작"):
        try:
            result = analyze_menu(img)
            st.session_state['menu_data'] = json.loads(result)
            st.success("분석 완료!")
        except Exception as e:
            st.error(f"분석 실패: {e}")

if 'menu_data' in st.session_state:
    st.write("오늘의 메뉴:", st.session_state['menu_data'])
