import streamlit as st

# 1. 상태 설정 및 색상 정의
color_theme = {
    "조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"
}

if 'active_meal' not in st.session_state:
    st.session_state.active_meal = "중식"

current = st.session_state.active_meal

# 2. 강력한 CSS: 라디오 버튼을 가로 탭 버튼으로 개조
st.markdown(f"""
<style>
    /* 메인 컨테이너 패딩 최적화 */
    .main .block-container {{ max-width: 500px !important; padding: 15px 5px !important; }}

    /* 라디오 버튼 그룹을 가로 한 줄로 고정 (절대 안깨짐) */
    div[data-testid="stRadio"] > div {{
        display: flex !important;
        flex-direction: row !important;
        justify-content: space-between !important;
        gap: 2px !important; /* 버튼 사이 촘촘한 간격 */
        width: 100% !important;
    }}

    /* 각 라디오 버튼 항목 스타일링 */
    div[data-testid="stRadio"] label {{
        flex: 1 !important;
        background-color: #f0f2f6 !important; 
        border-radius: 8px !important;
        padding: 12px 0 !important;
        justify-content: center !important;
        border: none !important;
        margin: 0 !important;
        cursor: pointer;
    }}

    /* 선택된 버튼에 테마 색상 강제 적용 */
    div[data-testid="stRadio"] label[data-baseweb="radio"] {{
        background-color: {color_theme[current]} !important;
        color: white !important;
        font-weight: bold !important;
    }}

    /* 라디오 버튼의 동그라미 아이콘 숨기기 */
    div[data-testid="stRadio"] label div:first-child {{ display: none !important; }}
    
    /* 불필요한 레이블 숨기기 */
    div[data-testid="stRadio"] > label {{ display: none !important; }}

    .meal-header {{
        border: 2px solid {color_theme[current]};
        border-radius: 15px; padding: 20px; text-align: center;
        background-color: white; margin-bottom: 10px;
    }}
</style>
""", unsafe_allow_html=True)

# 3. 상단 UI 카드
st.markdown(f"""
    <div class="meal-header">
        <h2 style="color: {color_theme[current]}; margin: 0;">{current}</h2>
    </div>
""", unsafe_allow_html=True)

# 4. 가로 통합 세그먼트 버튼 (st.radio 활용)
# 이 위젯 하나가 5개의 버튼 역할을 하며, CSS에 의해 가로로 꽉 차게 배치됩니다.
selected = st.radio(
    "meal_selector",
    options=list(color_theme.keys()),
    index=list(color_theme.keys()).index(current),
    horizontal=True,
    label_visibility="collapsed"
)

# 선택 변경 시 즉시 반영
if selected != st.session_state.active_meal:
    st.session_state.active_meal = selected
    st.rerun()
