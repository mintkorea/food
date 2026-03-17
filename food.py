import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="오늘의 식사", layout="centered")

# 2. 데이터 및 컬러 정의
menu_data = {
    "2026-03-17(화)": {
        "조식": ["연포탕", "매운두부찜"], "간편식": ["샌드위치", "요거트"],
        "중식": ["버섯불고기", "우엉채레몬튀김", "수수기장밥", "얼큰어묵탕", "수정과"],
        "석식": ["멘치카츠", "가쓰오장국"], "야식": ["소고기미역죽"]
    }
}

color_map = {
    "조식": ("#E95444", "#FFF5F4"), "간편식": ("#F1A33B", "#FFF9F0"),
    "중식": ("#8BC34A", "#F9FBF2"), "석식": ("#4A90E2", "#F0F7FF"), "야식": ("#673AB7", "#F7F2FF")
}

if 'selected_meal' not in st.session_state:
    st.session_state.selected_meal = "중식"

# 3. 레이아웃 스타일 설정 (버튼을 위로 올리는 핵심 로직)
st.markdown("""
    <style>
    /* 전체 컨테이너를 상대 좌표로 설정 */
    .main-container {
        position: relative;
        display: flex;
        width: 100%;
        height: 380px;
    }
    /* 실제 클릭되는 Streamlit 버튼들을 오른쪽 인덱스 위치로 강제 이동 */
    .stButton {
        position: absolute;
        right: 0;
        width: 45px; /* 인덱스 너비 */
        height: 20%; /* 5개 메뉴니까 20%씩 */
        z-index: 100;
    }
    /* 버튼 내부 스타일: 투명하게 만들어서 배경(인덱스)이 보이게 함 */
    .stButton > button {
        width: 100%;
        height: 100%;
        background: transparent !important;
        border: none !important;
        color: transparent !important;
        margin: 0;
        padding: 0;
    }
    /* 버튼 위치 개별 조정 */
    div[data-testid="stColumn"]:nth-child(1) .stButton { top: 0%; }
    div[data-testid="stColumn"]:nth-child(2) .stButton { top: 20%; }
    div[data-testid="stColumn"]:nth-child(3) .stButton { top: 40%; }
    div[data-testid="stColumn"]:nth-child(4) .stButton { top: 60%; }
    div[data-testid="stColumn"]:nth-child(5) .stButton { top: 80%; }
    </style>
""", unsafe_allow_html=True)

# 4. 카드 렌더링 함수
def render_card(selected_meal, date):
    bold_c, soft_c = color_map[selected_meal]
    menu = menu_data[date].get(selected_meal, ["정보 없음"])
    
    tabs_html = ""
    for label in ["조식", "간편식", "중식", "석식", "야식"]:
        b_color, _ = color_map[label]
        opacity = "1.0" if label == selected_meal else "0.4"
        tabs_html += f'<div style="background-color:{b_color}; flex:1; display:flex; align-items:center; justify-content:center; writing-mode:vertical-rl; text-orientation:upright; color:white; font-weight:bold; font-size:12px; opacity:{opacity}; border-radius:0 10px 10px 0; border-bottom:1px solid white;">{label}</div>'

    return f"""
    <div style="display: flex; width: 100%; height: 380px;">
        <div style="flex: 1; background-color: {soft_c}; border: 3px solid {bold_c}; border-radius: 15px 0 0 15px; padding: 20px; text-align: center; display: flex; flex-direction: column; justify-content: center;">
            <h2 style="color: {bold_c}; margin: 0;">{selected_meal}</h2>
            <hr style="border: 0.5px solid {bold_c}; opacity: 0.2; margin: 15px 0;">
            <p style="font-size: 20px; font-weight: bold;">{menu[0]}</p>
            <p style="font-size: 15px; color: #666;">{' / '.join(menu[1:])}</p>
        </div>
        <div style="display: flex; flex-direction: column; width: 45px;">
            {tabs_html}
        </div>
    </div>
    """

# 5. 화면 표시
st.markdown("### 🍴 오늘의 식사")
selected_date = st.selectbox("날짜", list(menu_data.keys()), label_visibility="collapsed")

# (1) 시각적인 카드 먼저 표시
st.markdown(render_card(st.session_state.selected_meal, selected_date), unsafe_allow_html=True)

# (2) 그 위에 투명 버튼 5개를 덧씌움 (CSS가 위치를 잡아줌)
cols = st.columns(5)
for i, meal in enumerate(["조식", "간편식", "중식", "석식", "야식"]):
    if cols[i].button(meal, key=f"btn_{meal}"):
        st.session_state.selected_meal = meal
        st.rerun()
