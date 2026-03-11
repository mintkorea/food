import google.generativeai as genai
from PIL import Image

# 발급받은 키를 여기에 넣으세요
genai.configure(api_key="AIzaSyAbCNCDKPHqFdvlM60I79nO9Z4RMye0IbQ")

# 분석 모델 설정 (이미지 인식에 특화된 flash 모델)
model = genai.GenerativeModel('gemini-1.5-flash')

# 식단표 이미지 로드
img = Image.open('식단표_이미지.png') 

# AI에게 줄 미션 (프롬프트)
prompt = """
이미지에서 요일별 식단을 추출해줘. 
특히 목요일은 [조식/간편식], [중식], [석식/야식] 그룹으로 나누어서 데이터를 정리해줘.
결과는 반드시 JSON 형식으로만 출력해.
"""

response = model.generate_content([prompt, img])
print(response.text)
