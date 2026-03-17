import streamlit as st
import streamlit.components.v1 as components

# 1. 테마 설정
color_theme = {
    "조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"
}

# 쿼리 파라미터 읽기
current = st.query_params.get("meal", "중식")

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

# 3. 메뉴바 생성 (클릭 문제 해결 버전)
nav_items_html = ""
for meal, color in color_theme.items():
    is_active = (meal == current)
    # <a> 태그 대신 onclick 이벤트를 사용하여 부모 창의 URL을 변경합니다.
    nav_items_html += f"""
        <div onclick="window.parent.location.href='/?meal={meal}'" 
             style="flex: 1; text-align: center; background-color: {color}; 
                    opacity: {1.0 if is_active else 0.4}; color: white; 
                    padding: 15px 0; border-radius: 10px; font-size: 15px; 
                    font-weight: bold; cursor: pointer; font-family: sans-serif;
                    border: { '2px solid white' if is_active else 'none' };">
            {meal}
        </div>
    """

# 전체를 감싸는 컨테이너
custom_nav_bar = f"""
    <div style="display: flex; gap: 6px; width: 100%; padding: 5px 0;">
        {nav_items_html}
    </div>
"""

# 컴포넌트 실행
components.html(custom_nav_bar, height=80)

# 4. 앱 레이아웃 최적화
st.markdown("""
<style>
    .main .block-container { max-width: 500px !important; padding: 10px !important; }
    iframe { width: 100% !important; border: none !important; }
</style>
""", unsafe_allow_html=True)