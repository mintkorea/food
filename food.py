import streamlit as st
import streamlit.components.v1 as components

# 1. 테마 설정
color_theme = {
    "조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"
}

# 쿼리 파라미터로 선택 상태 유지
current = st.query_params.get("meal", "중식")

# 2. CSS: 앱 레이아웃 최적화
st.markdown(f"""
<style>
    .main .block-container {{ max-width: 500px !important; padding: 10px !important; }}
    .meal-card {{
        border: 2px solid {color_theme.get(current)};
        border-radius: 20px; padding: 30px 15px; text-align: center;
        background-color: white; margin-bottom: 20px;
    }}
</style>
""", unsafe_allow_html=True)

# 3. 메인 UI
st.title("🍴 오늘의 식단")
st.markdown(f"""
    <div class="meal-card">
        <h2 style="color: {color_theme.get(current)};">{current}</h2>
        <p style="font-weight: bold; color: #333; margin-top: 10px;">원하시는 식단을 탭하세요</p>
    </div>
""", unsafe_allow_html=True)

# 4. 고정 간격 가로 메뉴 (HTML/JS)
# 여기서 gap: 4px를 주어 모바일에서도 벌어지지 않게 고정합니다.
nav_buttons = ""
for meal, color in color_theme.items():
    opacity = "1.0" if meal == current else "0.4"
    border = "2px solid white" if meal == current else "none"
    nav_buttons += f"""
        <div onclick="window.parent.location.href='/?meal={meal}'" 
             style="flex: 1; background-color: {color}; opacity: {opacity}; 
                    color: white; padding: 15px 0; text-align: center; 
                    border-radius: 8px; font-size: 14px; font-weight: bold; 
                    cursor: pointer; border: {border}; box-sizing: border-box;">
            {meal}
        </div>
    """

custom_menu_html = f"""
    <div style="display: flex; flex-direction: row; gap: 4px; width: 100%; box-sizing: border-box;">
        {nav_buttons}
    </div>
"""

# 컴포넌트 실행 (iframe 여백 제거)
components.html(custom_menu_html, height=65)

st.markdown("<style>iframe { border: none !important; }</style>", unsafe_allow_html=True)
