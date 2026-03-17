import streamlit as st

# 1. 색상 및 데이터 설정
meal_options = {"조": "#E95444", "간": "#F1A33B", "중": "#8BC34A", "석": "#4A90E2", "야": "#673AB7"}
meal_full_names = {"조": "조식", "간": "간편식", "중": "중식", "석": "석식", "야": "야식"}

if 'selected_meal' not in st.session_state:
    st.session_state.selected_meal = "중"

# 2. CSS: 라디오 버튼을 가로로 강제 정렬하고 간격을 좁힘
st.markdown(f"""
<style>
    /* 전체 컨테이너 너비 제한 및 중앙 정렬 */
    .main .block-container {{ max-width: 400px !important; padding: 10px !important; }}

    /* 라디오 버튼 그룹 가로 배치 */
    div[data-testid="stRadio"] > div {{
        display: flex !important;
        flex-direction: row !important;
        justify-content: space-around !important; /* 동일 간격 배치 */
        background-color: #f8f9fa;
        padding: 10px 5px;
        border-radius: 15px;
    }}

    /* 각 라디오 항목 스타일 */
    div[data-testid="stRadio"] label {{
        font-size: 16px !important;
        font-weight: bold !important;
        color: #555 !important;
        margin: 0 !important;
        padding: 0 5px !important;
    }}

    /* 선택된 항목의 텍스트 강조 */
    div[data-testid="stRadio"] label[data-baseweb="radio"] {{
        color: {meal_options[st.session_state.selected_meal]} !important;
    }}

    /* 상단 식단 표시 카드 */
    .meal-box {{
        border: 3px solid {meal_options[st.session_state.selected_meal]};
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        margin-bottom: 15px;
    }}
</style>
""", unsafe_allow_html=True)

# 3. 상단 결과 표시
current_full = meal_full_names[st.session_state.selected_meal]
st.markdown(f"""
    <div class="meal-box">
        <h2 style="color: {meal_options[st.session_state.selected_meal]}; margin: 0;">{current_full}</h2>
    </div>
""", unsafe_allow_html=True)

# 4. 가로형 라디오 버튼 (조 간 중 석 야)
selected = st.radio(
    "식단 선택",
    options=list(meal_options.keys()),
    index=list(meal_options.keys()).index(st.session_state.selected_meal),
    horizontal=True,
    label_visibility="collapsed" # 레이블 숨김
)

# 선택 값이 바뀌면 세션 상태 업데이트 후 재실행
if selected != st.session_state.selected_meal:
    st.session_state.selected_meal = selected
    st.rerun()
