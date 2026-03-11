import streamlit as st
import google.generativeai as genai
from PIL import Image
import json
from datetime import datetime
import time

# 1. API 설정
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ Streamlit Cloud의 [Settings > Secrets]에 GEMINI_API_KEY를 등록해주세요.")
    st.stop()

genai.configure(api_key=api_key)

# 2. 식단 분석 함수 (재시도 로직 포함)
def analyze_menu(image):
    # 가장 안정적인 모델 경로 지정 (404 에러 방지)
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    
    prompt = """
    이미지에서 이번 주 식단표를 찾아 요일별로 [조식, 중식, 석식] 메뉴를 추출해 JSON으로 응답해줘.
    형식: {"월": {"조식": "..", "중식": "..", "석식": "..", "인사": ".."}, ...}
    반드시 마크다운 없이 순수 JSON 텍스트만 응답해.
    """
    
    # 서버 혼잡(503) 시 최대 3번 자동 재시도
    for i in range(3):
        try:
            response = model.generate_content([prompt, image])
            res_text = response.text.strip()
            
            # JSON 클렌징 (불필요한 마크다운 제거)
            if "```json" in res_text:
                res_text = res_text.split("```json")[1].split("```")[0]
            elif "```" in res_text:
                res_text = res_text.split("```")[1].split("```")[0]
            
            return json.loads(res_text.strip())
        except Exception as e:
            if i < 2: # 3번 시도 전까지는 대기 후 재시도
                time.sleep(3)
                continue
            raise e

# 3. UI 레이아웃
st.set_page_config(page_title="스마트 식단 매니저", layout="centered")
st.title("🍱 스마트 식단 관리 매니저")

uploaded_file = st.file_uploader("식단표 이미지를 업로드하세요", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="선택된 식단표 이미지", use_container_width=True)
    
    if st.button("🚀 식단 분석 시작"):
        with st.spinner('AI가 식단을 분석 중입니다... (최대 10초 소요)'):
            try:
                result = analyze_menu(img)
                st.session_state['menu_data'] = result
                st.success("✅ 분석 완료!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ 분석 실패: {e}")

# 4. 오늘의 식단 자동 표시
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
    
    with st.expander("📝 전체 식단 데이터 보기"):
        st.json(st.session_state['menu_data'])
