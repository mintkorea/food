import streamlit as st

st.set_page_config(page_title="오늘의 식사", layout="centered")

# 1. 데이터 설정
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

# 2. CSS: 투명 버튼을 인덱스 위치에 강제로 박아넣기
st.markdown("""
    <style>
    /* 1. 카드가 들어갈 컨테이너 설정 */
    .card-wrapper {
        position: relative;
        width: 100%;
        height: 400px;
    }
    
    /* 2. 실제 Streamlit 버튼을 인덱스 위치로 이동 및 투명화 */
    div[data-testid="stHorizontalBlock"] {
        position: absolute !important;
        top: 45px !important; /* 날짜 선택창 아래 위치로 조정 */
        right: 0 !important;
        width: 45px !important; /* 인덱스 너비만큼 */
        height: 380px !important;
        z-index: 999 !important; /* 무조건 맨 위로 */
        display: flex !important;
        flex-direction: column !important;
        gap: 0 !important;
    }

    div[data-testid="stColumn"] {
        flex: 1 !important;
        width: 100% !important;
    }

    /* 3. 버튼 디자인 제거 (완전 투명 클릭 영역) */
    .stButton > button {
        width: 45px !important;
        height: 76px !important; /* 380px / 5개 */
        background: transparent !important;
        border: none !important;
        color: transparent !important;
        box-shadow: none !important;
        cursor: pointer !important;
    }
    
    .stButton > button:hover {
        background: rgba(255,255,255,0.1) !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 렌더링 함수
def render_card(selected_meal, date):
    bold_c, soft_c = color_map[selected_meal]
    menu = menu_data[date].get(selected_meal, ["정보 없음"])
    
    tabs_html = ""
    for label in ["조식", "간편식", "중식", "석식", "야식"]:
        b_color, _ = color_map[label]
        opacity = "1.0" if label == selected_meal else "0.4"
        tabs_html += f'<div style="background-color:{b_color}; flex:1; display:flex; align-items:center; justify-content:center; writing-mode:vertical-rl; text-orientation:upright; color:white; font-weight:bold; font-size:12px; opacity:{opacity}; border-radius:0 10px 10px 0; border-bottom:1px solid rgba(255,255,255,0.2);">{label}</div>'

    return f"""
    <div class="card-wrapper" style="display: flex; width: 100%; height: 380px;">
        <div style="flex: 1; background-color: {soft_c}; border: 3.2px solid {bold_c}; border-radius: 15px 0 0 15px; padding: 25px; text-align: center; display: flex; flex-direction: column; justify-content: center;">
            <h2 style="color: {bold_c}; margin-bottom: 20px;">{selected_meal}</h2>
            <p style="font-size: 22px; font-weight: bold; color: #333;">{menu[0]}</p>
            <p style="font-size: 16px; color: #666; line-height: 1.8;">{' / '.join(menu[1:])}</p>
        </div>
        <div style="display: flex; flex-direction: column; width: 45px;">
            {tabs_html}
        </div>
    </div>
    """

# 4. 앱 구성
st.markdown("### 🍴 오늘의 식사")
selected_date = st.selectbox("날짜", list(menu_data.keys()), label_visibility="collapsed")

# 카드 표시
st.markdown(render_card(st.session_state.selected_meal, selected_date), unsafe_allow_html=True)

# 카드 바로 아래에 정의하지만, CSS가 인덱스 위치로 끌어올림
cols = st.columns(1) # 세로로 쌓기 위해 하나만 사용하거나 CSS로 제어
with st.container():
    c1, c2, c3, c4, c5 = st.columns(5) # 실제 클릭은 여기서 발생
    if c1.button("1", key="b1"): st.session_state.selected_meal="조식"; st.rerun()
    if c2.button("2", key="b2"): st.session_state.selected_meal="간편식"; st.rerun()
    if c3.button("3", key="b3"): st.session_state.selected_meal="중식"; st.rerun()
    if c4.button("4", key="b4"): st.session_state.selected_meal="석식"; st.rerun()
    if c5.button("5", key="b5"): st.session_state.selected_meal="야식"; st.rerun()
