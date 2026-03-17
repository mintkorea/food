import streamlit as st

# 1. 데이터 설정
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

# 3. CSS: 브라우저 뷰포트(Viewport) 기준 절대 고정
# !important를 모든 속성에 부여하여 Streamlit의 간섭을 차단합니다.
st.markdown(f"""
<style>
    /* 메인 앱의 너비 제한 및 오른쪽 여백 확보 */
    .main .block-container {{
        max-width: 550px !important;
        padding-right: 80px !important;
        margin: 0 auto !important;
    }}

    /* 플로팅 버튼들을 감싸는 컨테이너 - 화면에 고정 */
    [data-testid="stVerticalBlock"] > div:has(button[key^="btn_"]) {{
        position: fixed !important;
        right: 0px !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        width: 55px !important;
        z-index: 999999 !important;
        background-color: transparent !important;
    }}

    /* 버튼 스타일 강제 적용 */
    button[key^="btn_"] {{
        writing-mode: vertical-rl !important;
        text-orientation: upright !important;
        height: 85px !important;
        width: 50px !important;
        min-width: 50px !important;
        border-radius: 12px 0 0 12px !important;
        border: none !important;
        color: white !important;
        font-weight: bold !important;
        margin-bottom: 3px !important;
        box-shadow: -2px 2px 10px rgba(0,0,0,0.2) !important;
        cursor: pointer !important;
    }}
</style>
""", unsafe_allow_html=True)

# 4. 메인 식단 카드
st.title("🍴 스마트 식단 가이드")

st.markdown(f"""
    <div style="
        background-color: {soft_bg};
        border: 2.5px solid {bold_c};
        border-radius: 20px;
        padding: 35px 20px;
        text-align: center;
        min-height: 400px;
    ">
        <h2 style="color: {bold_c};">{current_sel}</h2>
        <div style="width: 40px; height: 3px; background-color: {bold_c}; margin: 15px auto;"></div>
        <p style="font-size: 24px; font-weight: bold; color: #333; margin-top: 20px;">🍲 {menu_data[current_sel][0]}</p>
        <p style="font-size: 16px; color: #555; margin-top: 15px; line-height: 1.8;">
            {' / '.join(menu_data[current_sel][1:])}
        </p>
    </div>
""", unsafe_allow_html=True)

# 5. 플로팅 버튼 생성
# 이 버튼들이 CSS 선택자에 의해 우측 중앙에 고정됩니다.
for meal in ["조식", "간편식", "중식", "석식", "야식"]:
    is_active = (meal == current_sel)
    m_color = color_theme[meal]["idx"]
    
    st.markdown(f"""
        <style>
        button[key="btn_{meal}"] {{
            background-color: {m_color} !important;
            opacity: {1.0 if is_active else 0.4} !important;
            transform: {"scaleX(1.15) translateX(-5px)" if is_active else "none"} !important;
            transition: all 0.2s ease !important;
        }}
        </style>
    """, unsafe_allow_html=True)
    
    st.button(meal, key=f"btn_{meal}", on_click=update_meal, args=(meal,))
