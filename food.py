import streamlit as st

# 1. 설정 및 테마
color_theme = {
    "조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"
}

# 쿼리 파라미터로 선택된 식단 가져오기
query_params = st.query_params
active_meal = query_params.get("meal", "중식")

# 2. CSS: 가로 한 줄 강제 고정 및 텍스트 노출 방지
st.markdown(f"""
<style>
    /* 메인 너비 고정 */
    .main .block-container {{
        max-width: 450px !important;
        padding: 10px !important;
    }}

    /* 가로 메뉴바 컨테이너 */
    .nav-bar {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important; /* 줄바꿈 절대 금지 */
        justify-content: space-between;
        width: 100%;
        margin: 20px 0;
        gap: 5px;
    }}

    /* 메뉴 버튼(링크) 스타일 */
    .nav-item {{
        flex: 1;
        text-align: center;
        padding: 12px 0;
        font-size: 13px;
        font-weight: bold;
        text-decoration: none !important;
        border-radius: 10px;
        color: white !important;
        display: block;
    }}
    
    /* 카드 디자인 */
    .meal-card {{
        background-color: #fdfdfd;
        border: 2px solid {color_theme.get(active_meal, "#8BC34A")};
        border-radius: 20px;
        padding: 30px 15px;
        text-align: center;
    }}
</style>
""", unsafe_allow_html=True)

# 3. UI 출력
st.title("🍴 오늘의 식사")

# 식단 카드
st.markdown(f"""
    <div class="meal-card">
        <h2 style="color: {color_theme.get(active_meal, "#8BC34A")};">{active_meal}</h2>
        <p style="font-size: 22px; font-weight: bold; margin-top: 15px;">🍲 오늘의 추천 메뉴</p>
        <p style="color: #666; margin-top: 10px;">상세 내용은 식단을 선택해 확인하세요.</p>
    </div>
""", unsafe_allow_html=True)

# 4. 가로 메뉴바 생성 (HTML 링크 방식)
# 버튼 대신 <a> 태그를 사용하여 클릭 시 URL 파라미터를 변경함
nav_items = ""
for meal, color in color_theme.items():
    opacity = "1.0" if meal == active_meal else "0.35"
    # st.query_params와 연동되는 링크 생성
    nav_items += f'<a href="/?meal={meal}" target="_self" class="nav-item" style="background-color: {color}; opacity: {opacity};">{meal}</a>'

st.markdown(f'<div class="nav-bar">{nav_items}</div>', unsafe_allow_html=True)
