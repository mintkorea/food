import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime

st.set_page_config(page_title="성의교정 식단 변환기", layout="wide")

# 가독성을 높이는 커스텀 CSS
st.markdown("""
    <style>
    .menu-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        border-top: 6px solid #2E7D32;
        min-height: 150px;
    }
    .main-menu { font-size: 1.2rem; font-weight: bold; color: #2E7D32; margin-bottom: 8px; }
    .side-menu { font-size: 0.95rem; color: #555; line-height: 1.5; }
    </style>
    """, unsafe_allow_html=True)

st.title("🍱 식단표 스캐너 & 엑셀 변환")

with st.sidebar:
    st.header("📂 파일 업로드")
    uploaded_file = st.file_uploader("식단표 이미지를 올려주세요", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    # 데이터 (예시 데이터 - 실제 운영시 OCR 연동 가능)
    data = {
        "구분": ["중식", "석식", "야식"],
        "메인메뉴": ["소세지카레라이스", "춘천닭갈비", "우렁강된장덮밥"],
        "상세내용": [
            "완두콩밥, 유부유부국, 실곤약초무침, 깍두기, 미숫가루",
            "유채된장국, 흰쌀밥, 청포묵무침, 와사비쌈무, 열무김치",
            "미역국, 부추야채전, 동그랑땡구이, 깍두기, 포도주스"
        ]
    }
    df = pd.DataFrame(data)

    # 1. 시각적 카드 레이아웃
    cols = st.columns(3)
    icons = ["🍴 중식", "🌙 석식", "🌕 야식"]
    
    for i, row in df.iterrows():
        with cols[i]:
            st.markdown(f"""
                <div class="menu-card">
                    <h3 style='margin-top:0;'>{icons[i]}</h3>
                    <div class="main-menu">{row['메인메뉴']}</div>
                    <div class="side-menu">{row['상세내용']}</div>
                </div>
            """, unsafe_allow_html=True)

    st.divider()

    # 2. 엑셀 다운로드 (에러 방지용 openpyxl 엔진 사용)
    st.subheader("📊 데이터 확인 및 엑셀 저장")
    st.table(df)

    output = BytesIO()
    # 엔진을 openpyxl로 변경하여 안정성을 높였습니다.
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='식단표')
    
    st.download_button(
        label="📥 엑셀 파일로 내보내기",
        data=output.getvalue(),
        file_name=f"성의교정_식단_{datetime.now().strftime('%m%d')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("왼쪽 메뉴에서 식단표 이미지를 선택하면 분석이 시작됩니다.")
