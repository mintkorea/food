import streamlit as st
from google import genai
from PIL import Image
import json
from datetime import datetime
import io
import time

# --- 1. 설정 ---
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("API 키를 Secrets에 등록해주세요.")
    st.stop()

client = genai.Client(api_key=api_key)
MODEL_ID = "gemini-3-flash-preview"

# --- 2. 분석 함수 (상태 메시지 추가) ---
def analyze_menu(image):
    prompt = """
    이미지에서 이번 주 식단 데이터를 추출해서 JSON으로만 응답해줘.
    형식: {"월": {"조식": "..", "중식": "..", "석식": "..", "인사": ".."}, ...}
    """
    
    # 상태 알림창 생성
    status = st.empty()
    
    try:
        status.info("🔍 Gemini AI가 이미지를 읽고 있습니다...")
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=[prompt, image]
        )
        
        status.info("📝 데이터를 정리하는 중입니다...")
        res_text = response.text.strip()
        
        # JSON 문자열 추출 로직
        if "```json" in res_text:
            res_text = res_text.split("```json")[1].split("```")[0]
        elif "```" in res_text:
            res_text = res_text.split("```")[1].split("```")[0]
            
        status.empty() # 상태 메시지 삭제
        return res_text.strip()
        
    except Exception as e:
        status.empty()
        raise e

# --- 3. UI 구성 ---
st.set_page_config(page_title="스마트 식단 매니저", layout="centered")
st.title("🍱 스마트 식단 관리 매니저")

uploaded_file = st.file_uploader("식단표 이미지를 업로드하세요", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    img = Image.open(uploaded_file)
    
    # 버튼 클릭 시 세션 초기화 및 분석 시작
    if st.button("🚀 식단 분석 시작"):
        try:
            # 분석 시작 전 기존 데이터 삭제
            if 'menu_data' in st.session_state:
                del st.session_state['menu_data']
                
            result = analyze_menu(img)
            st.session_state['menu_data'] = json.loads(result)
            st.success("✅ 분석 완료!")
            st.rerun() # 화면 새로고침하여 결과 표시
        except Exception as e:
            st.error(f"❌ 오류 발생: {e}")

# --- 4. 결과 표시 로직 ---
if 'menu_data' in st.session_state:
    days = ["월", "화", "수", "목", "금", "토", "일"]
    today_str = days[datetime.now().weekday()]
    
    st.divider()
    st.header(f"📅 오늘의 식단 ({today_str}요일)")
    
    menu = st.session_state['menu_data'].get(today_str, {})
    
    if menu:
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**중식**\n\n{menu.get('중식', '정보 없음')}")
        with col2:
            st.error(f"**석식**\n\n{menu.get('석식', '정보 없음')}")
        
        st.chat_message("assistant").write(menu.get("인사", "맛있게 드세요!"))
    else:
        st.warning("오늘의 식단 데이터를 찾을 수 없습니다. 분석 결과를 확인해주세요.")
