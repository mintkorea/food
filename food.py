import streamlit as st

# 1. 테마 설정
color_theme = {
    "조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"
}

if 'active_meal' not in st.session_state:
    st.session_state.active_meal = "중식"

current = st.session_state.active_meal

# 2. 강력한 CSS: 공백 컬럼과 버튼 컬럼의 비율 고정
st.markdown(f"""
<style>
    .main .block-container {{ max-width: 500px !important; padding: 10px !important; }}

    /* [핵심] 9개의 컬럼이 모바일에서도 무조건 가로 한 줄을 유지하도록 강제 */
    [data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
    }}

    /* 버튼이 들어있는 컬럼과 공백 컬럼의 크기 조절 */
    [data-testid="column"] {{
        flex: 1 !important;
        min-width: 0 !important;
    }}

    /* 버튼 스타일 최적화 */
    div.stButton > button {{
        width: 100% !important;
        height: 45px !important;
        padding: 0 !important;
        font-size: 12px !important; /* 모바일 가독성 위해 약간 축소 */
        font-weight: bold !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
    }}

    /* 메뉴별 고유 색상 적용 */
    div[data-testid="column"]:nth-of-type(1) button {{ background-color: {color_theme["조식"]} !important; opacity: {1.0 if current == "조식" else 0.4}; }}
    div[data-testid="column"]:nth-of-type(3) button {{ background-color: {color_theme["간편식"]} !important; opacity: {1.0 if current == "간편식" else 0.4}; }}
    div[data-testid="column"]:nth-of-type(5) button {{ background-color: {color_theme["중식"]} !important; opacity: {1.0 if current == "중식" else 0.4}; }}
    div[data-testid="column"]:nth-of-type(7) button {{ background-color: {color_theme["석식"]} !important; opacity: {1.0 if current == "석식" else 0.4}; }}
    div[data-testid="column"]:nth-of-type(9) button {{ background-color: {color_theme["야식"]} !important; opacity: {1.0 if current == "야식" else 0.4}; }}

    .meal-card {{
        border: 2px solid {color_theme[current]};
        border-radius: 15px; padding: 25px 10px; text-align: center;
        margin-bottom: 20px;
    }}
</style>
""", unsafe_allow_html=True)

# 3. 상단 UI
st.title("🍴 오늘의 식단")
st.markdown(f'<div class="meal-card"><h2 style="color: {color_theme[current]}; margin: 0;">{current}</h2></div>', unsafe_allow_html=True)

# 4. 9컬럼 시스템 가동 (홀수: 버튼, 짝수: 공백)
cols = st.columns([1, 0.2, 1, 0.2, 1, 0.2, 1, 0.2, 1]) # 공백 컬럼은 0.2 비율로 좁게 설정

meals = list(color_theme.keys())
meal_index = 0

for i in range(9):
    if i % 2 == 0: # 홀수번째 컬럼 (0, 2, 4, 6, 8)에 버튼 배치
        meal_name = meals[meal_index]
        if cols[i].button(meal_name, key=f"btn_{meal_name}"):
            st.session_state.active_meal = meal_name
            st.rerun()
        meal_index += 1
    else:
        # 짝수번째 컬럼 (1, 3, 5, 7)은 빈 공간으로 둠
        cols[i].write("")
