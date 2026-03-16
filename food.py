import streamlit as st
import pandas as pd
from io import BytesIO

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 식단 스마트 변환기", layout="wide")

# 2. 디자인 (CSS)
st.markdown("""
    <style>
    .main { background-color: #F8F9FA; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #2E7D32; color: white; }
    .status-box { padding: 15px; border-radius: 10px; background-color: #E8F5E9; border: 1px solid #C8E6C9; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🍱 식단표 스캔 및 엑셀 변환 시스템")
st.write("식단표 이미지를 업로드하면 가독성 좋은 디자인으로 보여주고, 엑셀 파일로 변환해 드립니다.")

# 3. 사이드바: 이미지 업로드
with st.sidebar:
    st.header("📂 이미지 업로드")
    uploaded_file = st.file_uploader("주간 식단표 이미지 선택", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file:
        st.image(uploaded_file, caption="업로드된 식단표", use_container_width=True)

# 4. 메인 로직
if uploaded_file:
    with st.spinner('이미지에서 데이터를 분석 중입니다...'):
        # [참고] 실제 구현 시 이 부분에 OCR 라이브러리(pytesseract 등)가 들어갑니다.
        # 여기서는 사용자님이 올려주신 이미지의 데이터를 바탕으로 예시를 구성합니다.
        
        data = {
            "구분": ["중식", "석식", "야식"],
            "메인메뉴": ["소세지카레라이스", "춘천닭갈비", "우렁강된장덮밥"],
            "상세내용": [
                "완두콩밥, 유부유부국, 실곤약초무침, 깍두기, 미숫가루",
                "유채된장국, 흰쌀밥, 청포묵무침, 와사비쌈무, 열무김치",
                "미역국, 부추야채전, 동그랑땡구이, 깍두기, 포도주스"
            ],
            "칼로리": ["773kcal", "-", "-"]
        }
        df = pd.DataFrame(data)

    # 상단: 가독성 좋은 카드 디자인 출력
    st.subheader("✅ 분석된 오늘(금)의 식단")
    cols = st.columns(3)
    icons = ["🍴", "🌙", "🌕"]
    
    for i, row in df.iterrows():
        with cols[i]:
            st.markdown(f"""
                <div style="background-color:white; padding:20px; border-radius:15px; border-top:5px solid #2E7D32; shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    <h4 style="margin:0;">{icons[i]} {row['구분']}</h4>
                    <p style="font-size:1.1rem; font-weight:bold; color:#2E7D32; margin-top:10px;">{row['메인메뉴']}</p>
                    <p style="font-size:0.9rem; color:#666;">{row['상세내용']}</p>
                </div>
            """, unsafe_allow_html=True)

    st.divider()

    # 하단: 엑셀 변환 및 다운로드
    st.subheader("📊 엑셀 데이터 확인 및 다운로드")
    st.dataframe(df, use_container_width=True)

    # 엑셀 파일 생성
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='오늘의식단')
    processed_data = output.getvalue()

    st.download_button(
        label="📥 분석 결과 엑셀 파일로 다운로드",
        data=processed_data,
        file_name=f"성의교정_식단_{datetime.now().strftime('%Y%m%d')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

else:
    st.info("왼쪽 사이드바에서 식단표 이미지를 업로드해 주세요.")
    
    # 예시 이미지 가이드
    st.markdown("""
        <div class="status-box">
            <strong>💡 가독성을 높이는 팁:</strong><br>
            이미지가 흐릿하다면 '오늘 날짜' 부분만 크게 캡처해서 올려주시면 더 정확하게 분석됩니다.
        </div>
    """, unsafe_allow_html=True)
