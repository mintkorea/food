import streamlit as st

# 1. 페이지 설정
st.set_page_config(layout="centered")

# 2. 테마 색상 및 데이터
color_theme = {
    "조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"
}

# 3. 쿼리 파라미터 기반 상태 관리 (새로고침 속도 최적화)
if "meal" in st.query_params:
    st.session_state.active_meal = st.query_params["meal"]
elif 'active_meal' not in st.session_state:
    st.session_state.active_meal = "중식"

current = st.session_state.active_meal

# 4. CSS: 모바일 폰트 크기 고정 및 레이아웃 강제
st.markdown(f"""
<style>
    /* 여백 최적화 */
    .main .block-container {{ max-width: 500px !important; padding: 10px !important; }}
    
    /* 가로 메뉴바: 모바일에서도 절대 꺾이지 않고 글자 크기 유지 */
    .nav-bar {{
        display: flex !important;
        flex-direction: row !important;
        width: 100% !important;
        gap: 6px;
        margin: 15px 0;
    }}
    
    .nav-item {{
        flex: 1;
        text-align: center;
        padding: 14px 0 !important; /* 터치하기 편한 높이 */
        font-size: 14px !important; /* 글자 크기 강제 고정 */
        font-weight: 800 !important;
        text-decoration: none !important;
        border-radius: 12px;
        color: white !important;
        display: block !important;
        line-height: 1 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}

    .meal-card {{
        border: 2px solid {color_theme.get(current, "#8BC34A")};
        border-radius: 20px; padding: 40px 20px; text-align: center;
        background-color: #ffffff;
    }}
</style>
""", unsafe_allow_html=True)

# 5. UI 메인 섹션
st.title("🍴 오늘의 식단")

st.markdown(f"""
    <div class="meal-card">
        <h2 style="color: {color_theme.get(current, "#8BC34A")}; margin: 0;">{current}</h2>
        <div style="width: 40px; height: 3px; background-color: {color_theme.get(current, "#8BC34A")}; margin: 20px auto;"></div>
        <p style="font-size: 18px; font-weight: bold; color: #333;">🍱 식단을 선택해주세요</p>
    </div>
""", unsafe_allow_html=True)

# 6. 가로 메뉴바 (순수 HTML <a> 태그 방식)
# Streamlit 위젯을 거치지 않으므로 텍스트가 임의로 작아지거나 숨겨지지 않습니다.
nav_html = '<div class="nav-bar">'
for meal, color in color_theme.items():
    # 선택된 메뉴는 투명도 1.0, 나머지는 0.4
    opacity = "1.0" if meal == current else "0.4"
    # 클릭 시 URL 파라미터를 변경하여 현재 페이지로 리다이렉트
    nav_html += f"""
        <a href="/?meal={meal}" target="_self" class="nav-item" 
           style="background-color: {color}; opacity: {opacity};">
            {meal}
        </a>
    """
nav_html += '</div>'

st.markdown(nav_html, unsafe_allow_html=True)
