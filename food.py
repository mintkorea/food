import streamlit as st

# 1. 테마 및 상태 설정
color_theme = {
    "조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"
}

if 'active_meal' not in st.session_state:
    st.session_state.active_meal = "중식"

current = st.session_state.active_meal

# 2. CSS: 모바일 세로 꺾임 방지 및 버튼 디자인
st.markdown(f"""
<style>
    /* 메인 컨테이너 너비 최적화 */
    .main .block-container {{ max-width: 500px !important; padding: 10px !important; }}

    /* 핵심: columns가 모바일에서 세로로 변하는 것을 강제로 막음 */
    [data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-direction: row !important; /* 무조건 가로로 */
        flex-wrap: nowrap !important; /* 줄바꿈 금지 */
        align-items: center !important;
        gap: 5px !important;
    }}

    /* 각 컬럼의 너비를 동일하게 20%씩 할당 */
    [data-testid="column"] {{
        width: 20% !important;
        flex: 1 1 auto !important;
        min-width: 0 !important;
    }}

    /* 버튼 스타일 최적화 */
    div.stButton > button {{
        width: 100% !important;
        height: 50px !important;
        padding: 0 !important;
        font-size: 13px !important; /* 모바일 대응 글자 크기 */
        font-weight: bold !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        transition: 0.2s;
    }}

    /* 버튼별 동적 색상 적용 (선택된 메뉴 강조) */
    div[data-testid="column"]:nth-of-type(1) button {{ background-color: {color_theme["조식"]} !important; opacity: {1.0 if current == "조식" else 0.4}; }}
    div[data-testid="column"]:nth-of-type(2) button {{ background-color: {color_theme["간편식"]} !important; opacity: {1.0 if current == "간편식" else 0.4}; }}
    div[data-testid="column"]:nth-of-type(3) button {{ background-color: {color_theme["중식"]} !important; opacity: {1.0 if current == "중식" else 0.4}; }}
    div[data-testid="column"]:nth-of-type(4) button {{ background-color: {color_theme["석식"]} !important; opacity: {1.0 if current == "석식" else 0.4}; }}
    div[data-testid="column"]:nth-of-type(5) button {{ background-color: {color_theme["야식"]} !important; opacity: {1.0 if current == "야식" else 0.4}; }}

    .meal-card {{
        border: 2px solid {color_theme[current]};
        border-radius: 20px; padding: 30px 10px; text-align: center;
        background-color: white; margin-bottom: 20px;
    }}
</style>
""", unsafe_allow_html=True)

# 3. 상단 식단 카드
st.markdown(f"""
    <div class="meal-card">
        <h2 style="color: {color_theme[current]}; margin: 0;">{current}</h2>
        <p style="font-size: 16px; color: #666; margin-top: 10px;">원하시는 식단을 선택하세요</p>
    </div>
""", unsafe_allow_html=True)

# 4. 가로 배치 버튼 (st.columns 이용)
cols = st.columns(5)
meals = list(color_theme.keys())

for i, meal in enumerate(meals):
    if cols[i].button(meal, key=f"fixed_btn_{meal}"):
        st.session_state.active_meal = meal
        st.rerun()
