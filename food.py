import streamlit as st

# 1. 테마 및 데이터
color_theme = {
    "조식": {"idx": "#E95444", "bg": "#F9EBEA"},
    "간편식": {"idx": "#F1A33B", "bg": "#FEF5E7"},
    "중식": {"idx": "#8BC34A", "bg": "#F1F8E9"},
    "석식": {"idx": "#4A90E2", "bg": "#EBF5FB"},
    "야식": {"idx": "#673AB7", "bg": "#F4ECF7"}
}

menu_data = {
    "조식": ["제철미나리쭈꾸미연포탕", "매운두부찜", "흰쌀밥", "모둠장아찌", "누룽지"],
    "간편식": ["고로케양배추샌드위치", "삶은계란", "플레인요거트"],
    "중식": ["버섯불고기", "우엉채레몬튀김", "수수기장밥", "얼큰어묵탕", "수정과"],
    "석식": ["양배추멘치카츠", "가쓰오장국", "시저드레싱샐러드", "열무김치"],
    "야식": ["소고기미역죽", "돈육장조림", "깍두기", "블루베리요플레"]
}

# 2. 세션 관리
if 'active_meal' not in st.session_state:
    st.session_state.active_meal = "중식"

def update_meal(meal_name):
    st.session_state.active_meal = meal_name

current_sel = st.session_state.active_meal
bold_c = color_theme[current_sel]["idx"]
soft_bg = color_theme[current_sel]["bg"]

# 3. CSS: 부모 요소를 타겟팅하여 화면 우측에 강제 고정
st.markdown(f"""
<style>
    /* 메인 컨테이너 여백 */
    .main .block-container {{
        padding-right: 70px !important;
        padding-left: 15px !important;
    }}

    /* 인덱스 버튼들을 감싸는 부모 div를 찾아서 고정 */
    div[data-testid="stVerticalBlock"] > div:has(button[key^="btn_"]) {{
        position: fixed !important;
        right: 0px !important;
        top: 15% !important;
        width: 55px !important;
        z-index: 999999 !important;
        display: flex !important;
        flex-direction: column !important;
        gap: 2px !important;
    }}

    /* 버튼 스타일 (ID 기반이 아닌 통합 스타일) */
    button[key^="btn_"] {{
        writing-mode: vertical-rl !important;
        text-orientation: upright !important;
        height: 85px !important;
        width: 50px !important;
        min-width: 50px !important;
        border-radius: 8px 0 0 8px !important;
        border: none !important;
        color: white !important;
        font-weight: bold !important;
        margin: 0 !important;
        padding: 5px 0 !important;
        cursor: pointer !important;
    }}

    /* 메인 카드 */
    .main-card {{
        background-color: {soft_bg};
        border: 2.5px solid {bold_c};
        border-radius: 15px;
        padding: 30px 15px;
        text-align: center;
        min-height: 380px;
    }}
</style>
""", unsafe_allow_html=True)

# 4. UI 구성
st.title("🍴 오늘의 식사")

st.markdown(f"""
    <div class="main-card">
        <h2 style="color: {bold_c};">{current_sel}</h2>
        <hr style="border: 0.5px solid {bold_c}; opacity: 0.3;">
        <p style="font-size: 24px; font-weight: bold; color: #333; margin-top: 25px;">🍲 {menu_data[current_sel][0]}</p>
        <p style="font-size: 16px; color: #555; line-height: 1.8;">{' / '.join(menu_data[current_sel][1:])}</p>
    </div>
""", unsafe_allow_html=True)

# 5. 버튼 렌더링 (이 부분의 부모 div가 CSS로 우측 상단 고정됨)
for meal in ["조식", "간편식", "중식", "석식", "야식"]:
    is_active = (meal == current_sel)
    m_color = color_theme[meal]["idx"]
    
    st.markdown(f"""
        <style>
        button[key="btn_{meal}"] {{
            background-color: {m_color} !important;
            opacity: {1.0 if is_active else 0.4} !important;
            box-shadow: {"-3px 0 10px rgba(0,0,0,0.2)" if is_active else "none"} !important;
        }}
        </style>
    """, unsafe_allow_html=True)
    
    st.button(meal, key=f"btn_{meal}", on_click=update_meal, args=(meal,))
