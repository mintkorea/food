import streamlit as st

st.markdown("""
    <style>
    /* 1. 탭 전체 컨테이너: 하단 기본 회색 선 제거 */
    div[data-testid="stTabs"] [data-baseweb="tab-list"] {
        border-bottom: none !important;
        gap: 8px !important; /* 탭 버튼 사이 간격 */
    }

    /* 2. 개별 탭 버튼 기본 스타일 */
    div[data-testid="stTabs"] [data-baseweb="tab"] {
        height: 45px !important;
        background-color: #f0f2f6 !important; /* 비활성 탭 배경색 */
        border-radius: 12px 12px 0px 0px !important;
        padding: 0px 20px !important;
        border: none !important;
    }

    /* 3. 활성화된 탭 스타일: 빨간 선 대신 배경색 채우기 */
    div[data-testid="stTabs"] [aria-selected="true"] {
        background-color: #A3C639 !important; /* 이미지의 연두색 계열 */
        border: none !important;
    }
    
    /* 탭 안의 글자 색상 제어 */
    div[data-testid="stTabs"] [aria-selected="true"] p {
        color: white !important;
        font-weight: bold !important;
    }

    /* 4. 탭 하단 빨간색/검은색 인디케이터(바) 숨기기 */
    div[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
        background-color: transparent !important;
    }

    /* 5. 탭 하단 카드(내용물) 박스 스타일 */
    div[data-testid="stTabPanel"] {
        border: 2px solid #A3C639 !important; /* 연두색 테두리 */
        border-radius: 0px 20px 20px 20px !important;
        padding: 30px !important;
        margin-top: -2px !important; /* 탭 버튼과 완전히 밀착 */
        background-color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 테스트용 탭 구성
tabs = st.tabs(["조식", "간편식", "중식", "석식", "야식"])
with tabs[2]:
    st.markdown("<h2 style='text-align:center;'>순살닭볶음</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:gray;'>맑은뭇국, 흰쌀밥, 멕시칸마요범벅...</p>", unsafe_allow_html=True)
