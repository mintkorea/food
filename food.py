import streamlit as st

# 1. 페이지 설정 및 상태 관리
st.set_page_config(layout="centered")

color_theme = {
    "조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"
}

if 'active_meal' not in st.session_state:
    st.session_state.active_meal = "중식"

current = st.session_state.active_meal

# 2. CSS: Streamlit 버튼을 '가로 가득 찬 탭'으로 개조
# nth-child를 사용하여 각 버튼에 고유 색상을 입힙니다.
st.markdown(f"""
<style>
    /* 메인 컨테이너 여백 제거 */
    .main .block-container {{ max-width: 500px !important; padding: 10px !important; }}

    /* 가로 버튼 컨테이너 (st.columns 대응) */
    [data-testid="column"] {{
        padding: 0 2px !important;
    }}

    /* 버튼 기본 스타일 */
    div.stButton > button {{
        width: 100% !important;
        border-radius: 10px !important;
        height: 55px !important; /* 터치하기 쉬운 높이 */
        font-weight: bold !important;
        font-size: 15px !important;
        color: white !important;
        border: none !important;
        transition: 0.2s;
    }}

    /* 각 버튼별 색상 및 선택 효과 */
    /* 1번: 조식 */
    div[data-testid="column"]:nth-of-type(1) button {{ 
        background-color: {color_theme["조식"]} !important; 
        opacity: {1.0 if current == "조식" else 0.4} !important;
        border: {"3px solid white" if current == "조식" else "none"} !important;
    }}
    /* 2번: 간편식 */
    div[data-testid="column"]:nth-of-type(2) button {{ 
        background-color: {color_theme["간편식"]} !important; 
        opacity: {1.0 if current == "간편식" else 0.4} !important;
        border: {"3px solid white" if current == "간편식" else "none"} !important;
    }}
    /* 3번: 중식 */
    div[data-testid="column"]:nth-of-type(3) button {{ 
        background-color: {color_theme["중식"]} !important; 
        opacity: {1.0 if current == "중식" else 0.4} !important;
        border: {"3px solid white" if current == "중식" else "none"} !important;
    }}
    /* 4번: 석식 */
    div[data-testid="column"]:nth-of-type(4) button {{ 
        background-color: {color_theme["석식"]} !important; 
        opacity: {1.0 if current == "석식" else 0.4} !important;
        border: {"3px solid white" if current == "석식" else "none"} !important;
    }}
    /* 5번: 야식 */
    div[data-testid="column"]:nth-of-type(5) button {{ 
        background-color: {color_theme["야식"]} !important; 
        opacity: {1.0 if current == "야식" else 0.4} !important;
        border: {"3px solid white" if current == "야식" else "none"} !important;
    }}

    .meal-card {{
        border: 2px solid {color_theme[current]};
        border-radius: 20px; padding: 40px 10px; text-align: center;
        background-color: white; margin-bottom: 20px;
    }}
</style>
""", unsafe_allow_html=True)

# 3. UI 구성
st.title("🍴 오늘의 식단")

st.markdown(f"""
    <div class="meal-card">
        <h2 style="color: {color_theme[current]};">{current}</h2>
        <p style="font-size: 18px; font-weight: bold; color: #555; margin-top:10px;">🍱 선택한 식단을 확인하세요</p>
    </div>
""", unsafe_allow_html=True)

# 4. 가로 버튼 배치 (st.columns 사용)
cols = st.columns(5)
meals = list(color_theme.keys())

for i, meal in enumerate(meals):
    if cols[i].button(meal, key=f"btn_{meal}"):
        st.session_state.active_meal = meal
        st.rerun()
