import streamlit as st

# 1. 설정 및 상태
color_theme = {
    "조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"
}

if 'active_meal' not in st.session_state:
    st.session_state.active_meal = "중식"

current = st.session_state.active_meal

# 2. CSS: 사이 간격(Gutter) 0으로 고정
st.markdown(f"""
<style>
    /* 전체 너비 및 패딩 제거 */
    .main .block-container {{ max-width: 500px !important; padding: 10px 5px !important; }}

    /* 핵심: 컬럼 사이의 벌어지는 간격(gap)을 0으로 강제 조정 */
    [data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 0px !important; /* 간격을 완전히 없앰 */
    }}

    /* 각 컬럼의 패딩 제거 및 너비 고정 */
    [data-testid="column"] {{
        width: 20% !important;
        flex: 1 1 auto !important;
        min-width: 0 !important;
        padding: 0 2px !important; /* 아주 미세한 여백만 남김 */
    }}

    /* 버튼 높이 및 폰트 최적화 */
    div.stButton > button {{
        width: 100% !important;
        height: 48px !important;
        padding: 0 !important;
        font-size: 14px !important;
        font-weight: bold !important;
        color: white !important;
        border-radius: 6px !important;
        border: none !important;
    }}

    /* 버튼별 색상 (활성화/비활성화) */
    div[data-testid="column"]:nth-of-type(1) button {{ background-color: {color_theme["조식"]} !important; opacity: {1.0 if current == "조식" else 0.4}; }}
    div[data-testid="column"]:nth-of-type(2) button {{ background-color: {color_theme["간편식"]} !important; opacity: {1.0 if current == "간편식" else 0.4}; }}
    div[data-testid="column"]:nth-of-type(3) button {{ background-color: {color_theme["중식"]} !important; opacity: {1.0 if current == "중식" else 0.4}; }}
    div[data-testid="column"]:nth-of-type(4) button {{ background-color: {color_theme["석식"]} !important; opacity: {1.0 if current == "석식" else 0.4}; }}
    div[data-testid="column"]:nth-of-type(5) button {{ background-color: {color_theme["야식"]} !important; opacity: {1.0 if current == "야식" else 0.4}; }}

    .meal-card {{
        border: 2px solid {color_theme[current]};
        border-radius: 15px; padding: 25px 10px; text-align: center;
        background-color: white; margin-bottom: 15px;
    }}
</style>
""", unsafe_allow_html=True)

# 3. 상단 UI
st.markdown(f'<div class="meal-card"><h2 style="color: {color_theme[current]}; margin: 0;">{current}</h2></div>', unsafe_allow_html=True)

# 4. 가로 배치 버튼 (st.columns 간격 제거 버전)
cols = st.columns(5)
meals = list(color_theme.keys())

for i, meal in enumerate(meals):
    if cols[i].button(meal, key=f"fixed_gap_btn_{meal}"):
        st.session_state.active_meal = meal
        st.rerun()

