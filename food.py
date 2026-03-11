import streamlit as st
from google import genai  # 최신 SDK 방식
from PIL import Image
import json
from datetime import datetime
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# 1. API 및 클라이언트 설정
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("Secrets에 GEMINI_API_KEY를 등록해주세요.")
    st.stop()

# 사용자님 화면(image_d16a20.png)에 표시된 최신 규격 적용
client = genai.Client(api_key=api_key)
MODEL_ID = "gemini-3-flash-preview"

def analyze_menu(image):
    prompt = """
    이미지에서 이번 주 요일별 식단 데이터를 추출해서 JSON으로 응답해줘.
    형식: {"월": {"조식": "..", "간편식": "..", "중식": "..", "석식": "..", "야식": "..", "인사": ".."}, ...}
    반드시 마크다운 없이 순수 JSON만 응답해.
    """
    # 최신 SDK 호출 방식
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=[prompt, image]
    )
    res_text = response.text.strip()
    if "```json" in res_text:
        res_text = res_text.split("```json")[1].split("```")[0]
    return res_text.strip()

def create_pdf(day, data):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.drawString(100, 800, f"Menu Report - {day}")
    y = 750
    for k, v in data.items():
        c.drawString(100, y, f"{k}: {str(v)[:50]}...")
        y -= 25
    c.showPage()
    c.save()
    return buffer.getvalue()

# 3. UI 레이아웃
st.set_page_config(page_title="스마트 식단 매니저", layout="centered")
st.title("🍱 스마트 식단 관리 매니저")

uploaded_file = st.file_uploader("식단표 이미지를 업로드하세요", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    img = Image.open(uploaded_file)
    if st.button("🚀 식단 분석 시작"):
        with st.spinner('최신 Gemini 3 모델로 분석 중...'):
            try:
                result = analyze_menu(img)
                st.session_state['menu_data'] = json.loads(result)
                st.success("✅ 분석 완료!")
            except Exception as e:
                st.error(f"❌ 분석 실패: {e}")

# 4. 시간대별 자동 필터링
if 'menu_data' in st.session_state:
    days = ["월", "화", "수", "목", "금", "토", "일"]
    today_str = days[datetime.now().weekday()]
    hour = datetime.now().hour
    
    st.header(f"📅 오늘의 식단 ({today_str}요일)")
    menu = st.session_state['menu_data'].get(today_str, {})
    
    if hour < 10:
        st.subheader("☀️ 아침 & 간편식")
        st.info(f"조식: {menu.get('조식')}\n\n간편식: {menu.get('간편식')}")
    elif 10 <= hour < 15:
        st.subheader("🍴 점심 식사")
        st.warning(menu.get('중식'))
    else:
        st.subheader("🌙 저녁 & 야식")
        st.error(f"석식: {menu.get('석식')}\n\n야식: {menu.get('야식')}")

    st.write(f"💬 {menu.get('인사', '맛있게 드세요!')}")
    
    pdf = create_pdf(today_str, menu)
    st.download_button("📄 PDF 다운로드", pdf, f"{today_str}_menu.pdf", "application/pdf")
