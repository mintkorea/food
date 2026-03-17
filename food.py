import streamlit as st

# 1. 페이지 설정 및 여백 제거
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

# 3. 세션 상태 관리 (쿼리 파라미터 대신 사용)
if 'selected_meal' not in st.session_state:
    st.session_state.selected_meal = "중식"

# 4. 전체 레이아웃을 하나의 HTML로 구현
def render_guide(selected_meal, date):
    bold_c, soft_c = color_map[selected_meal]
    menu = menu_data[date].get(selected_meal, ["정보 없음"])
    
    # 인덱스 버튼 HTML 생성
    tabs_html = ""
    for label in ["조식", "간편식", "중식", "석식", "야식"]:
        b_color, _ = color_map[label]
        # 현재 선택된 메뉴면 강조 표시
        opacity = "1.0" if label == selected_meal else "0.6"
        tabs_html += f"""
        <div style="background-color:{b_color}; height:20%; width:100%; color:white; 
                    display:flex; align-items:center; justify-content:center; 
                    writing-mode:vertical-rl; text-orientation:upright; 
                    font-weight:bold; font-size:13px; opacity:{opacity};
                    border-radius:0 10px 10px 0; cursor:pointer; border-bottom:1px solid rgba(255,255,255,0.2);">
            {label}
        </div>
        """

    # 카드 + 인덱스 통합 HTML
    full_html = f"""
    <div style="display: flex; width: 100%; height: 350px; font-family: sans-serif;">
        <div style="flex: 8; background-color: {soft_c}; border: 2.5px solid {bold_c}; 
                    border-radius: 15px 0 0 15px; padding: 20px; text-align: center;
                    display: flex; flex-direction: column; justify-content: center;">
            <h2 style="color: {bold_c}; font-size: 20px; margin: 0;">{selected_meal}</h2>
            <hr style="border: 0.5px solid {bold_c}; opacity: 0.2; margin: 15px 0;">
            <p style="font-size: 22px; font-weight: bold; color: #333; margin-bottom: 10px;">{menu[0]}</p>
            <p style="font-size: 15px; color: #666; line-height: 1.6;">{' / '.join(menu[1:])}</p>
        </div>
        <div style="flex: 2; display: flex; flex-direction: column; height: 100%;">
            {tabs_html}
        </div>
    </div>
    """
    return full_html

# 5. 화면 표시
st.markdown('<div style="font-size:1.2rem; font-weight:bold; margin-bottom:10px;">🍴 오늘의 식사</div>', unsafe_allow_html=True)
selected_date = st.selectbox("날짜", list(menu_data.keys()), label_visibility="collapsed")

# HTML 렌더링
st.markdown(render_guide(st.session_state.selected_meal, selected_date), unsafe_allow_html=True)

# 6. 실제 작동을 위한 투명한 Streamlit 버튼 (HTML 위에 겹치기 대신 하단에 배치)
st.write("---")
cols = st.columns(5)
meals = ["조식", "간편식", "중식", "석식", "야식"]
for i, meal in enumerate(meals):
    if cols[i].button(meal):
        st.session_state.selected_meal = meal
        st.rerun()

st.markdown("""
    <style>
    /* 하단 실제 버튼은 인덱스 역할을 하되 보이지 않거나 작게 처리 가능 */
    div.stButton > button { width: 100%; font-size: 12px; padding: 5px; }
    </style>
""", unsafe_allow_html=True)
