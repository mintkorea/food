import streamlit as st
import google.generativeai as genai
from PIL import Image
import json
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io

# --- 1. API 및 모델 설정 ---
# 404 에러를 방지하기 위해 최신 라이브러리 방식과 모델 경로를 사용합니다.
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ Streamlit Cloud의 [Settings > Secrets]에 GEMINI_API_KEY를 등록해주세요.")
    st.stop()

genai.configure(api_key=api_key)

# 모델 선언 (가장 안정적인 호출 방식)
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception:
    model = genai.GenerativeModel('models/gemini-1.5-flash')

# --- 2. 주요 기능 함수 ---

def analyze_menu(image):
    """이미지에서 식단 데이터를 추출하여 JSON으로 반환"""
    prompt = """
    당신은 식단 분석 전문가입니다. 업로드된 이미지에서 이번 주 식단표를 찾아 정리하세요.
    1. 요일별(월~일)로 [조식, 간편식, 중식, 석식, 야식] 메뉴를 추출하세요.
    2. 각 요일별로 메뉴와 어울리는 '효능(이점)'과 따뜻한 '인사말'을 한 문장씩 작성하세요.
    3. 결과는 반드시 마크다운 기호(```json 등) 없이 순수한 JSON 형식으로만 응답하세요.
    형식 예시:
    {
      "월": {"조식": "..", "간편식": "..", "중식": "..", "석식": "..", "야식": "..", "효능": "..", "인사": ".."},
      ...
    }
    """
    response = model.generate_content([prompt, image])
    res_text = response.text.strip()
    
    # 만약 AI가 마크다운 블록을 포함했을 경우 제거
    if "```json" in res_text:
        res_text = res_text.split("```json")[1].split("```")[0]
    elif "```" in res_text:
        res_text = res_text.split("```")[1].split("```")[0]
        
    return res_text.strip()

def create_pdf(day, data):
    """오늘의 식단을 간단한 PDF 파일로 생성"""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(100, 800, f"Today's Menu Report ({day})")
    
    c.setFont("Helvetica", 12)
    y_position = 750
    for key, value in data.items():
        line = f"[{key}]: {str(value)[:60]}..."
        c.drawString(100, y_position, line)
        y_position -= 25
        
    c.showPage()
    c.save()
    return buffer.getvalue()

# --- 3. 앱 UI 레이아웃 ---

st.set_page_config(page_title="스마트 식단 매니저", layout="centered")
st.title("🍱 스마트 식단 관리 매니저")
st.caption("식단표 이미지를 올리면 시간대에 맞춰 최적의 정보를 보여줍니다.")

uploaded_file = st.file_uploader("주간 식단표 이미지를 업로드하세요 (PNG, JPG)", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    img = Image.open(uploaded_file)
    
    if st.button("🚀 식단 분석 시작"):
        with st.spinner('AI가 식단을 분석하고 있습니다. 잠시만 기다려주세요...'):
            try:
                raw_data = analyze_menu(img)
                st.session_state['menu_json'] = json.loads(raw_data)
                st.success("✅ 분석이 완료되었습니다!")
            except Exception as e:
                st.error(f"❌ 분석 중 오류 발생: {e}")
                st.info("Tip: 라이브러리 버전이 낮거나 모델명이 변경되었을 수 있습니다.")

# --- 4. 시간대별 자동 노출 로직 ---

if 'menu_json' in st.session_state:
    # 한국 요일 설정
    weekdays = ["월", "화", "수", "목", "금", "토", "일"]
    now = datetime.now()
    today_str = weekdays[now.weekday()]
    hour = now.hour
    
    st.divider()
    st.header(f"📅 오늘의 식단 ({today_str}요일)")
    
    today_menu = st.session_state['menu_json'].get(today_str, {})
    
    # 시간대별 섹션 배치
    if hour < 10:
        st.subheader("☀️ 아침 식사 및 간편식")
        c1, c2 = st.columns(2)
        c1.metric("조식", "든든한 한끼")
        c1.write(today_menu.get("조식", "정보 없음"))
        c2.metric("간편식", "빠르고 가볍게")
        c2.write(today_menu.get("간편식", "정보 없음"))
    elif 10 <= hour < 15:
        st.subheader("🍴 맛있는 점심 식사")
        st.warning(today_menu.get("중식", "정보 없음"))
    else:
        st.subheader("🌙 저녁 식사 및 야식")
        c1, c2 = st.columns(2)
        c1.error(f"석식: {today_menu.get('석식', '정보 없음')}")
        c2.dark(f"야식: {today_menu.get('야식', '정보 없음')}")

    # 추가 정보 (효능 및 인사)
    with st.expander("✨ 더 건강하게 먹는 팁 & 응원", expanded=True):
        st.write(f"🍏 **이 메뉴의 장점:** {today_menu.get('효능', '균형 잡힌 영양소 섭취가 가능합니다.')}")
        st.chat_message("assistant").write(today_menu.get("인사", "오늘 하루도 정말 고생 많으셨습니다! 맛있게 드세요."))

    # PDF 다운로드
    pdf_bytes = create_pdf(today_str, today_menu)
    st.download_button(
        label="📄 오늘 식단표 PDF 다운로드",
        data=pdf_bytes,
        file_name=f"menu_{today_str}.pdf",
        mime="application/pdf"
    )
    
    if st.button("🔄 다른 요일 식단 보기"):
        st.json(st.session_state['menu_json'])
