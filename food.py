import streamlit as st

st.markdown("""
    <style>
    /* 1. 탭 리스트 전체 배경 및 하단 선 제거 */
    div[data-testid="stTabs"] [data-baseweb="tab-list"] {
        border-bottom: none !important;
        gap: 5px !important;
    }

    /* 2. 개별 탭 버튼 스타일 */
    div[data-testid="stTabs"] [data-baseweb="tab"] {
        height: 50px !important;
        background-color: #f0f2f6 !important;
        border-radius: 12px 12px 0px 0px !important;
        padding: 0px 15px !important;
        border: none !important;
    }

    /* 3. 활성화된 탭 (선택된 탭) 색상 */
    div[data-testid="stTabs"] [aria-selected="true"] {
        background-color: #A3C639 !important; /* 이미지의 연두색 */
    }
    
    div[data-testid="stTabs"] [aria-selected="true"] p {
        color: white !important;
        font-weight: bold !important;
    }

    /* 하단 빨간색 바 강제 숨김 */
    div[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
        background-color: transparent !important;
    }

    /* 4. ⭐ 하단 카드 박스 구현 (이 부분이 핵심입니다) */
    div[data-testid="stTabPanel"] {
        border: 2px solid #A3C639 !important; /* 연두색 테두리 */
        border-radius: 0px 15px 15px 15px !important;
        padding: 40px 20px !important;
        margin-top: -2px !important; /* 탭과 딱 붙게 설정 */
        background-color: white !important;
        min-height: 200px; /* 카드가 보일 수 있도록 최소 높이 설정 */
    }
    </style>
    """, unsafe_allow_html=True)

# 5. 탭 내부 콘텐츠 구성 (콘텐츠가 있어야 테두리가 보입니다)
tab_names = ["조식", "간편식", "중식", "석식", "야식"]
tabs = st.tabs(tab_names)

for i, tab in enumerate(tabs):
    with tab:
        # 중앙 정렬된 텍스트 구성
        st.markdown(f"""
            <div style="text-align: center;">
                <h2 style="margin-bottom: 10px;">{tab_names[i]} 메뉴 준비 중</h2>
                <hr style="border: 0.5px solid #eee; width: 60%; margin: 20px auto;">
                <p style="color: #666;">상세 메뉴 내용은 데이터를 불러오는 중입니다.</p>
            </div>
        """, unsafe_allow_html=True)
