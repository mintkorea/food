import time

def analyze_menu(image):
    prompt = """
    이미지에서 요일별 [조식, 간편식, 중식, 석식, 야식] 식단 데이터를 추출해서 JSON으로 응답해줘.
    반드시 마크다운 없이 순수 JSON만 응답해.
    """
    
    # 서버 상황에 따라 모델을 바꿔가며 최대 3번 시도합니다.
    target_models = [MODEL_ID, "gemini-1.5-flash"] 
    
    for model_name in target_models:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=[prompt, image]
            )
            res_text = response.text.strip()
            if "```json" in res_text:
                res_text = res_text.split("```json")[1].split("```")[0]
            return res_text.strip()
        except Exception as e:
            if "503" in str(e):
                st.warning(f"⚠️ {model_name} 모델 서버가 혼잡합니다. 잠시 후 재시도합니다...")
                time.sleep(2) # 2초 대기 후 다음 시도
                continue
            else:
                raise e
    
    raise Exception("모든 모델 서버가 현재 응답하지 않습니다. 잠시 후 다시 시도해주세요.")
