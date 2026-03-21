import streamlit as st

# CSS 주입: 탭과 카드 사이의 여백 제거 및 스타일 정렬
st.markdown("""
    <style>
    /* 1. 탭 전체 컨테이너 여백 조정 */
    div[data-testid="stTabs"] {
        gap: 0px !important;
    }

    /* 2. 개별 탭 버튼 스타일 */
    button[data-testid="stMarker"] {
        border-radius: 10px 10px 0px 0px !important; /* 상단만 둥글게 */
        margin-bottom: -1px !important; /* 카드 테두리와 겹치게 하여 경계선 제거 */
        border-bottom: none !important;
    }

    /* 3. 탭 하단 콘텐츠(카드 부분) 박스 스타일 */
    div[data-testid="stTabPanel"] {
        background-color: white;
        border: 2px solid #A3C639; /* 이미지의 연두색 계열 예시 */
        border-radius: 0px 20px 20px 20px !important; /* 탭 연결부 제외 둥글게 */
        padding: 40px 20px !important;
        margin-top: 0px !important;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
    }
    
    /* 4. 메뉴 텍스트 중앙 정렬 및 여백 */
    .menu-title {
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }
    .menu-details {
        text-align: center;
        color: #666;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

# 탭 생성
tab1, tab2, tab3, tab4, tab5 = st.tabs(["조식", "간편식", "중식", "석식", "야식"])

with tab3: # 중식 예시
    st.markdown('<p class="menu-title">순살닭볶음</p>', unsafe_allow_html=True)
    st.markdown('<hr style="border:0.5px solid #eee; width:50%; margin:auto; margin-bottom:20px;">', unsafe_allow_html=True)
    st.markdown('<p class="menu-details">맑은뭇국, 흰쌀밥, 멕시칸마요범벅, 양념깻잎지,<br>깍두기, 원두커피</p>', unsafe_allow_html=True)
