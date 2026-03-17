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

# 3. CSS: 가로 일렬 강제 정렬 (Flexbox)
st.markdown(f"""
<style>
    /* 메인 컨테이너 여백 최적화 */
    .main .block-container {{
        padding: 10px 10px 100px 10px !important;
        max-width: 500px !important;
    }}

    /* 식단 카드 스타일 */
    .main-card {{
        background-color: {soft_bg};
        border: 2px solid {bold_c};
        border-radius: 20px;
        padding: 30px 15px;
        text-align: center;
        margin-bottom: 20px;
    }}

    /* ★ 가로 한 줄 강제 정렬 핵심 ★ */
    div[data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important; /* 줄바꿈 절대 금지 */
        justify-content: space-between !important;
        gap: 4px !important;
    }}

    /* 버튼 스타일 조정 (글자 크기 및 여백) */
    button[key^="btn_"] {{
        flex: 1 !important; /* 모든 버튼이 동일한 폭 점유 */
        padding: 10px 0 !important;
        font-size: 13px !important;
        border: none !important;
        color: white !important;
        border-radius: 8px !important;
        min-width: 0 !important; /* 폭 축소 허용 */
        white-space: nowrap !important; /* 텍스트 줄바꿈 방지 */
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

# 5. 하단 버튼 배치
cols = st.columns(5)
meals = ["조식", "간편식", "중식", "석식", "야식"]

for i, meal in enumerate(meals):
    is_active = (meal == current_sel)
    m_color = color_theme[meal]["idx"]
    
    st.markdown(f"""
        <style>
        button[key="btn_{meal}"] {{
            background-color: {m_color} !important;
            opacity: {1.0 if is_active else 0.4} !important;
            box-shadow: {"0 4px 8px rgba(0,0,0,0.2)" if is_active else "none"} !important;
        }}
        </style>
    """, unsafe_allow_html=True)
    
    with cols[i]:
        st.button(meal, key=f"btn_{meal}", on_click=update_meal, args=(meal,))
