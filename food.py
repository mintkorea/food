import streamlit as st
import google.generativeai as genai
from PIL import Image
import json
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io

# 1. API 설정 (404 에러 방지용 모델 경로 설정)
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("Secrets에 GEMINI_API_KEY를 설정해주세요.")
    st.stop()

# 기존의 모델 선언 부분을 아래와 같이 수정
try:
    # 1. 가장 표준적인 호출 방식
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception:
    # 2. 위 방식이 실패할 경우 대체 호출 방식
    model = genai.GenerativeModel('models/gemini-1.5-flash')

def analyze_menu(image):
    prompt = """
    이미지에서 이번 주 요일별 식단 데이터를 추출해서 JSON으로 응답해줘.
    형식: {"월": {"조식": "..", "간편식": "..", "중식": "..", "석식": "..", "야식": "..", "인사": "..", "효능": ".."}, ...}
    반드시 마크다운 기호 없이 순수한 JSON 텍스트만 출력해.
    """
    # 에러 발생 시 로그를 보기 위해 시도
    response = model.generate_content([prompt, image])
    return response.text.strip()

# PDF 생성 함수 (간이 버전)
def create_pdf(data, day_str):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont("Helvetica", 16) # 한글 폰트 설정이 복잡할 경우를 대비해 우선 영문 기반 구조
    p.drawString(100, 800, f"Weekly Menu Report ({day_str})")
    y = 750
    for meal, menu in data.items():
        p.drawString(100, y, f"[{meal}]: {menu[:50]}...")
        y -= 30
    p.showPage()
    p.save()
    return buffer.getvalue()

# 3. UI 구성
st.set_page_config(page_title="스마트 식단 매니저", layout="wide")
st.title("🍱 스마트 식단 관리 매니저")

uploaded_file = st.file_uploader("주간 식단표 이미지를 업로드하세요", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    img = Image.open(uploaded_file)
    if st.button("식단 분석 시작"):
        with st.spinner('AI가 분석 중... (404 에러 해결 중)'):
            try:
                result = analyze_menu(img)
                st.session_state['menu_data'] = json.loads(result)
                st.success("분석 완료!")
            except Exception as e:
                st.error(f"분석 실패: {e} \n(모델명을 다시 확인하거나 라이브러리를 업데이트 하세요)")

# 4. 시간대별 자동 표출 로직
if 'menu_data' in st.session_state:
    days = ["월", "화", "수", "목", "금", "토", "일"]
    # 현재 서버 시간 기준 (한국 시간 조정 필요 시 timedelta 사용)
    now = datetime.now()
    today_str = days[now.weekday()]
    
    st.header(f"📅 오늘의 식단 ({today_str}요일)")
    day_menu = st.session_state['menu_data'].get(today_str, {})
    hour = now.hour

    # 목요일 아침 예시: 조식+간편식 우선
    if hour < 10:
        st.subheader("☀️ 지금 가장 필요한 정보: 조식 & 간편식")
        c1, c2 = st.columns(2)
        c1.info(f"**조식**\n\n{day_menu.get('조식')}")
        c2.success(f"**간편식**\n\n{day_menu.get('간편식')}")
    elif 10 <= hour < 15:
        st.subheader("🍴 지금 가장 필요한 정보: 중식")
        st.warning(day_menu.get('중식'))
    else:
        st.subheader("🌙 지금 가장 필요한 정보: 석식 & 야식")
        c1, c2 = st.columns(2)
        c1.error(f"**석식**\n\n{day_menu.get('석식')}")
        c2.dark(f"**야식**\n\n{day_menu.get('야식')}")

    # 건강 정보 및 인사
    st.write("---")
    st.write(f"💡 **메뉴 효능:** {day_menu.get('효능', '건강한 한 끼로 에너지를 채우세요!')}")
    st.chat_message("assistant").write(day_menu.get("인사", "맛있게 드세요!"))

    # PDF 다운로드 버튼
    pdf_data = create_pdf(day_menu, today_str)
    st.download_button(label="📄 오늘 식단 PDF 다운로드", data=pdf_data, file_name=f"menu_{today_str}.pdf", mime="application/pdf")
