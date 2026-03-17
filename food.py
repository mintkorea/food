import streamlit as st

# 1. 테마 설정
color_theme = {
    "조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"
}

if 'active_meal' not in st.session_state:
    st.session_state.active_meal = "중식"

current = st.session_state.active_meal

# 2. 강력한 CSS: 라디오 버튼을 가로 탭 버튼으로 변신
st.markdown(f"""
<style>
    /* 전체 너비 최적화 */
    .main .block-container {{ max-width: 500px !important; padding: 10px !important; }}

    /* 라디오 버튼 컨테이너를 가로로 강제 정렬하고 간격을 0으로 */
    div[data-testid="stRadio"] > div {{
        display: flex !important;
        flex-direction: row !important;
        justify-content: space-between !important;
        gap: 2px !important; /* 버튼 사이 아주 미세한 간격 */
    }}

    /* 라디오 버튼 각각을 균등한 너비의 버튼 모양으로 변경 */
    div[data-testid="stRadio"] label {{
        flex: 1 !important;
        background-color: #f0f2f6 !important; /* 기본 배경색 */
        border-radius: 8px !important;
        padding: 15px 0 !important;
        justify-content: center !important;
        border: none !important;
        margin: 0 !important;
        transition: 0.2s;
    }}

    /* 선택된 버튼에 테마 색상 입히기 */
    div[data-testid="stRadio"] label[data-baseweb="radio"] {{
        background-color: {color_theme[current]} !important;
        color: white !important;
        font-weight: bold !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
    }}

    /* 라디오 원형 버튼 숨기기 */
    div[data-testid="stRadio"] label div:first-child {{ display: none !important; }}
    
    /* 기존 라디오 레이블 문구 숨기기 */
    div[data-testid="stRadio"] > label {{ display: none !important; }}

    .meal-card {{
        border: 2px solid {color_theme[current]};
        border-radius: 20px; padding: 30px 10px; text-align: center;
        background-color: white; margin-bottom: 20px;
    }}
</style>
""", unsafe_allow_html=True)

# 3. 상단 결과 카드
st.markdown(f"""
    <div class="meal-card">
        <h2 style="color: {color_theme[current]}; margin: 0;">{current}</h2>
        <p style="color: #666; margin-top: 5px;">선택한 식단의 메뉴를 확인하세요</p>
    </div>
""", unsafe_allow_html=True)

# 4. 가로 통합 라디오 버튼 (실제 조작부)
# 이 하나가 5개의 버튼 역할을 모두 수행하며 모바일에서도 벌어지지 않습니다.
selected = st.radio(
    "meal_selector",
    options=list(color_theme.keys()),
    index=list(color_theme.keys()).index(current),
    horizontal=True,
    label_visibility="collapsed"
)

# 상태 업데이트 및 리런
if selected != st.session_state.active_meal:
    st.session_state.active_meal = selected
    st.rerun()
