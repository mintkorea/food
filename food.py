import streamlit as st
import google.generativeai as genai
from PIL import Image
import json
from datetime import datetime

# 1. API 설정 (보안 준수)
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ Secrets에 GEMINI_API_KEY가 없습니다. 설정을 확인해 주세요.")
    st.stop()

genai.configure(api_key=api_key)

# 2. 식단 분석 함수 (404 에러 원천 차단)
def analyze_menu(image):
    # 가장 안정적인 표준 모델 경로 지정
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    
    prompt = """
    이미지 속 식단표에서 요일별 [중식, 석식] 메뉴를 추출해 JSON으로 응답해줘.
    형식: {"월": {"중식": "..", "석식": "..", "인사": ".."}, ...}
    마크다운 없이 순수 JSON 데이터만 출력해.
    """
    
    try:
        response = model.generate_content([prompt, image])
        res_text = response.text.strip()
        
        # JSON 데이터 클렌징
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

uploaded_file = st.file_uploader("식단표 이미지를 업로드하세요", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="업로드된 식단표", use_container_width=True)
    
    if st.button("🚀 식단 분석 시작"):
        with st.spinner('AI가 식단을 정밀 분석 중입니다...'):
            try:
                # 429 에러 방지를 위해 한 번만 신중하게 호출
                result = analyze_menu(img)
                st.session_state['menu_data'] = result
                st.success("✅ 분석 완료!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ 오류 발생: {e}")
                st.info("Tip: 429 에러(Quota exceeded) 발생 시 약 5분 뒤에 다시 시도해 주세요.")

# 4. 결과 표시 로직
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
