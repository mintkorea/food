import streamlit as st

# 1. 테마 및 데이터 설정
color_theme = {
    "조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"
}

# 2. 쿼리 파라미터를 이용한 상태 관리 (버튼 대신 링크 클릭 감지)
query_params = st.query_params
if "meal" in query_params:
    st.session_state.active_meal = query_params["meal"]
elif 'active_meal' not in st.session_state:
    st.session_state.active_meal = "중식"

current = st.session_state.active_meal

# 3. CSS: 모바일 가로 고정 및 링크 스타일
st.markdown(f"""
<style>
    /* 메인 컨테이너 너비 제한 및 중앙 정렬 */
    .main .block-container {{
        max-width: 450px !important;
        padding: 10px !important;
    }}

    /* 가로 메뉴바 - 절대 세로로 변하지 않음 */
    .nav-bar {{
        display: flex !important;
        flex-direction: row !important;
        justify-content: center !important;
        width: 100% !important;
        margin: 20px 0;
        gap: 4px;
    }}

    /* 메뉴 아이템 스타일 */
    .nav-item {{
        flex: 1;
        text-align: center;
        padding: 12px 0;
        font-size: 14px;
        font-weight: bold;
        text-decoration: none !important;
        border-radius: 8px;
        color: white !important;
        transition: 0.2s;
        display: block;
    }}

    /* 식단 카드 디자인 */
    .meal-card {{
        background-color: white;
        border: 2px solid {color_theme[current]};
        border-radius: 20px;
        padding: 40px 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }}
</style>
""", unsafe_allow_html=True)

# 4. 메인 UI 구성
st.title("🍴 오늘의 식사")

# 식단 카드 표시
st.markdown(f"""
    <div class="meal-card">
        <h2 style="color: {color_theme[current]};">{current}</h2>
        <div style="width: 30px; height: 3px; background-color: {color_theme[current]}; margin: 15px auto;"></div>
        <p style="font-size: 24px; font-weight: bold; margin-top: 20px;">🍲 오늘의 메뉴</p>
        <p style="color: #666; margin-top: 10px;">상세 메뉴 정보가 여기에 표시됩니다.</p>
    </div>
""", unsafe_allow_html=True)

# 5. HTML 가로 메뉴바 (링크 방식)
# 버튼 대신 <a> 태그를 사용하여 클릭 시 URL 뒤에 ?meal=... 을 붙여 새로고침합니다.
nav_html = '<div class="nav-bar">'
for meal, color in color_theme.items():
    opacity = "1.0" if meal == current else "0.3"
    # 현재 URL을 유지하면서 파라미터만 변경
    nav_html += f"""
        <a href="/?meal={meal}" target="_self" class="nav-item" 
           style="background-color: {color}; opacity: {opacity};">
            {meal}
        </a>
    """
nav_html += '</div>'

st.markdown(nav_html, unsafe_allow_html=True)
