import streamlit as st

# 1. 색상 테마 정의
menu_info = {
    "조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"
}

# 세션 상태 초기화
if 'selected_meal' not in st.session_state:
    st.session_state.selected_meal = "중식"

current = st.session_state.selected_meal
selected_color = menu_info[current]

# 2. CSS: 라디오 버튼을 하단 인덱스 카드로 개조
st.markdown(f"""
<style>
    /* 메인 컨테이너 좁게 유지 */
    .main .block-container {{ max-width: 500px !important; padding: 10px !important; }}

    /* [상단 카드] 인덱스와 연결된 느낌의 디자인 */
    .display-card {{
        border: 3px solid {selected_color};
        border-bottom: none; /* 하단 버튼 영역과 연결 */
        border-radius: 20px 20px 0 0;
        padding: 40px 20px;
        text-align: center;
        background-color: white;
    }}

    /* [하단 라디오] 가로 배치 및 인덱스 탭 스타일 */
    div[data-testid="stRadio"] > div {{
        display: flex !important;
        flex-direction: row !important;
        justify-content: space-between !important;
        gap: 2px !important;
        background-color: #f0f2f6;
        padding: 5px;
        border-radius: 0 0 20px 20px;
        border: 3px solid {selected_color};
        border-top: 1px solid #eee;
    }}

    /* 라디오 각 항목을 탭 카드로 변경 */
    div[data-testid="stRadio"] label {{
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        flex: 1 !important;
        padding: 10px 0 !important;
        margin: 0 !important;
        transition: 0.3s;
    }}

    /* 메뉴명 텍스트 스타일 (인덱스 라벨) */
    div[data-testid="stRadio"] label div[data-testid="stMarkdownContainer"] p {{
        font-size: 13px !important;
        font-weight: bold !important;
        margin-bottom: 8px !important;
        color: #666;
    }}

    /* 선택된 항목의 배경색과 텍스트 강조 (첫 번째 이미지의 인덱스 느낌) */
    div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input[checked]) {{
        background-color: white !important; /* 선택된 탭은 밝게 */
        border-radius: 10px;
        box-shadow: 0 -4px 10px rgba(0,0,0,0.05);
    }}
    
    div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input[checked]) p {{
        color: {selected_color} !important;
        font-size: 15px !important;
    }}

    /* 라디오 버튼 원형(동그라미) 색상 커스텀 */
    div[data-testid="stRadio"] div[role="radiogroup"] input[checked] + div {{
        background-color: {selected_color} !important;
        border-color: {selected_color} !important;
    }}
</style>
""", unsafe_allow_html=True)

# 3. 상단 결과 표시 카드
st.markdown(f"""
    <div class="display-card">
        <span style="background-color: {selected_color}; color: white; padding: 5px 15px; border-radius: 50px; font-size: 14px; font-weight: bold;">Today's Menu</span>
        <h1 style="color: {selected_color}; margin: 15px 0 0 0; font-size: 40px;">{current}</h1>
    </div>
""", unsafe_allow_html=True)

# 4. 하단 통합형 인덱스 라디오 버튼
selected = st.radio(
    "meal_selector",
    options=list(menu_info.keys()),
    index=list(menu_info.keys()).index(current),
    horizontal=True,
    label_visibility="collapsed"
)

# 선택 변경 시 로직
if selected != st.session_state.selected_meal:
    st.session_state.selected_meal = selected
    st.rerun()
