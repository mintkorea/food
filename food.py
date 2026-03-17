import streamlit as st

# 1. 색상 테마 및 초기 상태
color_theme = {
    "조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"
}

if 'active_meal' not in st.session_state:
    st.session_state.active_meal = "중식"

current = st.session_state.active_meal

# 2. 강력한 CSS 스타일링
st.markdown(f"""
<style>
    /* 메인 너비 고정 */
    .main .block-container {{ max-width: 500px !important; padding: 10px 5px !important; }}

    /* [핵심] 가로 세로 모드 모두에서 5개 버튼을 한 줄로 고정 */
    [data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important; 
        gap: 4px !important; /* 버튼 사이 간격 */
    }}

    /* 컬럼 너비 균등 배분 */
    [data-testid="column"] {{
        flex: 1 !important;
        min-width: 0 !important;
    }}

    /* 버튼 기본 스타일 및 마우스 오버(Hover) 효과 */
    div.stButton > button {{
        width: 100% !important;
        height: 45px !important;
        font-size: 13px !important;
        font-weight: bold !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        transition: all 0.2s ease-in-out;
    }}

    /* 마우스 오버 시: 선명해지고 살짝 커짐 */
    div.stButton > button:hover {{
        opacity: 1.0 !important;
        transform: scale(1.05);
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    }}

    /* 버튼별 배경색 및 활성 상태 투명도 */
    div[data-testid="column"]:nth-of-type(1) button {{ background-color: {color_theme["조식"]} !important; opacity: {1.0 if current == "조식" else 0.4}; }}
    div[data-testid="column"]:nth-of-type(2) button {{ background-color: {color_theme["간편식"]} !important; opacity: {1.0 if current == "간편식" else 0.4}; }}
    div[data-testid="column"]:nth-of-type(3) button {{ background-color: {color_theme["중식"]} !important; opacity: {1.0 if current == "중식" else 0.4}; }}
    div[data-testid="column"]:nth-of-type(4) button {{ background-color: {color_theme["석식"]} !important; opacity: {1.0 if current == "석식" else 0.4}; }}
    div[data-testid="column"]:nth-of-type(5) button {{ background-color: {color_theme["야식"]} !important; opacity: {1.0 if current == "야식" else 0.4}; }}

    /* 식단 표시 카드 */
    .meal-card {{
        border: 2px solid {color_theme[current]};
        border-radius: 15px; padding: 30px 10px; text-align: center;
        background-color: white; margin-bottom: 15px;
    }}
</style>
""", unsafe_allow_html=True)

# 3. 화면 표시
st.markdown(f'<div class="meal-card"><h1 style="color: {color_theme[current]}; margin: 0;">{current}</h1></div>', unsafe_allow_html=True)

# 4. 버튼 레이아웃 (5컬럼)
cols = st.columns(5)
meals = list(color_theme.keys())

for i, m in enumerate(meals):
    if cols[i].button(m, key=f"btn_{m}"):
        st.session_state.active_meal = m
        st.rerun()
