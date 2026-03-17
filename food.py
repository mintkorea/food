import streamlit as st

# 1. 데이터 및 테마 설정
color_theme = {
    "조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"
}

if 'active_meal' not in st.session_state:
    st.session_state.active_meal = "중식"

current = st.session_state.active_meal

# 2. CSS: 상단 디자인 바 및 하단 라디오 스타일
st.markdown(f"""
<style>
    .main .block-container {{ max-width: 500px !important; padding: 10px !important; }}

    /* 상단 디자인 바 (보기용) */
    .design-nav-bar {{
        display: flex !important;
        flex-direction: row !important;
        width: 100% !important;
        gap: 4px;
        margin-bottom: 5px;
    }}
    .nav-item {{
        flex: 1; text-align: center; padding: 12px 0;
        font-size: 13px; font-weight: bold; border-radius: 8px 8px 0 0;
        color: white; transition: 0.3s;
    }}

    /* 하단 라디오 버튼 커스텀 (버튼처럼 보이게) */
    div[data-testid="stRadio"] > div {{
        flex-direction: row !important;
        gap: 4px !important;
    }}
    div[data-testid="stRadio"] label {{
        flex: 1;
        justify-content: center !important;
        background-color: #f0f2f6 !important; /* 기본 배경 */
        border-radius: 0 0 8px 8px !important; /* 위쪽은 평평하게 */
        padding: 10px 0 !important;
        border: none !important;
    }}
    /* 선택된 라디오 항목 강조 */
    div[data-testid="stRadio"] label[data-baseweb="radio"] {{
        background-color: {color_theme[current]} !important;
        color: white !important;
    }}
    /* 라디오 원형 버튼 숨기기 */
    div[data-testid="stRadio"] label div:first-child {{ display: none !important; }}
    div[data-testid="stRadio"] > label {{ display: none !important; }}

    .meal-card {{
        border: 2px solid {color_theme[current]};
        border-radius: 20px; padding: 30px; text-align: center;
        margin-bottom: 20px;
    }}
</style>
""", unsafe_allow_html=True)

# 3. 메인 카드 UI
st.title("🍴 식단 매니저")
st.markdown(f"""
    <div class="meal-card">
        <h2 style="color: {color_theme[current]};">{current}</h2>
        <p style="color: #666;">아래 버튼을 눌러 식단을 변경하세요.</p>
    </div>
""", unsafe_allow_html=True)

# 4. 상단 디자인 바 (HTML)
nav_html = '<div class="design-nav-bar">'
for meal, color in color_theme.items():
    opacity = "1.0" if meal == current else "0.3"
    nav_html += f'<div class="nav-item" style="background-color: {color}; opacity: {opacity};">{meal}</div>'
nav_html += '</div>'
st.markdown(nav_html, unsafe_allow_html=True)

# 5. 하단 실제 작동 라디오 버튼
# 디자인 바 바로 아래 붙어서 버튼처럼 작동합니다.
selected = st.radio(
    "식단선택",
    options=list(color_theme.keys()),
    index=list(color_theme.keys()).index(current),
    horizontal=True,
    label_visibility="collapsed"
)

if selected != st.session_state.active_meal:
    st.session_state.active_meal = selected
    st.rerun()
