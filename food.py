import streamlit as st

# 1. 색상 및 초기화
menu_cfg = {
    "조": "#E95444", "간": "#F1A33B", "중": "#8BC34A", "석": "#4A90E2", "야": "#673AB7"
}

if 'active_meal' not in st.session_state:
    st.session_state.active_meal = "중"

current = st.session_state.active_meal
current_color = menu_cfg[current]

# 2. 강력한 가로 고정 CSS
st.markdown(f"""
<style>
    /* 화면 너비에 상관없이 수직 쌓기 방지 */
    [data-testid="stRadio"] > div {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important; 
        justify-content: space-between !important;
        gap: 4px !important;
        width: 100% !important;
    }}

    /* 각 항목(상단바 + 하단점) 정렬 */
    [data-testid="stRadio"] label {{
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        flex: 1 !important;
        min-width: 0 !important;
        margin: 0 !important;
        padding: 5px 0 !important;
    }}

    /* [상단 메뉴바] 텍스트 박스 스타일 */
    [data-testid="stRadio"] label div[data-testid="stMarkdownContainer"] p {{
        width: 100% !important;
        text-align: center !important;
        padding: 12px 0 !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        font-size: 15px !important;
        background-color: #f0f2f6 !important; /* 기본 회색 */
        color: #333 !important;
        margin-bottom: 10px !important;
        transition: 0.3s;
    }}

    /* [마우스 온/선택 효과] 선택된 메뉴의 상단바 배경색 변경 */
    [data-testid="stRadio"] label[data-baseweb="radio"] div[data-testid="stMarkdownContainer"] p {{
        background-color: {current_color} !important;
        color: white !important;
    }}

    /* [하단 라디오 점] 선택된 색상 강조 */
    div[data-testid="stRadio"] div[role="radiogroup"] input[checked] + div {{
        background-color: {current_color} !important;
        border-color: {current_color} !important;
    }}

    /* 상단 알림 카드 */
    .meal-card {{
        border: 2px solid {current_color};
        border-radius: 15px; padding: 25px; text-align: center;
        margin-bottom: 20px; background-color: white;
    }}
</style>
""", unsafe_allow_html=True)

# 3. 메인 디스플레이
st.markdown(f"""
    <div class="meal-card">
        <h1 style="color: {current_color}; margin: 0;">{current}식 메뉴</h1>
    </div>
""", unsafe_allow_html=True)

# 4. 일체형 라디오 버튼
# 글자를 '조, 간, 중, 석, 야'로 짧게 구성하여 공간 확보
selected = st.radio(
    "meal_nav",
    options=list(menu_cfg.keys()),
    index=list(menu_cfg.keys()).index(current),
    horizontal=True,
    label_visibility="collapsed"
)

# 변경 감지 및 새로고침
if selected != st.session_state.active_meal:
    st.session_state.active_meal = selected
    st.rerun()
