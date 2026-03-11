import streamlit as st
import google.generativeai as genai
from PIL import Image
import json
from datetime import datetime

# 1. API 키 설정 (보안 준수)
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ Streamlit Secrets에 GEMINI_API_KEY를 등록해주세요.")
    st.stop()

genai.configure(api_key=api_key)

# 2. 식단 분석 함수 (군더더기 없는 표준 로직)
def analyze_menu(image):
    # 가장 오류가 적은 표준 모델 경로 사용
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    
    prompt = """
    이미지에서 요일별 식단(조식, 중식, 석식)을 추출해 JSON으로 응답해줘.
    형식: {"월": {"중식": "..", "석식": "..", "인사": ".."}, "화": {...}}
    마크다운 없이 순수 JSON 텍스트만 출력해.
    """
    
    try:
        response = model.generate_content([prompt, image])
        res_text = response.text.strip()
        
        # JSON 데이터만 깔끔하게 추출
        if "```json" in res_text:
            res_text = res_text.split("```json")[1].split("```")[0]
        elif "```" in res_text:
            res_text = res_text.split("```")[1].split("```")[0]
            
        return json.loads(res_text.strip())
    except Exception as e:
        raise e

# 3. 메인 UI
st.set_page_config(page_title="스마트 식단 매니저", layout="centered")
st.title("🍱 스마트 식단 관리 매니저")

uploaded_file = st.file_uploader("주간 식단표 이미지를 업로드하세요", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="업로드된 식단표", use_container_width=True)
    
    if st.button("🚀 식단 분석 시작"):
        # 사용량 제한(429)을 피하기 위해 한 번만 신중하게 호출
        with st.spinner('AI가 식단을 분석 중입니다...'):
            try:
                result = analyze_menu(img)
                st.session_state['menu_data'] = result
                st.success("✅ 분석 성공!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ 분석 실패: {e}")
                st.info("Tip: 'Quota exceeded' 에러라면 5분 뒤에 다시 시도해주세요.")

# 4. 오늘의 식단 자동 필터링 표시
if 'menu_data' in st.session_state:
    days = ["월", "화", "수", "목", "금", "토", "일"]
    # 2026년 기준 현재 요일 계산
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
