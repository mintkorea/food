import streamlit as st

# 1. 설정 및 상태 관리
menu_cfg = {
    "조": "#E95444", "간": "#F1A33B", "중": "#8BC34A", "석": "#4A90E2", "야": "#673AB7"
}

if 'active_meal' not in st.session_state:
    st.session_state.active_meal = "중"

current = st.session_state.active_meal
current_color = menu_cfg[current]

# 2. CSS: 라디오 버튼 폰트 조절 및 인덱스 디자인
st.markdown(f"""
<style>
    .main .block-container {{ max-width: 500px !important; padding: 10px !important; }}

    /* 라디오 버튼 그룹 설정 */
    [data-testid="stRadio"] > div {{
        display: flex !important;
        flex-direction: row !important;
        justify-content: space-between !important;
        padding: 0 5px !important;
        margin-bottom: -4px !important; /* 카드와 밀착 */
    }}

    /* 라디오 버튼 레이블(글자) 스타일 */
    [data-testid="stRadio"] label {{
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        cursor: pointer;
        flex: 1 !important;
    }}

    /* [폰트/간격] 배경색과 동일한 글자로 간격을 벌리는 효과 */
    [data-testid="stRadio"] label div[data-testid="stMarkdownContainer"] p {{
        font-size: 20px !important; /* 글자 크기 확대 */
        font-weight: 900 !important;
        width: 100% !important;
        text-align: center !important;
        padding: 12px 0 !important;
        border-radius: 12px 12px 0 0 !important;
        background-color: #f0f2f6 !important; /* 기본 배경색 */
        color: #f0f2f6 !important; /* 배경과 같은 색으로 글자를 숨겨 간격 확보 */
        transition: 0.3s;
        border: 1px solid transparent;
    }}

    /* 선택된 버튼: 글자가 보이고 배경색이 테마색으로 변경 */
    [data-testid="stRadio"] label[data-baseweb="radio"] div[data-testid="stMarkdownContainer"] p {{
        background-color: {current_color} !important;
        color: white !important; /* 선택될 때만 글자 노출 */
        box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
    }}

    /* 하단 인덱스 카드 디자인 */
    .index-card-body {{
        border: 4px solid {current_color};
        border-radius: 0 0 20px 20px;
        padding: 40px 20px;
        text-align: center;
        background-color: white;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }}

    /* 라디오 원형 버튼 색상 */
    div[data-testid="stRadio"] div[role="radiogroup"] input[checked] + div {{
        background-color: {current_color} !important;
        border-color: {current_color} !important;
    }}
</style>
""", unsafe_allow_html=True)

# 3. 상단 라디오 버튼 (간격 확보형)
# 실제 값은 보이지 않다가 선택 시에만 '조, 간, 중...'이 나타납니다.
selected = st.radio(
    "nav",
    options=list(menu_cfg.keys()),
    index=list(menu_cfg.keys()).index(current),
    horizontal=True,
    label_visibility="collapsed"
)

# 4. 하단 일체형 카드
full_names = {"조": "조식", "간": "간편식", "중": "중식", "석": "석식", "야": "야식"}
st.markdown(f"""
    <div class="index-card-body">
        <h2 style="color: {current_color}; margin: 0; font-size: 22px;">{full_names[current]}</h2>
        <h1 style="color: {current_color}; margin: 10px 0; font-size: 45px; font-weight: 900;">MENU</h1>
        <p style="color: #888;">맛있는 식사가 준비되어 있습니다.</p>
    </div>
""", unsafe_allow_html=True)

# 상태 업데이트
if selected != st.session_state.active_meal:
    st.session_state.active_meal = selected
    st.rerun()
