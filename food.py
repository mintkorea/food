import streamlit as st

# 1. 테마 설정
menu_cfg = {
    "조": "#E95444", "간": "#F1A33B", "중": "#8BC34A", "석": "#4A90E2", "야": "#673AB7"
}

if 'active_meal' not in st.session_state:
    st.session_state.active_meal = "중"

current = st.session_state.active_meal
current_color = menu_cfg[current]

# 2. CSS: 순서 변경 및 폰트 크기 조절
st.markdown(f"""
<style>
    .main .block-container {{ max-width: 500px !important; padding: 10px !important; }}

    /* [상단 라디오 영역] 가로 한 줄 고정 */
    [data-testid="stRadio"] > div {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        justify-content: space-between !important;
        gap: 5px !important;
        margin-bottom: -5px !important; /* 아래 카드와 밀착 */
        z-index: 1;
    }}

    /* 라디오 버튼 각각의 항목 */
    [data-testid="stRadio"] label {{
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        flex: 1 !important;
        cursor: pointer;
    }}

    /* [폰트 조절] 라디오 버튼 글자 크기 확대 및 스타일 */
    [data-testid="stRadio"] label div[data-testid="stMarkdownContainer"] p {{
        font-size: 18px !important; /* 폰트 크기 키움 */
        font-weight: 800 !important;
        padding: 10px 0 !important;
        width: 100% !important;
        text-align: center !important;
        border-radius: 12px 12px 0 0 !important; /* 윗부분만 둥글게 */
        background-color: #eee !important;
        color: #999 !important;
        transition: 0.3s;
    }}

    /* 선택된 메뉴의 폰트 색상 및 배경 강조 */
    [data-testid="stRadio"] label[data-baseweb="radio"] div[data-testid="stMarkdownContainer"] p {{
        background-color: {current_color} !important;
        color: white !important;
        font-size: 20px !important; /* 선택 시 더 크게 */
    }}

    /* [하단 카드 영역] 선택된 메뉴와 색상 일치 */
    .meal-index-card {{
        border: 4px solid {current_color};
        border-radius: 0 0 20px 20px; /* 아래부분만 둥글게 */
        padding: 40px 20px;
        text-align: center;
        background-color: white;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
    }}

    /* 라디오 원형 버튼 색상 조절 */
    div[data-testid="stRadio"] div[role="radiogroup"] input[checked] + div {{
        background-color: {current_color} !important;
        border-color: {current_color} !important;
    }}
</style>
""", unsafe_allow_html=True)

# 3. [상단] 라디오 버튼 조작부
# 메뉴명을 '조, 간, 중, 석, 야'로 짧게 유지하여 폰트를 키워도 안 깨지게 함
selected = st.radio(
    "nav",
    options=list(menu_cfg.keys()),
    index=list(menu_cfg.keys()).index(current),
    horizontal=True,
    label_visibility="collapsed"
)

# 4. [하단] 인덱스 일체형 카드 디자인
full_names = {"조": "조식", "간": "간편식", "중": "중식", "석": "석식", "야": "야식"}
st.markdown(f"""
    <div class="meal-index-card">
        <h3 style="color: {current_color}; margin: 0; font-size: 18px; opacity: 0.7;">{full_names[current]}</h3>
        <h1 style="color: {current_color}; margin: 5px 0; font-size: 42px;">MENU</h1>
    </div>
""", unsafe_allow_html=True)

# 변경 시 리런
if selected != st.session_state.active_meal:
    st.session_state.active_meal = selected
    st.rerun()
