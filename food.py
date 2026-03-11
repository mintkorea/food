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

# 2. 모델 로드 함수 (404 에러 방지용 다중 시도)
def get_stable_model():
    # 시도해볼 모델 이름 목록 (최신순)
    model_candidates = [
        'gemini-2.0-flash', 
        'models/gemini-2.0-flash', 
        'gemini-1.5-flash',
        'models/gemini-1.5-flash'
    ]
    
    for name in model_candidates:
        try:
            model = genai.GenerativeModel(name)
            # 모델이 정상인지 테스트 호출 (토큰 제한 확인 등)
            return model
        except:
            continue
    return None

# 3. 식단 분석 함수
def analyze_menu(image):
    model = get_stable_model()
    if not model:
        raise Exception("사용 가능한 Gemini 모델을 찾을 수 없습니다. API 권한을 확인해주세요.")
    
    prompt = """
    이미지에서 요일별 [조식, 중식, 석식] 메뉴를 추출해 JSON으로 응답해줘.
    형식: {"월": {"조식": "..", "중식": "..", "석식": "..", "인사": ".."}, ...}
    반드시 마크다운 없이 순수 JSON 텍스트만 응답해.
    """
    
    # 서버 혼잡(503) 시 재시도
    for i in range(3):
        try:
            response = model.generate_content([prompt, image])
            res_text = response.text.strip()
            
            # JSON 클렌징
            if "```json" in res_text:
                res_text = res_text.split("```json")[1].split("```")[0]
            elif "```" in res_text:
                res_text = res_text.split("```")[1].split("```")[0]
            
            return json.loads(res_text.strip())
        except Exception as e:
            if i < 2:
                time.sleep(3)
                continue
            raise e

# 4. UI 레이아웃 (생략 가능하나 확인용)
st.title("🍱 스마트 식단 관리 매니저")
uploaded_file = st.file_uploader("식단표 이미지를 업로드하세요", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    img = Image.open(uploaded_file)
    if st.button("🚀 식단 분석 시작"):
        with st.spinner('AI가 모델을 찾아 분석 중입니다...'):
            try:
                result = analyze_menu(img)
                st.session_state['menu_data'] = result
                st.success("✅ 분석 완료!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ 분석 실패: {e}")

# 결과 표시 로직은 기존과 동일...
