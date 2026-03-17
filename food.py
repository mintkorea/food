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

# 3. CSS: 하단 가로 버튼 및 카드 디자인
st.markdown(f"""
<style>
    /* 메인 컨테이너 너비 제한 */
    .main .block-container {{
        max-width: 450px !important;
        padding: 20px 15px !important;
    }}

    /* 식단 카드 스타일 */
    .main-card {{
        background-color: {soft_bg};
        border: 2px solid {bold_c};
        border-radius: 20px;
        padding: 40px 20px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }}

    /* 가로 버튼 컨테이너 */
    div[data-testid="stHorizontalBlock"] {{
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 15px;
        gap: 5px !important;
    }}

    /* 버튼 공통 스타일 */
    button[key^="btn_"] {{
        width: 100% !important;
        border: none !important;
        padding: 10px 0 !important;
        font-weight: bold !important;
        font-size: 14px !important;
        border-radius: 10px !important;
        color: white !important;
        transition: all 0.2s ease;
    }}
</style>
""", unsafe_allow_html=True)

# 4. 메인 UI 구성
st.title("🍴 오늘의 식단")

# 식단 카드 표시
st.markdown(f"""
    <div class="main-card">
        <h2 style="color: {bold_c}; margin-bottom: 5px;">{current_sel}</h2>
        <p style="font-size: 13px; color: #999; margin-bottom: 20px;">2026-03-17(화)</p>
        <p style="font-size: 24px; font-weight: 800; color: #333;">🍲 {menu_data[current_sel][0]}</p>
        <p style="font-size: 16px; color: #666; margin-top: 20px; line-height: 1.8;">
            {' / '.join(menu_data[current_sel][1:])}
        </p>
    </div>
""", unsafe_allow_html=True)

# 5. 하단 가로 일렬 버튼 (5컬럼 레이아웃)
cols = st.columns(5)
meals = ["조식", "간편식", "중식", "석식", "야식"]

for i, meal in enumerate(meals):
    is_active = (meal == current_sel)
    m_color = color_theme[meal]["idx"]
    
    # 버튼별 개별 스타일 적용
    st.markdown(f"""
        <style>
        button[key="btn_{meal}"] {{
            background-color: {m_color} !important;
            opacity: {1.0 if is_active else 0.3} !important;
            transform: {"scale(1.05)" if is_active else "scale(1.0)"};
            box-shadow: {"0 4px 8px rgba(0,0,0,0.2)" if is_active else "none"} !important;
        }}
        </style>
    """, unsafe_allow_html=True)
    
    cols[i].button(meal, key=f"btn_{meal}", on_click=update_meal, args=(meal,))
