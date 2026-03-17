import streamlit as st

# 1. 색상 테마 (인덱스: 선명 / 카드배경: 파스텔)
color_theme = {
    "조식": {"idx": "#E95444", "bg": "#F9EBEA"},
    "간편식": {"idx": "#F1A33B", "bg": "#FEF5E7"},
    "중식": {"idx": "#8BC34A", "bg": "#F1F8E9"},
    "석식": {"idx": "#4A90E2", "bg": "#EBF5FB"},
    "야식": {"idx": "#673AB7", "bg": "#F4ECF7"}
}

# 2. 식단 데이터 (예시: 3/17 화요일 데이터)
menu_data = {
    "조식": ["제철미나리쭈꾸미연포탕", "매운두부찜", "흰쌀밥", "모둠장아찌", "누룽지"],
    "간편식": ["고로케양배추샌드위치", "삶은계란", "플레인요거트"],
    "중식": ["버섯불고기", "우엉채레몬튀김", "수수기장밥", "얼큰어묵탕", "수정과"],
    "석식": ["양배추멘치카츠", "가쓰오장국", "시저드레싱샐러드", "열무김치"],
    "야식": ["소고기미역죽", "돈육장조림", "깍두기", "블루베리요플레"]
}

# 3. 세션 상태 초기화 (메뉴 선택 유지의 핵심)
if 'current_meal' not in st.session_state:
    st.session_state.current_meal = "중식"

# 4. CSS: 인덱스 고정 및 테마 적용
sel_meal = st.session_state.current_meal
bold_c = color_theme[sel_meal]["idx"]
soft_bg = color_theme[sel_meal]["bg"]

st.markdown(f"""
<style>
    /* 메인 카드 스타일 */
    .main-card {{
        background-color: {soft_bg};
        border: 2px solid {bold_c};
        border-radius: 15px 0 0 15px;
        padding: 30px 15px;
        margin-right: 50px; /* 인덱스 버튼 공간 */
        min-height: 350px;
        text-align: center;
        transition: all 0.3s ease;
    }}
    
    /* 우측 고정 인덱스 컨테이너 */
    .fixed-nav {{
        position: fixed;
        right: 10px;
        top: 55%;
        transform: translateY(-50%);
        display: flex;
        flex-direction: column;
        gap: 2px;
        z-index: 1000;
    }}
</style>
""", unsafe_allow_html=True)

# 5. UI 렌더링
st.title("🍴 오늘의 식사")
st.selectbox("날짜 선택", ["2026-03-17(화)"], label_visibility="collapsed")

# 카드와 버튼 레이아웃
col_content, col_nav = st.columns([8.5, 1.5])

with col_content:
    menu = menu_data.get(sel_meal, ["정보 없음"])
    st.markdown(f"""
        <div class="main-card">
            <h2 style="color: {bold_c}; margin-bottom: 20px;">{sel_meal}</h2>
            <p style="font-size: 22px; font-weight: bold; color: #333;">🍲 {menu[0]}</p>
            <p style="font-size: 16px; color: #666; margin-top: 15px; line-height: 1.6;">
                {' / '.join(menu[1:])}
            </p>
        </div>
    """, unsafe_allow_html=True)

# 6. 고정 인덱스 버튼 (선택 로직 보정)
with col_nav:
    st.markdown('<div class="fixed-nav">', unsafe_allow_html=True)
    for meal in ["조식", "간편식", "중식", "석식", "야식"]:
        # 버튼 스타일 동적 생성
        m_color = color_theme[meal]["idx"]
        is_selected = (meal == sel_meal)
        
        st.markdown(f"""
            <style>
            button[key="btn_{meal}"] {{
                background-color: {m_color} !important;
                opacity: {1.0 if is_selected else 0.5};
                color: white !important;
                writing-mode: vertical-rl;
                text-orientation: upright;
                height: 80px !important;
                width: 45px !important;
                border-radius: 0 10px 10px 0 !important;
                border: none !important;
                font-weight: bold !important;
                box-shadow: {"2px 2px 8px rgba(0,0,0,0.2)" if is_selected else "none"};
            }}
            </style>
        """, unsafe_allow_html=True)
        
        if st.button(meal, key=f"btn_{meal}"):
            st.session_state.current_meal = meal
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
