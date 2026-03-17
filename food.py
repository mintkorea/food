import streamlit as st

# 1. 설정 및 상태
color_theme = {
    "조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"
}

if 'active_meal' not in st.session_state:
    st.session_state.active_meal = "중식"

current = st.session_state.active_meal

# 2. CSS: 호버(Hover) 효과 추가
st.markdown(f"""
<style>
    .main .block-container {{ max-width: 500px !important; padding: 10px 5px !important; }}

    [data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important; 
        gap: 2px !important; 
    }}

    [data-testid="column"] {{
        flex: 1 !important;
        min-width: 0 !important;
        padding: 0 !important;
    }}

    /* 버튼 기본 스타일 및 호버 효과 */
    div.stButton > button {{
        width: 100% !important;
        height: 44px !important;
        font-size: 13px !important;
        font-weight: 800 !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        transition: all 0.3s ease; /* 부드러운 전환 효과 */
    }}

    /* 마우스를 올렸을 때(Hover) 효과 */
    div.stButton > button:hover {{
        opacity: 1.0 !important; /* 마우스 올리면 선명하게 */
        transform: translateY(-2px); /* 살짝 위로 올라가는 효과 */
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }}

    /* 각 버튼 고유 색상 및 활성화 상태 */
    div[data-testid="column"]:nth-of-type(1) button {{ background-color: {color_theme["조식"]} !important; opacity: {1.0 if current == "조식" else 0.4}; }}
    div[data-testid="column"]:nth-of-type(2) button {{ background-color: {color_theme["간편식"]} !important; opacity: {1.0 if current == "간편식" else 0.4}; }}
    div[data-testid="column"]:nth-of-type(3) button {{ background-color: {color_theme["중식"]} !important; opacity: {1.0 if current == "중식" else 0.4}; }}
    div[data-testid="column"]:nth-of-type(4) button {{ background-color: {color_theme["석식"]} !important; opacity: {1.0 if current == "석식" else 0.4}; }}
    div[data-testid="column"]:nth-of-type(5) button {{ background-color: {color_theme["야식"]} !important; opacity: {1.0 if current == "야식" else 0.4}; }}

    .meal-card {{
        border: 2px solid {color_theme[current]};
        border-radius: 15px; padding: 25px; text-align: center;
        margin-bottom: 15px; background-color: white;
    }}
</style>
""", unsafe_allow_html=True)

# 3. 메인 화면
st.markdown(f'<div class="meal-card"><h2 style="color: {color_theme[current]}; margin: 0;">{current}</h2></div>', unsafe_allow_html=True)

# 4. 버튼 배치
cols = st.columns(5)
meals = list(color_theme.keys())

for i, meal_name in enumerate(meals):
    if cols[i].button(meal_name, key=f"hover_btn_{meal_name}"):
        st.session_state.active_meal = meal_name
        st.rerun()
