import streamlit as st
import google.generativeai as genai
from PIL import Image  # <-- 이 부분이 빠지면 NameError가 납니다!
import json
from datetime import datetime

# 1. API 설정
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("Secrets에 GEMINI_API_KEY를 설정해주세요.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. 식단 분석 함수
def analyze_menu(image):
    prompt = """
    이미지에서 이번 주 요일별 식단 데이터를 추출해줘.
    결과는 반드시 아래 구조의 순수한 JSON 데이터로만 응답해:
    {
      "월": {"조식": "..", "간편식": "..", "중식": "..", "석식": "..", "야식": "..", "인사": ".."},
      ...
      "일": {"조식": "..", ...}
    }
    """
    response = model.generate_content([prompt, image])
    res_text = response.text
    if "```json" in res_text:
        res_text = res_text.split("```json")[1].split("```")[0]
    return res_text.strip()

# 3. UI 구성
st.set_page_config(page_title="스마트 식단 매니저", layout="wide")
st.title("🍱 스마트 식단 관리 매니저")

uploaded_file = st.file_uploader("주간 식단표 이미지를 업로드하세요", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    # 에러 수정 포인트: PIL의 Image.open 사용
    img = Image.open(uploaded_file)
    
    if st.button("식단 분석 및 앱 실행"):
        with st.spinner('AI가 식단을 분석 중입니다...'):
            try:
                result = analyze_menu(img)
                st.session_state['menu_data'] = json.loads(result)
                st.success("분석 완료!")
            except Exception as e:
                st.error(f"분석 실패: {e}")

# 4. 시간대별 자동 표출 로직
if 'menu_data' in st.session_state:
    # 현재 요일 (월~일)
    days = ["월", "화", "수", "목", "금", "토", "일"]
    today_idx = datetime.now().weekday()
    today_str = days[today_idx]
    
    # 네비게이션바 (이전/다음날)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.header(f"📅 오늘의 식단 ({today_str}요일)")
    
    day_menu = st.session_state['menu_data'].get(today_str, {})
    now_hour = datetime.now().hour
    
    # 시간대별 우선순위 노출
    st.divider()
    
    # 아침 (오전 10시 전)
    if now_hour < 10:
        st.subheader("☀️ 지금은 [조식/간편식] 시간!")
        c1, c2 = st.columns(2)
        c1.info(f"**조식**\n\n{day_menu.get('조식')}")
        c2.success(f"**간편식**\n\n{day_menu.get('간편식')}")
        with st.expander("이후 식단(중식/석식) 보기"):
            st.write(f"중식: {day_menu.get('중식')}")
            st.write(f"석식: {day_menu.get('석식')}")
            
    # 점심 (10시~15시)
    elif 10 <= now_hour < 15:
        st.subheader("🍴 지금은 [중식] 시간!")
        st.warning(day_menu.get('중식'))
        with st.expander("이후 식단(석식/야식) 보기"):
            st.write(f"석식: {day_menu.get('석식')}")
            st.write(f"야식: {day_menu.get('야식')}")
            
    # 저녁 이후
    else:
        st.subheader("🌙 지금은 [석식/야식] 시간!")
        c1, c2 = st.columns(2)
        c1.error(f"**석식**\n\n{day_menu.get('석식')}")
        c2.dark(f"**야식**\n\n{day_menu.get('야식')}")
        with st.expander("내일 조식 미리보기"):
            next_day = days[(today_idx + 1) % 7]
            st.write(st.session_state['menu_data'].get(next_day, {}).get('조식'))

    # 격려말
    st.chat_message("assistant").write(day_menu.get("인사", "맛있게 드시고 힘내세요!"))
