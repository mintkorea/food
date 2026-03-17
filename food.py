import streamlit as st

# 1. 테마 색상 설정
menu_config = {
    "조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"
}

if 'active_meal' not in st.session_state:
    st.session_state.active_meal = "중식"

current = st.session_state.active_meal
current_color = menu_config[current]

# 2. 핵심 CSS: 세로 정렬 방지 및 이미지 디자인 구현
st.markdown(f"""
<style>
    /* 전체 너비 최적화 */
    .main .block-container {{ max-width: 500px !important; padding: 10px !important; }}

    /* 라디오 그룹 전체를 가로로 강제 고정 */
    div[data-testid="stRadio"] > div {{
        display: flex !important;
        flex-direction: row !important;
        justify-content: space-around !important;
        align-items: flex-end !important;
        gap: 0px !important;
        width: 100% !important;
    }}

    /* 각 항목(버튼 + 원형)을 감싸는 영역 */
    div[data-testid="stRadio"] label {{
        display: flex !important;
        flex-direction: column !important; /* 위: 글자(메뉴바), 아래: 원형 */
        align-items: center !important;
        justify-content: center !important;
        flex: 1 !important;
        margin: 0 !important;
        padding: 5px 0 !important;
    }}

    /* 윗부분: 메뉴바(텍스트) 스타일 */
    div[data-testid="stRadio"] label div[data-testid="stMarkdownContainer"] p {{
        width: 100% !important;
        text-align: center !important;
        padding: 10px 0 !important;
        border-radius: 8px 8px 0 0 !important;
        font-weight: bold !important;
        font-size: 14px !important;
        background-color: #f0f2f6 !important; /* 기본 배경색 */
        margin-bottom: 8px !important;
    }}

    /* 선택된 항목의 상단 메뉴바 색상 변경 (마우스 온 효과 대체) */
    div[data-testid="stRadio"] label[data-baseweb="radio"] div[data-testid="stMarkdownContainer"] p {{
        background-color: {current_color} !important;
        color: white !important;
    }}

    /* 아랫부분: 라디오 버튼 원형 크기 및 간격 조절 */
    div[data-testid="stRadio"] label div:first-child {{
        margin: 0 !important;
    }}
    
    /* 선택된 라디오 원형 색상 강조 */
    div[data-testid="stRadio"] div[role="radiogroup"] input[checked] + div {{
        background-color: {current_color} !important;
        border-color: {current_color} !important;
    }}

    /* 상단 큰 카드 스타일 */
    .display-card {{
        border: 2px solid {current_color};
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        background-color: white;
        margin-bottom: 20px;
    }}
</style>
""", unsafe_allow_html=True)

# 3. 상단 결과 표시
st.markdown(f"""
    <div class="display-card">
        <h1 style="color: {current_color}; margin: 0;">{current}</h1>
        <p style="color: #888; margin-top: 5px;">원하시는 식단을 아래에서 선택하세요</p>
    </div>
""", unsafe_allow_html=True)

# 4. 통합 라디오 버튼 (상단 바 + 하단 점)
# 레이블을 'collapsed'로 설정하여 불필요한 제목을 지웁니다.
selected = st.radio(
    "meal_selector",
    options=list(menu_config.keys()),
    index=list(menu_config.keys()).index(current),
    horizontal=True,
    label_visibility="collapsed"
)

# 선택 값이 바뀌면 즉시 업데이트
if selected != st.session_state.active_meal:
    st.session_state.active_meal = selected
    st.rerun()
