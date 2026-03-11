import streamlit as st
import google.generativeai as genai
from PIL import Image
import json
from datetime import datetime
import os

# 코드에 직접 키를 쓰지 않고, 시스템이나 Streamlit 설정에서 불러옵니다.
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("API 키가 설정되지 않았습니다. 환경 변수를 확인해주세요.")
else:
    genai.configure(api_key=api_key)

# 1. Gemini API 설정
genai.configure(api_key="AIzaSyAbCNCDKPHqFdvlM60I79nO9Z4RMye0IbQ") # 발급받은 키 입력
model = genai.GenerativeModel('gemini-1.5-flash')

def analyze_menu(image):
    # 프롬프트를 조금 더 명확하게 다듬었습니다.
    prompt = """
    당신은 식단 분석 전문가입니다. 업로드된 주간 식단표 이미지에서 데이터를 추출하세요.
    1. 요일별(월~일)로 조식, 간편식, 중식, 석식, 야식 메뉴를 정확히 분리하세요.
    2. 결과는 반드시 마크다운 기호 없이 순수한 JSON 형식으로만 응답하세요.
    3. JSON 구조 예시:
    {
      "목요일": {
        "조식": "메뉴내용",
        "간편식": "메뉴내용",
        "중식": "메뉴내용",
        "석식": "메뉴내용",
        "야식": "메뉴내용",
        "격려말": "오늘도 파이팅!"
      }
    }
    """
    # 에러 방지를 위해 stream=False를 명시하거나 모델명을 재확인합니다.
    try:
        response = model.generate_content([prompt, image])
        # JSON 문자열만 깔끔하게 뽑아내는 코드
        res_text = response.text
        if "```json" in res_text:
            res_text = res_text.split("```json")[1].split("```")[0]
        return res_text.strip()
    except Exception as e:
        return f"Error: {str(e)}"

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
