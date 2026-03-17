import streamlit as st

# 1. 테마 및 상태 설정
color_theme = {
    "조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"
}
if 'active_meal' not in st.session_state:
    st.session_state.active_meal = "중식"

current = st.session_state.active_meal

# 2. CSS: 화면 모드에 상관없이 강제로 버튼을 촘촘하게 배치
st.markdown(f"""
<style>
    /* 메인 컨테이너 패딩 최소화 */
    .main .block-container {{ 
        max-width: 500px !important; 
        padding: 10px 5px !important; 
    }}

    /* [핵심] 컬럼 컨테이너의 간격(gap)을 아예 제거 */
    [data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important; 
        gap: 0px !important; 
    }}

    /* 각 컬럼의 너비를 동일하게 고정하고 여백 제거 */
    [data-testid="column"] {{
        flex: 1 !important;
        width: 20% !important;
        min-width: 0 !important;
        padding: 0 1px !important; /* 여기서 버튼 사이의 실제 간격 조절 */
    }}

    /* 버튼 스타일: 텍스트가 잘리지 않도록 최적화 */
    div.stButton > button {{
        width: 100% !important;
        height: 44px !important;
        padding: 0 !important;
        font-size: 13px !important;
        font-weight: 800 !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
    }}

    /* 버튼별 색상 (순서 고정) */
    div[data-testid="column"]:nth-of-type(1) button {{ background-color: {color_theme["조식"]} !important; opacity: {1.0 if current == "조식" else 0.4}; }}
    div[data-testid="column"]:nth-of-type(2) button {{ background-color: {color_theme["간편식"]} !important; opacity: {1.0 if current == "간편식" else 0.4}; }}
    div[data-testid="column"]:nth-of-type(3) button {{ background-color: {color_theme["중식"]} !important; opacity: {1.0 if current == "중식" else 0.4}; }}
    div[data-testid="column"]:nth-of-type(4) button {{ background-color: {color_theme["석식"]} !important; opacity: {1.0 if current == "석식" else 0.4}; }}
    div[data-testid="column"]:nth-of-type(5) button {{ background-color: {color_theme["야식"]} !important; opacity: {1.0 if current == "야식" else 0.4}; }}

    .meal-display-box {{
        border: 2px solid {color_theme[current]};
        border-radius: 15px; padding: 20px; text-align: center;
        margin-bottom: 15px; background-color: #fff;
    }}
</style>
""", unsafe_allow_html=True)

# 3. 상단 UI
st.markdown(f"""
    <div class="meal-display-box">
        <h2 style="color: {color_theme[current]}; margin: 0; font-size: 24px;">{current}</h2>
    </div>
""", unsafe_allow_html=True)

# 4. 5개 컬럼 (가로 고정)
cols = st.columns(5)
meals = list(color_theme.keys())

for i, meal_name in enumerate(meals):
    if cols[i].button(meal_name, key=f"fixed_btn_{meal_name}"):
        st.session_state.active_meal = meal_name
        st.rerun()
