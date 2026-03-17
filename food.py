import streamlit as st

# 1. 설정 및 테마
color_theme = {
    "조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"
}

if 'active_meal' not in st.session_state:
    st.session_state.active_meal = "중식"

current = st.session_state.active_meal

# 2. CSS: 상단 바와 라디오 버튼을 하나처럼 연결
st.markdown(f"""
<style>
    .main .block-container {{ max-width: 500px !important; padding: 10px !important; }}

    /* [레이어 1] 상단 컬러 바 디자인 */
    .nav-design-wrap {{
        display: flex !important;
        flex-direction: row !important;
        width: 100% !important;
        gap: 4px;
        margin-bottom: -5px; /* 라디오 버튼과 밀착 */
    }}
    .nav-tab {{
        flex: 1; text-align: center; padding: 12px 0;
        font-size: 13px; font-weight: bold; border-radius: 10px 10px 0 0;
        color: white; transition: 0.3s;
    }}

    /* [레이어 2] 하단 라디오 버튼 개조 */
    div[data-testid="stRadio"] > div {{
        flex-direction: row !important;
        gap: 4px !important;
    }}
    div[data-testid="stRadio"] label {{
        flex: 1;
        justify-content: center !important;
        background-color: #f0f2f6 !important;
        border-radius: 0 0 10px 10px !important;
        padding: 10px 0 !important;
        border: none !important;
        margin: 0 !important;
    }}
    /* 선택된 항목 강조: 상단 바와 같은 색으로 표시 */
    div[data-testid="stRadio"] label[data-baseweb="radio"] {{
        background-color: {color_theme[current]} !important;
        color: white !important;
        font-weight: bold !important;
    }}
    /* 라디오 원형 숨기기 */
    div[data-testid="stRadio"] label div:first-child {{ display: none !important; }}
    div[data-testid="stRadio"] > label {{ display: none !important; }}

    .meal-card {{
        border: 2px solid {color_theme[current]};
        border-radius: 20px; padding: 30px 15px; text-align: center;
        background-color: white; margin-bottom: 20px;
    }}
</style>
""", unsafe_allow_html=True)

# 3. 메인 식단 카드
st.title("🍴 오늘의 식단")
st.markdown(f"""
    <div class="meal-card">
        <h2 style="color: {color_theme[current]}; margin: 0;">{current}</h2>
        <p style="font-size: 15px; color: #666; margin-top: 10px;">아래 버튼을 눌러 메뉴를 확인하세요.</p>
    </div>
""", unsafe_allow_html=True)

# 4. 시각적 가로 바 (HTML)
nav_html = '<div class="nav-design-wrap">'
for meal, color in color_theme.items():
    opacity = "1.0" if meal == current else "0.3"
    nav_html += f'<div class="nav-tab" style="background-color: {color}; opacity: {opacity};">{meal}</div>'
nav_html += '</div>'
st.markdown(nav_html, unsafe_allow_html=True)

# 5. 실제 작동 라디오 버튼
selected = st.radio(
    "meal_select",
    options=list(color_theme.keys()),
    index=list(color_theme.keys()).index(current),
    horizontal=True,
    label_visibility="collapsed"
)

if selected != st.session_state.active_meal:
    st.session_state.active_meal = selected
    st.rerun()
