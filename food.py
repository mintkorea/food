import streamlit as st

# 1. 데이터 및 테마 설정
color_theme = {
    "조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"
}

if 'active_meal' not in st.session_state:
    st.session_state.active_meal = "중식"

current = st.session_state.active_meal

# 2. CSS: 라디오 버튼을 가로 탭 메뉴로 변신시키기
st.markdown(f"""
<style>
    /* 메인 너비 고정 */
    .main .block-container {{ max-width: 450px !important; padding: 10px !important; }}

    /* 1. 라디오 버튼 컨테이너를 가로 flexbox로 변경 */
    div[data-testid="stRadio"] > div {{
        flex-direction: row !important;
        justify-content: space-between !important;
        gap: 5px !important;
    }}

    /* 2. 라디오 버튼의 동그라미 숨기기 */
    div[data-testid="stRadio"] label div[data-testid="stMarkdownContainer"] p {{
        font-size: 14px !important;
        font-weight: bold !important;
    }}
    
    div[data-testid="stRadio"] label {{
        flex: 1;
        background-color: #eee; /* 기본 배경 */
        padding: 10px 0 !important;
        border-radius: 10px !important;
        justify-content: center !important;
        transition: 0.3s;
        border: none !important;
    }}

    /* 3. 선택된 항목 커스텀 (현재 선택된 식단 강조) */
    div[data-testid="stRadio"] label[data-baseweb="radio"] {{
        background-color: {color_theme[current]} !important;
        color: white !important;
    }}
    
    /* 4. 불필요한 위젯 라벨 숨기기 */
    div[data-testid="stRadio"] > label {{ display: none !important; }}

    /* 식단 카드 */
    .meal-card {{
        border: 2px solid {color_theme[current]};
        border-radius: 20px; padding: 30px 15px; text-align: center;
        margin-bottom: 20px;
    }}
</style>
""", unsafe_allow_html=True)

# 3. UI 출력
st.title("🍴 오늘의 식사")

st.markdown(f"""
    <div class="meal-card">
        <h2 style="color: {color_theme[current]};">{current}</h2>
        <p style="font-size: 20px; font-weight: bold; margin-top: 15px;">🍲 즉시 확인하는 식단</p>
    </div>
""", unsafe_allow_html=True)

# 4. 가로 탭 메뉴 (실제로는 라디오 버튼)
# 선택 즉시 페이지가 새로고침 없이(Fragment 처럼) 반응합니다.
selected = st.radio(
    "식단선택",
    options=list(color_theme.keys()),
    index=list(color_theme.keys()).index(current),
    horizontal=True,
    label_visibility="collapsed"
)

# 선택이 바뀌면 세션 상태 업데이트
if selected != st.session_state.active_meal:
    st.session_state.active_meal = selected
    st.rerun()
