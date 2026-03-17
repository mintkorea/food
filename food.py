import streamlit as st

# 1. 테마 및 상태 설정
color_theme = {
    "조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"
}
if 'active_meal' not in st.session_state:
    st.session_state.active_meal = "중식"

current = st.session_state.active_meal

# 2. CSS: 모바일에서도 무조건 한 줄 유지 및 버튼 간격 고정
st.markdown(f"""
<style>
    /* 전체 컨테이너 패딩 조절 */
    .main .block-container {{ padding: 10px !important; }}

    /* [핵심] 9개 컬럼이 절대 아래로 떨어지지 않게 강제 고정 */
    [data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important; 
        gap: 0 !important; /* 컬럼 간 기본 간격 제거 (우리가 직접 조절) */
    }}

    /* 각 컬럼의 최소 너비 해제 */
    [data-testid="column"] {{
        min-width: 0 !important;
        flex: 1 !important;
    }}

    /* 버튼 스타일: 꽉 차게 만들고 테두리 제거 */
    div.stButton > button {{
        width: 100% !important;
        height: 42px !important;
        padding: 0 !important;
        font-size: 13px !important;
        font-weight: bold !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        transition: 0.2s;
    }}

    /* 메뉴별 버튼 색상 및 활성화 효과 */
    div[data-testid="column"]:nth-of-type(1) button {{ background-color: {color_theme["조식"]} !important; opacity: {1.0 if current == "조식" else 0.4}; }}
    div[data-testid="column"]:nth-of-type(3) button {{ background-color: {color_theme["간편식"]} !important; opacity: {1.0 if current == "간편식" else 0.4}; }}
    div[data-testid="column"]:nth-of-type(5) button {{ background-color: {color_theme["중식"]} !important; opacity: {1.0 if current == "중식" else 0.4}; }}
    div[data-testid="column"]:nth-of-type(7) button {{ background-color: {color_theme["석식"]} !important; opacity: {1.0 if current == "석식" else 0.4}; }}
    div[data-testid="column"]:nth-of-type(9) button {{ background-color: {color_theme["야식"]} !important; opacity: {1.0 if current == "야식" else 0.4}; }}

    .meal-display {{
        border: 2px solid {color_theme[current]};
        border-radius: 15px; padding: 20px; text-align: center;
        margin-bottom: 20px; background-color: #fff;
    }}
</style>
""", unsafe_allow_html=True)

# 3. 상단 결과 표시 영역
st.markdown(f"""
    <div class="meal-display">
        <h2 style="color: {color_theme[current]}; margin: 0;">{current}</h2>
        <p style="margin: 5px 0 0 0; color: #888; font-size: 14px;">식단을 확인하려면 버튼을 탭하세요</p>
    </div>
""", unsafe_allow_html=True)

# 4. 9개 컬럼 생성 (비율: 1은 버튼, 0.15는 가짜 공백)
# 1(버튼)-0.15(공백)-1(버튼)-0.15(공백)-1(버튼)-0.15(공백)-1(버튼)-0.15(공백)-1(버튼)
cols = st.columns([1, 0.15, 1, 0.15, 1, 0.15, 1, 0.15, 1])

meals = list(color_theme.keys())
meal_idx = 0

for i in range(9):
    if i % 2 == 0:  # 0, 2, 4, 6, 8번째 컬럼에만 실제 버튼 배치
        m_name = meals[meal_idx]
        if cols[i].button(m_name, key=f"btn_{m_name}"):
            st.session_state.active_meal = m_name
            st.rerun()
        meal_idx += 1
    else:
        # 1, 3, 5, 7번째 컬럼은 '가짜 버튼' 공간으로 비워둠
        cols[i].write("")
