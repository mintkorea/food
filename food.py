import streamlit as st

# 1. 초기 설정
color_theme = {
    "조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"
}

if 'active_meal' not in st.session_state:
    st.session_state.active_meal = "중식"

current = st.session_state.active_meal

# 2. 레이아웃 강제 고정 CSS (가로 좁아짐 방지)
st.markdown(f"""
<style>
    /* 메인 컨테이너 너비 제한 (폰 화면 최적화) */
    .main .block-container {{ max-width: 450px !important; padding: 15px 5px !important; }}

    /* [핵심] 버튼을 담는 가로 박스 설정 */
    [data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-direction: row !important; /* 무조건 가로로 배치 */
        flex-wrap: nowrap !important; /* 아래로 줄바꿈 금지 */
        justify-content: space-between !important;
        gap: 4px !important;
    }}

    /* 각 컬럼(버튼)이 전체의 1/5씩 차지하도록 강제 */
    [data-testid="column"] {{
        flex: 1 1 0% !important;
        min-width: 0 !important; /* 좁은 화면에서도 줄어들 수 있게 허용 */
    }}

    /* 버튼 스타일 디자인 */
    div.stButton > button {{
        width: 100% !important;
        height: 42px !important;
        padding: 0 !important;
        font-size: 12px !important;
        font-weight: 800 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        transition: transform 0.2s;
    }}

    /* 버튼 개별 색상 및 활성화 투명도 */
    div[data-testid="column"]:nth-of-type(1) button {{ background-color: {color_theme["조식"]} !important; opacity: {1.0 if current == "조식" else 0.4}; }}
    div[data-testid="column"]:nth-of-type(2) button {{ background-color: {color_theme["간편식"]} !important; opacity: {1.0 if current == "간편식" else 0.4}; }}
    div[data-testid="column"]:nth-of-type(3) button {{ background-color: {color_theme["중식"]} !important; opacity: {1.0 if current == "중식" else 0.4}; }}
    div[data-testid="column"]:nth-of-type(4) button {{ background-color: {color_theme["석식"]} !important; opacity: {1.0 if current == "석식" else 0.4}; }}
    div[data-testid="column"]:nth-of-type(5) button {{ background-color: {color_theme["야식"]} !important; opacity: {1.0 if current == "야식" else 0.4}; }}

    /* 중앙 식단 표시 카드 */
    .info-box {{
        border: 2px solid {color_theme[current]};
        border-radius: 15px; padding: 25px 10px;
        text-align: center; background-color: white;
        margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }}
</style>
""", unsafe_allow_html=True)

# 3. 화면 UI 출력
st.markdown(f'<div class="info-box"><h1 style="color: {color_theme[current]}; margin:0;">{current}</h1></div>', unsafe_allow_html=True)

# 4. 버튼 생성 (이제 절대 깨지지 않습니다)
cols = st.columns(5)
meals = list(color_theme.keys())

for i, m in enumerate(meals):
    if cols[i].button(m, key=f"fixed_btn_{m}"):
        st.session_state.active_meal = m
        st.rerun()
