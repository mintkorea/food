import streamlit as st
from google import genai
from PIL import Image
import json
from datetime import datetime
import io
import time
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# --- 1. 클라이언트 및 모델 설정 ---
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ Streamlit Cloud의 [Settings > Secrets]에 새로운 API 키를 등록해주세요.")
    st.stop()

# 최신 SDK 규격 적용 (image_d16a20.png 참조)
client = genai.Client(api_key=api_key)
MODEL_ID = "gemini-3-flash-preview"

# --- 2. 핵심 기능 함수 ---

def analyze_menu(image):
    """서버 상태를 고려하여 식단을 분석합니다."""
    prompt = """
    이미지에서 이번 주 요일별 식단 데이터를 추출해서 JSON으로 응답해줘.
    형식: {"월": {"조식": "..", "간편식": "..", "중식": "..", "석식": "..", "야식": "..", "인사": "..", "효능": ".."}, ...}
    반드시 마크다운 없이 순수 JSON 텍스트만 응답해.
    """
    
    # 503 에러 대비 재시도 로직
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=[prompt, image]
            )
            res_text = response.text.strip()
            # JSON 클렌징
            if "```json" in res_text:
                res_text = res_text.split("```json")[1].split("```")[0]
            elif "```" in res_text:
                res_text = res_text.split("```")[1].split("```")[0]
            return res_text.strip()
        except Exception as e:
            if "503" in str(e) and attempt < 2:
                st.warning("서버가 혼잡하여 재시도 중입니다... 잠시만 기다려주세요.")
                time.sleep(2)
                continue
            raise e

def create_pdf(day, data):
    """식단 데이터를 PDF로 변환"""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(100, 800, f"Weekly Menu Report - {day}")
    y = 750
    c.setFont("Helvetica", 12)
    for k, v in data.items():
        c.drawString(100, y, f"[{k}]: {str(v)[:60]}")
        y -= 25
    c.showPage()
    c.save()
    return buffer.getvalue()

# --- 3. UI 레이아웃 ---

st.set_page_config(page_title="스마트 식단 매니저", layout="centered")
st.title("🍱 스마트 식단 관리 매니저")
st.caption("최신 Gemini 3 엔진이 식단을 분석하고 시간대별로 안내합니다.")

uploaded_file = st.file_uploader("식단표 이미지를 업로드하세요", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    img = Image.open(uploaded_file)
    if st.button("🚀 식단 분석 시작"):
        with st.spinner('AI가 식단표를 정밀 분석 중입니다...'):
            try:
                result = analyze_menu(img)
                st.session_state['menu_data'] = json.loads(result)
                st.success("✅ 분석이 완료되었습니다!")
            except Exception as e:
                st.error(f"❌ 분석 실패: {e}")

# --- 4. 시간대별 자동 필터링 로직 ---

if 'menu_data' in st.session_state:
    days = ["월", "화", "수", "목", "금", "토", "일"]
    # 현재 시간 기준 (서버 시간이 다를 경우 timedelta 조정 가능)
    today_str = days[datetime.now().weekday()]
    hour = datetime.now().hour
    
    st.divider()
    st.header(f"📅 오늘의 식단 ({today_str}요일)")
    menu = st.session_state['menu_data'].get(today_str, {})

    # 시간대별 우선 노출
    if hour < 10:
        st.subheader("☀️ 지금은 [조식 & 간편식] 시간")
        col1, col2 = st.columns(2)
        col1.info(f"**조식**\n\n{menu.get('조식')}")
        col2.success(f"**간편식**\n\n{menu.get('간편식')}")
    elif 10 <= hour < 15:
        st.subheader("🍴 지금은 [중식] 시간")
        st.warning(menu.get('중식'))
    else:
        st.subheader("🌙 지금은 [석식 & 야식] 시간")
        col1, col2 = st.columns(2)
        col1.error(f"**석식**\n\n{menu.get('석식')}")
        col2.dark(f"**야식**\n\n{menu.get('야식')}")

    # 추가 정보
    with st.expander("💡 영양 정보 및 응원 메시지"):
        st.write(f"🍏 **메뉴 효능:** {menu.get('효능', '균형 잡힌 영양 식단입니다.')}")
        st.chat_message("assistant").write(menu.get("인사", "맛있게 드시고 힘찬 하루 보내세요!"))

    # PDF 다운로드
    pdf_bytes = create_pdf(today_str, menu)
    st.download_button("📄 오늘 식단 PDF 저장", pdf_bytes, f"menu_{today_str}.pdf", "application/pdf")
