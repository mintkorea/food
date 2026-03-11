import streamlit as st
import google.generativeai as genai
from PIL import Image
import json
from datetime import datetime
import time

# 1. 페이지 기본 설정
st.set_page_config(page_title="스마트 식단 매니저", layout="centered")

# 2. API 키 설정 (보안 및 에러 방지)
# 반드시 새로운 API 키를 발급받아 Secrets에 'GEMINI_API_KEY'로 저장해야 합니다.
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ Streamlit Cloud의 [Settings > Secrets]에 'GEMINI_API_KEY'를 등록해주세요.")
    st.stop()

genai.configure(api_key=api_key)

# 3. 식단 분석 함수 (404 및 429 에러 대응 로직)
def analyze_menu(image):
    # 'models/'를 명시하여 404 에러를 원천 차단합니다.
    model = genai.GenerativeModel('models/gemini-1.5-flash')

    prompt = """
    이미지에서 요일별 [중식, 석식] 메뉴를 추출해 JSON으로 응답해줘.
    형식: {"월": {"중식": "..", "석식": "..", "인사": ".."}, "화": {...}}
    반드시 마크다운 기호(```json 등) 없이 순수 JSON 데이터만 출력해.
    """
    
    # 503(서버 바쁨)이나 일시적 오류 시 2번 재시도
    for i in range(2):
        try:
            response = model.generate_content([prompt, image])
            res_text = response.text.strip()
            
            # JSON 텍스트 정제 (AI가 앞뒤에 설명을 붙일 경우 대비)
            if "{" in res_text:
                res_text = res_text[res_text.find("{"):res_text.rfind("}")+1]
            
            return json.loads(res_text)
        except Exception as e:
            if i < 1: # 첫 번째 실패 시 5초 대기 후 재시도
                time.sleep(5)
                continue
            raise e

# 4. 사용자 인터페이스(UI)
st.title("🍱 스마트 식단 관리 매니저")
st.write("주간 식단표를 업로드하면 오늘의 메뉴를 자동으로 알려드립니다.")

uploaded_file = st.file_uploader("식단표 이미지를 선택하세요", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="업로드된 식단표", use_container_width=True)
    
    if st.button("🚀 식단 분석 시작"):
        with st.spinner('AI가 식단표를 읽고 있습니다. 잠시만 기다려주세요...'):
            try:
                # 분석 실행
                result = analyze_menu(img)
                st.session_state['menu_data'] = result
                st.success("✅ 분석이 완료되었습니다!")
                st.rerun()
            except Exception as e:
                # 429 에러(할당량 초과)에 대한 친절한 안내
                if "429" in str(e):
                    st.error("❌ 요청이 너무 많습니다. 약 5분 뒤에 다시 시도해주세요.")
                else:
                    st.error(f"❌ 오류 발생: {e}")

# 5. 분석 결과 표시 (오늘의 요일에 맞춰 자동 필터링)
if 'menu_data' in st.session_state:
    days = ["월", "화", "수", "목", "금", "토", "일"]
    # 2026년 기준 현재 요일 인덱스 (0:월 ~ 6:일)
    today_idx = datetime.now().weekday()
    today_str = days[today_idx]
    
    st.divider()
    st.header(f"📅 오늘의 식단 ({today_str}요일)")
    
    # 해당 요일 데이터 가져오기
    day_menu = st.session_state['menu_data'].get(today_str)
    
    if day_menu:
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"🍴 **중식**\n\n{day_menu.get('중식', '정보 없음')}")
        with col2:
            st.error(f"🌙 **석식**\n\n{day_menu.get('석식', '정보 없음')}")
        
        # AI의 친절한 인사말 표시
        if day_menu.get("인사"):
            st.chat_message("assistant").write(day_menu["인사"])
    else:
        st.warning(f"죄송합니다. {today_str}요일 식단 정보를 찾을 수 없습니다.")

    # 전체 데이터 확인용 (개발용)
    with st.expander("📝 추출된 전체 데이터 보기"):
        st.json(st.session_state['menu_data'])
