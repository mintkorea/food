import streamlit as st

# 1. 데이터 및 테마 설정
color_theme = {
    "조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"
}

if 'active_meal' not in st.session_state:
    st.session_state.active_meal = "중식"

current = st.session_state.active_meal

# 2. CSS: 개별 버튼 색상 강제 지정 및 선택 효과
# nth-of-type을 사용하여 각 버튼에 순서대로 색상을 부여합니다.
color_styles = ""
for i, (meal, color) in enumerate(color_theme.items(), 1):
    is_active = (meal == current)
    color_styles += f"""
        div[data-testid="stRadio"] label:nth-of-type({i}) {{
            background-color: {color} !important;
            opacity: {1.0 if is_active else 0.3} !important;
            color: white !important;
            flex: 1;
            padding: 10px 0 !important;
            border-radius: 10px !important;
            justify-content: center !important;
            border: {"2px solid white" if is_active else "none"} !important;
            transition: 0.2s;
        }}
    """

st.markdown(f"""
<style>
    .main .block-container {{ max-width: 450px !important; padding: 10px !important; }}

    /* 라디오 버튼 가로 배치 고정 */
    div[data-testid="stRadio"] > div {{
        flex-direction: row !important;
        justify-content: space-between !important;
        gap: 4px !important;
    }}

    /* 라디오 버튼 원형 아이콘 숨기기 */
    div[data-testid="stRadio"] div[data-testid="stMarkdownContainer"] p {{
        font-size: 13px !important;
        font-weight: bold !important;
    }}
    div[data-testid="stRadio"] div[role="radiogroup"] {{
        gap: 4px !important;
    }}
    div[data-testid="stRadio"] label div:first-child {{
        display: none !important; /* 동그라미 제거 */
    }}

    /* 개별 색상 적용 */
    {color_styles}

    /* 위젯 라벨 숨기기 */
    div[data-testid="stRadio"] > label {{ display: none !important; }}

    .meal-card {{
        border: 2px solid {color_theme[current]};
        border-radius: 20px; padding: 30px 15px; text-align: center;
        margin-bottom: 25px;
        background-color: #ffffff;
    }}
</style>
""", unsafe_allow_html=True)

# 3. UI 출력
st.title("🍴 오늘의 식단")

st.markdown(f"""
    <div class="meal-card">
        <h2 style="color: {color_theme[current]};">{current}</h2>
        <p style="font-size: 22px; font-weight: bold; margin-top: 15px;">🍲 확인 중인 식단</p>
    </div>
""", unsafe_allow_html=True)

# 4. 가로 탭 메뉴 (라디오 버튼 개조)
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
