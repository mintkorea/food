import streamlit as st

# 1. 테마 색상 정의
color_theme = {
    "조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"
}

if 'active_meal' not in st.session_state:
    st.session_state.active_meal = "중식"

current = st.session_state.active_meal

# 2. CSS: 간격 파괴 및 가로 고정
st.markdown(f"""
<style>
    /* 전체 배경 및 컨테이너 여백 제거 */
    .main .block-container {{ 
        max-width: 500px !important; 
        padding: 10px 5px !important; 
    }}

    /* 버튼들을 감싸는 부모 컨테이너: 간격 0 고정 */
    .button-container {{
        display: flex !important;
        flex-direction: row !important;
        justify-content: space-between !important;
        gap: 4px !important; /* 버튼 사이 아주 미세한 간격 */
        width: 100% !important;
        margin: 0 auto !important;
    }}

    /* 개별 버튼이 들어갈 공간 (20%씩 정확히 배분) */
    .button-item {{
        flex: 1 !important;
        min-width: 0 !important;
    }}

    /* Streamlit 버튼 디자인 덮어쓰기 */
    div.stButton > button {{
        width: 100% !important;
        height: 45px !important;
        padding: 0 !important;
        font-size: 14px !important;
        font-weight: bold !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        transition: 0.2s;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}

    /* 선택된 버튼 강조 효과 */
    .active-btn button {{
        border: 3px solid white !important;
        box-shadow: 0 0 10px rgba(0,0,0,0.2) !important;
    }}

    .meal-card {{
        border: 2px solid {color_theme[current]};
        border-radius: 15px; padding: 20px 10px; text-align: center;
        background-color: white; margin-bottom: 15px;
    }}
</style>
""", unsafe_allow_html=True)

# 3. 상단 식단 카드
st.markdown(f'<div class="meal-card"><h2 style="color: {color_theme[current]}; margin: 0;">{current}</h2></div>', unsafe_allow_html=True)

# 4. 버튼 배치 (st.columns 대신 컨테이너 활용)
# 텍스트가 아닌 실제 버튼을 CSS 클래스로 감싸서 배치
with st.container():
    # HTML 태그로 가로 정렬 시작
    st.write('<div class="button-container">', unsafe_allow_html=True)
    
    # 5개의 버튼 생성
    for meal, color in color_theme.items():
        is_active = "active-btn" if current == meal else ""
        
        # 각 버튼을 개별 아이템으로 감싸고 스타일 주입
        st.markdown(f"""
            <style>
                div[data-testid="stVerticalBlock"] > div:nth-child({list(color_theme.keys()).index(meal) + 3}) button {{
                    background-color: {color} !important;
                    opacity: {1.0 if current == meal else 0.5} !important;
                }}
            </style>
        """, unsafe_allow_html=True)
        
        # 가로 배치를 위한 컬럼 활용 (이번엔 간격을 0으로 세팅)
        # 단, st.columns 안의 요소를 CSS로 강하게 묶습니다.
    
    # 다시 안정적인 columns 호출하되, CSS로 강제 결합
    cols = st.columns(5)
    for i, meal in enumerate(color_theme.keys()):
        if cols[i].button(meal, key=f"final_btn_{meal}"):
            st.session_state.active_meal = meal
            st.rerun()

    st.write('</div>', unsafe_allow_html=True)
