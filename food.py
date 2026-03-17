import streamlit as st

# 1. 색상 및 식단 데이터
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

# 3. CSS: 모바일에서도 절대 밀리지 않는 우측 고정 (핵심 수정)
st.markdown(f"""
<style>
    /* 메인 카드 영역: 인덱스가 들어올 자리를 확보(margin-right) */
    .main-card {{
        background-color: {soft_bg} !important;
        border: 2.5px solid {bold_c} !important;
        border-radius: 15px 0 0 15px !important;
        padding: 30px 15px !important;
        margin-right: 48px !important; 
        min-height: 380px !important;
        text-align: center;
    }}
    
    /* 인덱스 컨테이너: 화면 우측 끝에 강제 고정 */
    .stButton {{
        position: fixed !important;
        right: 0px !important;
        z-index: 9999 !important;
    }}
    
    /* 각 버튼의 높이 위치(top)를 개별 지정하여 겹치지 않게 함 */
    #btn_조식 {{ top: 150px !important; }}
    #btn_간편식 {{ top: 232px !important; }}
    #btn_중식 {{ top: 314px !important; }}
    #btn_석식 {{ top: 396px !important; }}
    #btn_야식 {{ top: 478px !important; }}
</style>
""", unsafe_allow_html=True)

# 4. UI 렌더링
st.title("🍴 오늘의 식사")

# 메인 카드
menu = menu_data.get(current_sel, ["정보 없음"])
st.markdown(f"""
    <div class="main-card">
        <h2 style="color: {bold_c};">{current_sel}</h2>
        <hr style="border: 0.5px solid {bold_c}; opacity: 0.2;">
        <p style="font-size: 24px; font-weight: bold; color: #333; margin-top: 20px;">🍲 {menu[0]}</p>
        <p style="font-size: 16px; color: #555; line-height: 1.8;">{' / '.join(menu[1:])}</p>
    </div>
""", unsafe_allow_html=True)

# 5. 인덱스 버튼 생성 (ID를 부여하여 위치 고정)
for meal in ["조식", "간편식", "중식", "석식", "야식"]:
    m_color = color_theme[meal]["idx"]
    is_active = (meal == current_sel)
    
    st.markdown(f"""
        <style>
        div[data-testid="stButton"] > button:has(div:contains("{meal}")) {{
            background-color: {m_color} !important;
            opacity: {1.0 if is_active else 0.4} !important;
            color: white !important;
            writing-mode: vertical-rl !important;
            text-orientation: upright !important;
            height: 80px !important;
            width: 48px !important;
            border-radius: 10px 0 0 10px !important;
            border: none !important;
            padding: 0 !important;
            font-weight: bold !important;
        }}
        </style>
    """, unsafe_allow_html=True)
    
    # 각 버튼에 고유 ID를 부여할 수 없으므로 스타일 시트에서 제어하기 쉽게 구성
    st.button(meal, key=f"btn_{meal}", on_click=update_meal, args=(meal,))
