import streamlit as st
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="오늘의 식사", layout="centered")

# 2. 데이터 (날짜와 메뉴)
menu_data = {
    "2026-03-17(화)": {
        "조식": ["제철미나리쭈꾸미연포탕", "매운두부찜", "모둠장아찌", "누룽지"],
        "간편식": ["고로케양배추샌드위치", "삶은계란", "플레인요거트"],
        "중식": ["버섯불고기", "우엉채레몬튀김", "수수기장밥", "얼큰어묵탕", "수정과"],
        "석식": ["양배추멘치카츠", "가쓰오장국", "시저드레싱샐러드", "열무김치"],
        "야식": ["소고기미역죽", "돈육장조림", "블루베리요플레"]
    }
}

# 3. 컬러 구성 (가이드북 인덱스 컨셉)
color_map = {
    "조식": ("#E95444", "#FFF5F4"),
    "간편식": ("#F1A33B", "#FFF9F0"),
    "중식": ("#8BC34A", "#F9FBF2"),
    "석식": ("#4A90E2", "#F0F7FF"),
    "야식": ("#673AB7", "#F7F2FF")
}

if 'selected_meal' not in st.session_state:
    st.session_state.selected_meal = "중식"

bold_c, soft_c = color_map[st.session_state.selected_meal]

# 4. [핵심] 모바일 밀림 및 사라짐 방지 CSS
st.markdown(f"""
    <style>
    /* 상단 타이틀 여백 최소화 */
    .block-container {{
        padding-top: 10px !important;
        padding-right: 65px !important; /* 인덱스 버튼 공간 확보 */
        padding-left: 10px !important;
    }}
    
    /* 제목 스타일 */
    .app-title {{
        font-size: 1.1rem;
        font-weight: bold;
        margin-bottom: 5px;
    }}

    /* 메인 카드: 인덱스와 밀착되도록 조정 */
    .main-card-ui {{
        background-color: {soft_c};
        height: 320px;
        border: 2px solid {bold_c};
        border-radius: 12px 0 0 12px;
        padding: 15px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-align: center;
        margin-top: 5px;
    }}

    /* 인덱스 버튼을 화면 우측에 강제 고정 */
    .stButton button {{
        position: fixed;
        right: 5px;
        width: 50px !important;
        height: 65px !important;
        writing-mode: vertical-rl !important;
        text-orientation: upright !important;
        color: white !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 0 8px 8px 0 !important;
        z-index: 1000;
        padding: 0 !important;
        font-size: 13px !important;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }}
    </style>
""", unsafe_allow_html=True)

# 5. 화면 상단 구성
st.markdown('<div class="app-title">🍴 오늘의 식사</div>', unsafe_allow_html=True)
selected_date = st.selectbox("날짜", list(menu_data.keys()), label_visibility="collapsed")

# 6. 메인 콘텐츠 (카드)
menu = menu_data[selected_date].get(st.session_state.selected_meal, ["정보 없음"])
st.markdown(f"""
    <div class="main-card-ui">
        <h2 style="color: {bold_c}; font-size: 20px; margin: 0;">{st.session_state.selected_meal}</h2>
        <div style="height: 1px; background-color: {bold_c}; opacity: 0.2; margin: 10px 0;"></div>
        <p style="font-size: 20px; font-weight: bold; color: #333; margin-bottom: 8px;">{menu[0]}</p>
        <p style="font-size: 14px; color: #666; line-height: 1.5;">{' / '.join(menu[1:])}</p>
    </div>
""", unsafe_allow_html=True)

# 7. 우측 고정 인덱스 (절대 아래로 밀리지 않음)
meals = ["조식", "간편식", "중식", "석식", "야식"]
for i, label in enumerate(meals):
    b_color, _ = color_map[label]
    top_pos = 110 + (i * 67) # 상단에서부터의 간격 조절
    
    # 각 버튼의 위치와 색상을 개별적으로 고정
    st.markdown(f"""
        <style>
        div[data-testid="stVerticalBlock"] > div:nth-child({i+4}) button {{
            top: {top_pos}px !important;
            background-color: {b_color} !important;
        }}
        </style>
    """, unsafe_allow_html=True)
    
    if st.button(label, key=f"fixed_{label}"):
        st.session_state.selected_meal = label
        st.rerun()
