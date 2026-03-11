import streamlit as st
import google.generativeai as genai
from PIL import Image
import json
from datetime import datetime

# 1. Gemini API 설정
genai.configure(api_key="AIzaSyAbCNCDKPHqFdvlM60I79nO9Z4RMye0IbQ") # 발급받은 키 입력
model = genai.GenerativeModel('gemini-1.5-flash')

def analyze_menu(image):
    prompt = """
    이 식단표 이미지에서 이번 주 식단 데이터를 추출해서 JSON 형식으로 응답해줘.
    형식은 { "요일": { "조식": "메뉴", "간편식": "메뉴", "중식": "메뉴", "석식": "메뉴", "야식": "메뉴" } } 로 해줘.
    추가로 각 메뉴의 건강 효능 1가지와 따뜻한 격려말 1개도 JSON에 포함해줘.
    """
    response = model.generate_content([prompt, image])
    # JSON 문자열만 추출하는 로직 (간소화)
    return response.text.replace('```json', '').replace('```', '').strip()

# 2. UI 구성
st.title("🍱 스마트 식단 관리 매니저")

uploaded_file = st.file_uploader("주간 식단표 이미지를 업로드하세요", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='업로드된 식단표', use_column_width=True)
    
    if st.button("식단 분석 시작"):
        with st.spinner('AI가 식단을 분석하고 있습니다...'):
            try:
                raw_json = analyze_menu(image)
                menu_data = json.loads(raw_json)
                st.session_state['menu_data'] = menu_data
                st.success("분석 완료!")
            except Exception as e:
                st.error(f"분석 중 오류가 발생했습니다: {e}")

# 3. 시간대별 자동 표출 로직
if 'menu_data' in st.session_state:
    # 예시로 '목요일' 데이터 사용 (실제로는 datetime 활용 가능)
    today = "목요일" 
    day_menu = st.session_state['menu_data'].get(today, {})
    
    st.header(f"📅 오늘의 식단 ({today})")
    
    # 시간대에 따른 우선순위 배치 (사용자 요청 반영)
    now_hour = datetime.now().hour
    
    if now_hour < 10: # 아침 시간
        st.subheader("☀️ 아침 & 간편식")
        col1, col2 = st.columns(2)
        col1.metric("조식", day_menu.get("조식", "정보 없음"))
        col2.metric("간편식", day_menu.get("간편식", "정보 없음"))
    elif 10 <= now_hour < 15: # 점심 시간
        st.subheader("🍴 점심 식사")
        st.info(day_menu.get("중식", "정보 없음"))
    else: # 저녁 & 야식
        st.subheader("🌙 저녁 & 야식")
        col1, col2 = st.columns(2)
        col1.metric("석식", day_menu.get("석식", "정보 없음"))
        col2.metric("야식", day_menu.get("야식", "정보 없음"))

    # 격려말 출력
    st.write("---")
    st.heart(day_menu.get("격려말", "오늘 하루도 멋지게 보내세요!"))
