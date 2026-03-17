import streamlit as st

# 1. 데이터 및 테마 설정
color_theme = {
    "조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"
}

if 'active_meal' not in st.session_state:
    st.session_state.active_meal = "중식"

current = st.session_state.active_meal

# 2. CSS: 모바일 호환성 강화 및 개별 색상 강제 주입
# 각 버튼의 배경색을 '순서'가 아닌 '상태'와 '구조'에 맞춰 재정의합니다.
color_styles = ""
for i, (meal, color) in enumerate(color_theme.items(), 1):
    is_active = (meal == current)
    color_styles += f"""
        /* 모든 기기에서 개별 라벨 색상 강제 적용 */
        div[data-testid="stRadio"] div[role="radiogroup"] > label:nth-child({i}) {{
            background-color: {color} !important;
            opacity: {1.0 if is_active else 0.3} !important;
            flex: 1 !important;
            min-width: 0 !important; /* 모바일 좁은 화면 대응 */
            padding: 10px 2px !important;
            margin: 0 2px !important;
            border-radius: 8px !important;
            cursor: pointer !important;
            border: {"2px solid #fff" if is_active else "none"} !important;
            box-shadow: {"0px 2px 5px rgba(0,0,0,0.2)" if is_active else "none"} !important;
        }}
    """

st.markdown(f"""
<style>
    .main .block-container {{ max-width: 450px !important; padding: 10px !important; }}

    /* 라디오 그룹 가로 고정 및 여백 제거 */
    div[data-testid="stRadio"] > div[role="radiogroup"] {{
        display: flex !important;
        flex-direction: row !important;
        justify-content: space-between !important;
        width: 100% !important;
        gap: 0px !important;
    }}

    /* 텍스트 스타일 및 라디오 원형 숨기기 */
    div[data-testid="stRadio"] label p {{
        color: white !important;
        font-size: 13px !important;
        font-weight: bold !important;
        text-align: center !important;
        width: 100% !important;
    }}
    
    div[data-testid="stRadio"] label div:first-child {{
        display: none !important; /* 라디오 동그라미 제거 */
    }}

    /* 위젯 제목 제거 */
    div[data-testid="stRadio"] > label {{ display: none !important; }}

    {color_styles}

    .meal-card {{
        border: 2px solid {color_theme[current]};
        border-radius: 20px; padding: 35px 15px; text-align: center;
        background-color: white; margin-bottom: 20px;
    }}
</style>
""", unsafe_allow_html=True)

# 3. UI 구성
st.title("🍴 오늘의 식단")

st.markdown(f"""
    <div class="meal-card">
        <h2 style="color: {color_theme[current]}; margin-bottom: 10px;">{current}</h2>
        <p style="font-size: 18px; font-weight: 500; color: #444;">🍱 맛있는 식사 시간이 되세요!</p>
    </div>
""", unsafe_allow_html=True)

# 4. 가로 탭 (Radio 위젯 개조)
selected = st.radio(
    "meal_selector",
    options=list(color_theme.keys()),
    index=list(color_theme.keys()).index(current),
    horizontal=True,
    label_visibility="collapsed"
)

if selected != st.session_state.active_meal:
    st.session_state.active_meal = selected
    st.rerun()
