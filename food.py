import streamlit as st
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="오늘의 식사", layout="centered")

# 2. 식단 데이터
menu_data = {
    "2026-03-17(화)": {
        "조식": ["제철미나리쭈꾸미연포탕", "매운두부찜", "모둠장아찌", "누룽지"],
        "간편식": ["고로케양배추샌드위치", "삶은계란", "플레인요거트"],
        "중식": ["버섯불고기", "우엉채레몬튀김", "수수기장밥", "얼큰어묵탕", "수정과"],
        "석식": ["양배추멘치카츠", "가쓰오장국", "시저드레싱샐러드", "열무김치"],
        "야식": ["소고기미역죽", "돈육장조림", "블루베리요플레"]
    }
}

# 3. 세션 상태 초기화
if 'selected_meal' not in st.session_state:
    st.session_state.selected_meal = "중식"

# 4. 컬러 맵
color_map = {
    "조식": ("#E95444", "#FFF5F4"),
    "간편식": ("#F1A33B", "#FFF9F0"),
    "중식": ("#8BC34A", "#F9FBF2"),
    "석식": ("#4A90E2", "#F0F7FF"),
    "야식": ("#673AB7", "#F7F2FF")
}
bold_c, soft_c = color_map[st.session_state.selected_meal]

# 5. 초강력 밀림 방지 CSS (테이블 레이아웃 고정)
st.markdown(f"""
    <style>
    /* 여백 최소화 */
    .block-container {{ padding: 10px !important; }}
    
    /* 타이틀 스타일 */
    .app-header {{ font-size: 1.2rem; font-weight: bold; margin-bottom: 8px; }}

    /* 테이블 레이아웃: 카드와 버튼을 강제로 한 줄에 고정 */
    .fixed-layout {{
        display: table;
        width: 100%;
        border-spacing: 0;
        border-collapse: collapse;
    }}
    .card-cell {{
        display: table-cell;
        width: 82%;
        background-color: {soft_c};
        border: 2.5px solid {bold_c};
        border-radius: 15px 0 0 15px;
        height: 340px;
        vertical-align: middle;
        text-align: center;
        padding: 20px;
    }}
    .index-cell {{
        display: table-cell;
        width: 18%;
        vertical-align: top;
    }}

    /* 버튼 스타일 오버라이드 */
    .stButton button {{
        width: 100% !important;
        height: 68px !important; /* 340px / 5개 */
        writing-mode: vertical-rl !important;
        text-orientation: upright !important;
        color: white !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 0 10px 10px 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        font-size: 13px !important;
        line-height: 1 !important;
    }}
    </style>
""", unsafe_allow_html=True)

# 6. 화면 상단 (타이틀 및 날짜)
st.markdown('<div class="app-header">🍴 오늘의 식사</div>', unsafe_allow_html=True)
selected_date = st.selectbox("날짜", list(menu_data.keys()), label_visibility="collapsed")

# 7. 물리적 고정 레이아웃 (HTML + Streamlit Button)
menu = menu_data[selected_date].get(st.session_state.selected_meal, ["정보 없음"])

# 카드 부분 (HTML)
st.markdown(f"""
    <div class="fixed-layout">
        <div class="card-cell">
            <h2 style="color: {bold_c}; font-size: 20px; margin: 0;">{st.session_state.selected_meal}</h2>
            <div style="height: 1.5px; background-color: {bold_c}; opacity: 0.2; margin: 15px 0;"></div>
            <p style="font-size: 22px; font-weight: bold; color: #333; margin-bottom: 10px;">{menu[0]}</p>
            <p style="font-size: 15px; color: #666; line-height: 1.6;">{' / '.join(menu[1:])}</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# 인덱스 부분 (Streamlit 버튼을 카드 바로 우측에 배치)
# absolute 포지션을 이용해 카드 옆에 강제로 붙입니다.
for i, label in enumerate(["조식", "간편식", "중식", "석식", "야식"]):
    b_color, _ = color_map[label]
    top_pos = 108 + (i * 68) # 타이틀/날짜박스 높이에 맞춰 시작 지점 조정
    
    st.markdown(f"""
        <style>
        div[data-testid="stVerticalBlock"] > div:nth-child({i+4}) button {{
            position: fixed !important;
            right: 10px !important;
            top: {top_pos}px !important;
            background-color: {b_color} !important;
            z-index: 1000;
            width: 50px !important;
        }}
        </style>
    """, unsafe_allow_html=True)
    
    if st.button(label, key=f"tab_{label}"):
        st.session_state.selected_meal = label
        st.rerun()
