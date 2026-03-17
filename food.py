import streamlit as st

# 1. 테마 설정
color_theme = {
    "조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"
}

if 'active_meal' not in st.session_state:
    st.session_state.active_meal = "중식"

current = st.session_state.active_meal

# 2. 강력한 CSS 고정 (모바일/PC 공통)
st.markdown(f"""
<style>
    /* 전체 화면 중앙 정렬 및 너비 제한 */
    .main .block-container {{ max-width: 500px !important; padding: 20px 10px !important; }}

    /* [중요] 버튼들을 무조건 한 줄로 배치 */
    [data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important; 
        gap: 5px !important; /* 버튼 사이 미세 간격 */
    }}

    /* 각 컬럼의 너비를 동일하게 20%로 고정 */
    [data-testid="column"] {{
        flex: 1 !important;
        width: 20% !important;
        min-width: 0 !important;
    }}

    /* 버튼 기본 스타일: 둥근 모서리와 애니메이션 */
    div.stButton > button {{
        width: 100% !important;
        height: 48px !important;
        font-size: 14px !important;
        font-weight: 800 !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        transition: all 0.2s ease; /* 부드러운 변화 */
    }}

    /* 마우스 오버(Hover) 효과: 선명해지고 위로 살짝 들림 */
    div.stButton > button:hover {{
        opacity: 1.0 !important;
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }}

    /* 활성화 상태에 따른 불투명도 조절 */
    div[data-testid="column"]:nth-of-type(1) button {{ background-color: {color_theme["조식"]} !important; opacity: {1.0 if current == "조식" else 0.4}; }}
    div[data-testid="column"]:nth-of-type(2) button {{ background-color: {color_theme["간편식"]} !important; opacity: {1.0 if current == "간편식" else 0.4}; }}
    div[data-testid="column"]:nth-of-type(3) button {{ background-color: {color_theme["중식"]} !important; opacity: {1.0 if current == "중식" else 0.4}; }}
    div[data-testid="column"]:nth-of-type(4) button {{ background-color: {color_theme["석식"]} !important; opacity: {1.0 if current == "석식" else 0.4}; }}
    div[data-testid="column"]:nth-of-type(5) button {{ background-color: {color_theme["야식"]} !important; opacity: {1.0 if current == "야식" else 0.4}; }}

    /* 메인 식단 카드 디자인 */
    .meal-display {{
        border: 3px solid {color_theme[current]};
        border-radius: 20px;
        padding: 40px 20px;
        text-align: center;
        background-color: white;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }}
</style>
""", unsafe_allow_html=True)

# 3. 상단 식단 표시 영역
st.markdown(f"""
    <div class="meal-display">
        <h3 style="color: #888; margin: 0; font-size: 16px;">오늘의 메뉴</h3>
        <h1 style="color: {color_theme[current]}; margin: 10px 0; font-size: 36px;">{current}</h1>
        <p style="color: #444; margin: 0;">원하시는 식단을 아래에서 탭하세요</p>
    </div>
""", unsafe_allow_html=True)

# 4. 버튼 영역 (무조건 5컬럼)
cols = st.columns(5)
meals = list(color_theme.keys())

for i, m in enumerate(meals):
    if cols[i].button(m, key=f"v5_btn_{m}"):
        st.session_state.active_meal = m
        st.rerun()
