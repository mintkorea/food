import streamlit as st
import google.generativeai as genai
from PIL import Image
import json
from datetime import datetime

# 1. API 키 설정
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("Secrets에 API 키가 등록되지 않았습니다.")
    st.stop()

genai.configure(api_key=api_key)

# 2. 식단 분석 함수 (핵심 에러 방어)
def analyze_menu(image):
    # 'models/'를 명확히 붙여야 404 에러가 나지 않습니다.
   model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    prompt = """
    이미지에서 요일별 식단(중식, 석식)을 추출해서 JSON으로 출력해줘.
    형식: {"월": {"중식": "..", "석식": "..", "인사": ".."}, "화": {...}}
    반드시 마크다운 없이 JSON 텍스트만 출력할 것.
    """
    
    try:
        response = model.generate_content([prompt, image])
        res_text = response.text.strip()
        
        # 불필요한 마크다운 기호 제거
        if "```" in res_text:
            res_text = res_text.split("```")[1].replace("json", "").strip()
            
        return json.loads(res_text)
    except Exception as e:
        raise e

# 3. 메인 UI
st.title("🍱 성의교정 스마트 식단 매니저")

uploaded_file = st.file_uploader("주간 식단표 이미지를 올려주세요", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="업로드된 식단표", use_container_width=True)
    
    if st.button("🚀 식단 분석 시작"):
        with st.spinner('AI가 분석 중입니다...'):
            try:
                # 분석 실행
                result = analyze_menu(img)
                st.session_state['menu_data'] = result
                st.success("분석 완료!")
                st.rerun()
            except Exception as e:
                st.error(f"오류가 발생했습니다: {str(e)}")
                if "404" in str(e):
                    st.info("모델을 찾을 수 없습니다. 사용 가능한 모델을 확인하세요.")
                elif "429" in str(e):
                    st.info("서버 할당량 초과입니다. 5분 후에 다시 시도해 주세요.")

# 4. 결과 출력
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
