
import streamlit as st

st.markdown("""
    <style>
    /* 1. 기본 탭의 하단 빨간색 바와 밑줄 제거 */
    div[data-testid="stTab"] {
        border: none !important;
        background-color: transparent !important;
    }
    
    div[data-testid="stTab"] p {
        font-size: 16px;
        font-weight: 600;
        color: #888; /* 비활성 탭 글자색 */
    }

    /* 2. 탭 버튼을 '카드 형태'로 변형 */
    div[data-testid="stTab"] {
        background-color: #f0f2f6; /* 비활성 배경색 */
        border-radius: 12px 12px 0 0 !important;
        padding: 8px 16px !important;
        margin-right: 4px !important;
        min-width: 80px;
        text-align: center;
    }

    /* 3. 활성화된 탭 스타일 (이미지의 색감 반영) */
    div[aria-selected="true"] {
        background-color: #A3C639 !important; /* 목표 이미지의 연두색 계열 */
        color: white !important;
    }
    
    div[aria-selected="true"] p {
        color: white !important;
    }

    /* 4. 탭 하단 콘텐츠 박스와 연결 */
    div[data-testid="stTabPanel"] {
        border: 2px solid #A3C639 !important;
        border-radius: 0 15px 15px 15px !important;
        padding: 30px !important;
        margin-top: -1px !important; /* 탭과 박스 사이 간격 제거 */
    }
    </style>
    """, unsafe_allow_html=True)

# 탭 구현부
tabs = st.tabs(["조식", "간편식", "중식", "석식", "야식"])
with tabs[2]: # 중식
    st.markdown("### 순살닭볶음")
    st.write("맑은뭇국, 흰쌀밥, 멕시칸마요범벅...")
