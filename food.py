import streamlit as st

# 1. 데이터 및 테마 설정
color_theme = {
    "조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"
}

if 'active_meal' not in st.session_state:
    st.session_state.active_meal = "중식"

# 2. CSS: 레이아웃 고정 및 링크 스타일
st.markdown(f"""
<style>
    /* 전체 컨테이너 너비 고정 */
    .main .block-container {{
        max-width: 450px !important;
        padding: 10px !important;
    }}

    /* 가로 링크 바 컨테이너 */
    .nav-wrapper {{
        display: flex !important;
        flex-direction: row !important;
        justify-content: center !important;
        gap: 5px !important;
        margin-top: 20px;
        width: 100%;
    }}

    /* 링크 버튼 스타일 */
    .meal-link {{
        flex: 1;
        text-align: center;
        padding: 12px 0;
        font-size: 14px;
        font-weight: bold;
        text-decoration: none;
        border-radius: 8px;
        color: white !important;
        transition: 0.2s;
        cursor: pointer;
        border: none;
        display: block;
    }}
</style>
""", unsafe_allow_html=True)

# 3. 메인 식단 카드 (생략 가능, 기존 코드 활용)
st.title("🍴 오늘의 식사")
current = st.session_state.active_meal
st.markdown(f"""
    <div style="background-color: white; border: 2px solid {color_theme[current]}; border-radius: 15px; padding: 30px; text-align: center;">
        <h2 style="color: {color_theme[current]};">{current}</h2>
        <p style="font-size: 22px; font-weight: bold; margin-top: 20px;">🍲 오늘의 메뉴</p>
    </div>
""", unsafe_allow_html=True)

# 4. 링크 형태의 가로 바 구현
# st.columns를 사용하지 않고 한 줄에 HTML로 다 넣습니다.
nav_html = '<div class="nav-wrapper">'
for meal, color in color_theme.items():
    opacity = "1.0" if meal == current else "0.3"
    # 클릭 시 세션 상태를 바꾸기 위해 Streamlit의 쿼리 파라미터나 hidden button 트릭 대신 
    # 가장 확실한 'invisible button' 레이어 방식을 사용합니다.
    nav_html += f'<div style="flex:1;"><a class="meal-link" style="background-color:{color}; opacity:{opacity};">{meal}</a></div>'
nav_html += '</div>'

st.markdown(nav_html, unsafe_allow_html=True)

# 5. 실제 클릭을 처리할 투명 레이어 (Hidden Buttons)
# HTML 바 바로 아래에 아주 얇게 버튼들을 배치하여 실제 클릭 기능을 부여합니다.
cols = st.columns(5)
for i, meal in enumerate(color_theme.keys()):
    with cols[i]:
        # 버튼을 투명하게 만들어 위 HTML 바와 겹치게 보이게 함 (CSS로 위치 조정 가능)
        st.button(meal, key=f"hidden_{meal}", on_click=lambda m=meal: setattr(st.session_state, 'active_meal', m), use_container_width=True)

st.markdown("""
<style>
    /* hidden button들을 HTML 바 위치로 끌어올리고 투명화 */
    div[data-testid="stHorizontalBlock"] {{
        margin-top: -50px !important; /* 위 HTML 바 위로 덮음 */
        opacity: 0 !important; /* 완전히 투명하게 */
        height: 50px;
    }}
</style>
""", unsafe_allow_html=True)
