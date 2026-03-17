import streamlit as st

# 1. 색상 및 식단 데이터 설정
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

# 2. 세션 상태 초기화 및 콜백 함수 (오류 해결의 핵심)
if 'meal_selection' not in st.session_state:
    st.session_state.meal_selection = "중식"

def change_meal(meal_name):
    st.session_state.meal_selection = meal_name

# 3. CSS: 인덱스 고정 및 디자인
sel_meal = st.session_state.meal_selection
bold_c = color_theme[sel_meal]["idx"]
soft_bg = color_theme[sel_meal]["bg"]

st.markdown(f"""
<style>
    .main-card {{
        background-color: {soft_bg};
        border: 2.5px solid {bold_c};
        border-radius: 15px 0 0 15px;
        padding: 40px 20px;
        margin-right: 52px;
        min-height: 380px;
        text-align: center;
        transition: all 0.3s ease-in-out;
    }}
    .fixed-nav {{
        position: fixed;
        right: 8px;
        top: 50%;
        transform: translateY(-50%);
        display: flex;
        flex-direction: column;
        gap: 4px;
        z-index: 1000;
    }}
</style>
""", unsafe_allow_html=True)

# 4. UI 렌더링
st.title("🍴 오늘의 식사")
st.selectbox("날짜", ["2026-03-17(화)"], label_visibility="collapsed")

# 메인 콘텐츠 영역
menu = menu_data.get(sel_meal, ["정보 없음"])
st.markdown(f"""
    <div class="main-card">
        <h2 style="color: {bold_c}; margin-bottom: 25px;">{sel_meal}</h2>
        <p style="font-size: 24px; font-weight: bold; color: #333;">🍲 {menu[0]}</p>
        <p style="font-size: 16px; color: #555; margin-top: 20px; line-height: 1.8;">
            {' / '.join(menu[1:])}
        </p>
    </div>
""", unsafe_allow_html=True)

# 5. 고정 인덱스 버튼 (on_click 콜백 적용으로 오작동 방지)
st.markdown('<div class="fixed-nav">', unsafe_allow_html=True)
for meal in ["조식", "간편식", "중식", "석식", "야식"]:
    m_color = color_theme[meal]["idx"]
    is_active = (meal == sel_meal)
    
    # 각 버튼별 스타일 개별 적용
    st.markdown(f"""
        <style>
        button[key="btn_{meal}"] {{
            background-color: {m_color} !important;
            opacity: {1.0 if is_active else 0.4};
            color: white !important;
            writing-mode: vertical-rl;
            text-orientation: upright;
            height: 82px !important;
            width: 46px !important;
            border-radius: 0 10px 10px 0 !important;
            border: none !important;
            font-weight: bold !important;
            box-shadow: {"2px 2px 10px rgba(0,0,0,0.3)" if is_active else "none"};
        }}
        </style>
    """, unsafe_allow_html=True)
    
    # on_click을 사용하여 즉각적인 상태 변경 보장
    st.button(meal, key=f"btn_{meal}", on_click=change_meal, args=(meal,))
st.markdown('</div>', unsafe_allow_html=True)
