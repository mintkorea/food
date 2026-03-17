import streamlit as st

# 1. 테마 및 데이터 설정
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

# 2. 세션 상태 관리
if 'active_meal' not in st.session_state:
    st.session_state.active_meal = "중식"

def update_meal(meal_name):
    st.session_state.active_meal = meal_name

current_sel = st.session_state.active_meal
bold_c = color_theme[current_sel]["idx"]
soft_bg = color_theme[current_sel]["bg"]

# 3. CSS: 가로 정렬 및 버튼 크기 고정
st.markdown(f"""
<style>
    /* 메인 컨테이너 */
    .main .block-container {{
        padding: 10px 15px !important;
        max-width: 450px !important;
    }}

    /* 식단 카드 */
    .main-card {{
        background-color: {soft_bg};
        border: 2px solid {bold_c};
        border-radius: 20px;
        padding: 30px 15px;
        text-align: center;
        margin-bottom: 25px;
    }}

    /* ★ 가로 버튼 뭉치 중앙 정렬 및 너비 제한 ★ */
    div[data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-direction: row !important;
        justify-content: center !important; /* 중앙으로 모음 */
        align-items: center !important;
        gap: 8px !important; /* 버튼 사이 간격 */
        width: 100% !important;
    }}

    /* 개별 버튼 크기 강제 고정 */
    button[key^="btn_"] {{
        min-width: 65px !important; /* 너무 좁아지지 않게 */
        max-width: 80px !important; /* 너무 넓어지지 않게 */
        height: 42px !important;
        padding: 0 !important;
        font-size: 13px !important;
        border: none !important;
        color: white !important;
        border-radius: 10px !important;
        flex: none !important; /* 늘어나지 않도록 설정 */
    }}
</style>
""", unsafe_allow_html=True)

# 4. 메인 UI
st.title("🍴 오늘의 식사")

st.markdown(f"""
    <div class="main-card">
        <h2 style="color: {bold_c}; margin-bottom: 5px;">{current_sel}</h2>
        <p style="font-size: 24px; font-weight: 800; color: #333; margin-top: 15px;">🍲 {menu_data[current_sel][0]}</p>
        <p style="font-size: 16px; color: #666; margin-top: 15px; line-height: 1.6;">
            {' / '.join(menu_data[current_sel][1:])}
        </p>
    </div>
""", unsafe_allow_html=True)

# 5. 하단 버튼 (중앙 정렬)
cols = st.columns([1,1,1,1,1]) # 동일 비율
meals = ["조식", "간편식", "중식", "석식", "야식"]

for i, meal in enumerate(meals):
    is_active = (meal == current_sel)
    m_color = color_theme[meal]["idx"]
    
    st.markdown(f"""
        <style>
        button[key="btn_{meal}"] {{
            background-color: {m_color} !important;
            opacity: {1.0 if is_active else 0.4} !important;
            box-shadow: {"0 4px 10px rgba(0,0,0,0.1)" if is_active else "none"} !important;
        }}
        </style>
    """, unsafe_allow_html=True)
    
    with cols[i]:
        st.button(meal, key=f"btn_{meal}", on_click=update_meal, args=(meal,))
