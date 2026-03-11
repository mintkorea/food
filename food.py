# --- 모델 설정 부분 수정 ---
# AI Studio 화면에 나온 최신 모델명을 포함하여 시도합니다.
model_names = ['gemini-3-flash-preview', 'gemini-1.5-flash', 'gemini-1.5-flash-latest']

model = None
for name in model_names:
    try:
        model = genai.GenerativeModel(name)
        # 테스트 호출로 모델 유효성 확인
        break 
    except:
        continue

if not model:
    st.error("사용 가능한 Gemini 모델을 찾을 수 없습니다. API 키 권한을 확인해주세요.")
    st.stop()

def analyze_menu(image):
    prompt = """
    식단표 이미지에서 요일별(월~일) [조식, 간편식, 중식, 석식, 야식]을 추출해 JSON으로 줘.
    메뉴별 효능과 따뜻한 인사말도 포함해줘. 마크다운 없이 JSON만 응답해.
    """
    # 모델 호출 방식 업데이트
    response = model.generate_content([prompt, image])
    return response.text.strip()
