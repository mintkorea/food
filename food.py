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

# 3. CSS: 진정한 플로팅 레이아웃 (본문과 완전 분리)
st.markdown(f"""
<style>
    /* 메인 컨테이너 여백 (플로팅 버튼 자리를 미리 비워둠) */
    .main .block-container {{
        padding-right: 80px !important;
        max-width: 500px !important; /* 모바일 가독성 최적화 */
    }}

    /* 플로팅 버튼들을 감싸는 박스 - 화면 우측 중앙 고정 */
    div.floating-nav {{
        position: fixed;
        right: 0px;
        top: 50%;
        transform: translateY(-50%);
        display: flex;
        flex-direction: column;
        z-index: 100000;
    }}

    /* 각 버튼의 부모 div 스타일 */
    div.floating-nav > div {{
        margin-bottom: 2px;
    }}

    /* 실제 Streamlit 버튼 스타일 강제 오버라이드 */
    button[key^="btn_"] {{
        writing-mode: vertical-rl !important;
        text-orientation: upright !important;
        height: 80px !important;
        width: 45px !important;
        min-width: 45px !important;
        border-radius: 15px 0 0 15px !important;
        border: none !important;
        color: white !important;
        font-weight: bold !important;
        padding: 0 !important;
        font-size: 14px !important;
        line-height: 1 !important;
        box-shadow: -2px 2px 8px rgba(0,0,0,0.15) !important;
    }}
</style>
""", unsafe_allow_html=True)

# 4. 메인 콘텐츠 (카드형 식단표)
st.title("🍴 스마트 식단 가이드")

st.markdown(f"""
    <div style="
        background-color: {soft_bg};
        border: 2px solid {bold_c};
        border-radius: 20px;
        padding: 30px 20px;
        text-align: center;
        min-height: 350px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
    ">
        <h2 style="color: {bold_c}; margin-bottom: 5px;">{current_sel}</h2>
        <p style="font-size: 13px; color: #999; margin-bottom: 25px;">2026-03-17(화)</p>
        <p style="font-size: 24px; font-weight: 800; color: #333;">🍲 {menu_data[current_sel][0]}</p>
        <p style="font-size: 16px; color: #666; margin-top: 20px; line-height: 1.8;">
            {' / '.join(menu_data[current_sel][1:])}
        </p>
    </div>
""", unsafe_allow_html=True)

# 5. 플로팅 버튼 영역 (핵심: 컨테이너를 사용하여 묶어줌)
# empty()를 사용해 레이아웃 하단에 배치해도 CSS로 상단 고정
floating_container = st.container()
with floating_container:
    # 이 div 클래스가 CSS fixed의 타겟이 됨
    st.markdown('<div class="floating-nav">', unsafe_allow_html=True)
    for meal in ["조식", "간편식", "중식", "석식", "야식"]:
        is_active = (meal == current_sel)
        m_color = color_theme[meal]["idx"]
        
        # 버튼별 활성화 효과
        st.markdown(f"""
            <style>
            button[key="btn_{meal}"] {{
                background-color: {m_color} !important;
                opacity: {1.0 if is_active else 0.4} !important;
                transform: {"scaleX(1.1)" if is_active else "none"} !important;
            }}
            </style>
        """, unsafe_allow_html=True)
        
        st.button(meal, key=f"btn_{meal}", on_click=update_meal, args=(meal,))
    st.markdown('</div>', unsafe_allow_html=True)
