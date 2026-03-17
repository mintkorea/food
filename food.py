import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="오늘의 식사", layout="centered")

# 2. 데이터 및 컬러 정의 (수정 없이 그대로 사용 가능)
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

# 3. 렌더링 함수 (중괄호 충돌 방지를 위해 이중 중괄호 사용)
def render_guide(selected_meal, date):
    bold_c, soft_c = color_map[selected_meal]
    menu = menu_data[date].get(selected_meal, ["정보 없음"])
    
    tabs_html = ""
    meals = ["조식", "간편식", "중식", "석식", "야식"]
    
    for label in meals:
        b_color, _ = color_map[label]
        is_selected = (label == selected_meal)
        opacity = "1.0" if is_selected else "0.5"
        
        # 탭 개별 스타일
        tabs_html += f"""
        <div style="
            background-color: {b_color};
            color: white;
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            writing-mode: vertical-rl;
            text-orientation: upright;
            font-weight: bold;
            font-size: 13px;
            opacity: {opacity};
            border-radius: 0 10px 10px 0;
            border-bottom: 1px solid rgba(255,255,255,0.2);
            width: 35px;
        ">
            {label}
        </div>
        """

    # 메인 HTML (f-string 내 CSS 중괄호 겹침 주의)
    full_html = f"""
    <div style="display: flex; width: 100%; height: 380px; align-items: stretch;">
        <div style="
            flex: 1;
            background-color: {soft_c};
            border: 3px solid {bold_c};
            border-radius: 15px 0 0 15px;
            padding: 20px;
            text-align: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
            box-shadow: -2px 2px 10px rgba(0,0,0,0.05);
        ">
            <h2 style="color: {bold_c}; font-size: 22px; margin: 0;">{selected_meal}</h2>
            <hr style="border: 0.5px solid {bold_c}; opacity: 0.2; margin: 15px 0;">
            <p style="font-size: 20px; font-weight: bold; color: #333; margin: 0 0 10px 0;">{menu[0]}</p>
            <p style="font-size: 15px; color: #666; line-height: 1.6;">{' / '.join(menu[1:]) if len(menu)>1 else ""}</p>
        </div>
        <div style="display: flex; flex-direction: column; width: 35px;">
            {tabs_html}
        </div>
    </div>
    """
    return full_html

# 4. 화면 표시부
st.markdown('### 🍴 오늘의 식사')
selected_date = st.selectbox("날짜", list(menu_data.keys()), label_visibility="collapsed")

# HTML 렌더링
st.markdown(render_guide(st.session_state.selected_meal, selected_date), unsafe_allow_html=True)

# 5. 하단 버튼 (이 버튼을 눌러야 세션이 갱신되며 화면이 바뀝니다)
st.write("")
cols = st.columns(5)
for i, meal in enumerate(["조식", "간편식", "중식", "석식", "야식"]):
    if cols[i].button(meal):
        st.session_state.selected_meal = meal
        st.rerun()
