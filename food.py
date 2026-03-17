import streamlit as st
import streamlit.components.v1 as components

# 1. 테마 설정
color_theme = {
    "조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"
}

# 쿼리 파라미터로 선택 상태 유지
query_params = st.query_params
current = query_params.get("meal", "중식")

# 2. 메인 UI (상단 카드)
st.title("🍴 오늘의 식단")
st.markdown(f"""
    <div style="border: 2px solid {color_theme.get(current)}; border-radius: 20px; 
                padding: 40px 20px; text-align: center; background-color: white;">
        <h2 style="color: {color_theme.get(current)}; margin: 0;">{current}</h2>
        <hr style="border: 1px solid #eee; margin: 20px 0;">
        <p style="font-size: 18px; font-weight: bold; color: #333;">🍱 식단을 선택해주세요</p>
    </div>
""", unsafe_allow_html=True)

# 3. HTML/CSS 기반 커스텀 가로 메뉴바
# 이 부분은 독립된 iframe으로 실행되어 모바일에서도 레이아웃이 깨지지 않습니다.
nav_items_html = ""
for meal, color in color_theme.items():
    opacity = "1.0" if meal == current else "0.4"
    # 클릭 시 부모 창(top)의 URL을 변경하여 즉시 새로고침 유도
    nav_items_html += f"""
        <a href="/?meal={meal}" target="_top" 
           style="flex: 1; text-align: center; background-color: {color}; 
                  opacity: {opacity}; color: white; text-decoration: none; 
                  padding: 15px 0; border-radius: 10px; font-size: 16px; 
                  font-weight: bold; font-family: sans-serif;">
            {meal}
        </a>
    """

custom_nav_bar = f"""
    <div style="display: flex; gap: 8px; width: 100%; padding: 10px 0;">
        {nav_items_html}
    </div>
"""

# 컴포넌트 실행 (높이를 80px로 여유 있게 설정)
components.html(custom_nav_bar, height=80)

# 4. CSS: Streamlit 기본 여백 제거 (모바일 가득 채우기)
st.markdown("""
<style>
    .main .block-container { max-width: 500px !important; padding: 10px !important; }
    iframe { width: 100% !important; border: none !important; }
</style>
""", unsafe_allow_html=True)
