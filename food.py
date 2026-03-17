import streamlit as st
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="오늘의 식사", layout="centered")

# 2. 데이터 (이미지 분석 결과 반영)
menu_data = {
    "2026-03-17(화)": {
        "조식": ["제철미나리쭈꾸미연포탕", "매운두부찜", "모둠장아찌", "누룽지"],
        "간편식": ["고로케양배추샌드위치", "삶은계란", "플레인요거트"],
        "중식": ["버섯불고기", "우엉채레몬튀김", "수수기장밥", "얼큰어묵탕", "수정과"],
        "석식": ["양배추멘치카츠", "가쓰오장국", "시저드레싱샐러드", "열무김치"],
        "야식": ["소고기미역죽", "돈육장조림", "블루베리요플레"]
    }
}

# 3. 컬러 맵
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

# 4. 상단 밀착 및 콤팩트 디자인 CSS
st.markdown(f"""
    <style>
    /* 상단 여백 제거 및 전체 배경 설정 */
    .stApp {{ background-color: #FFFFFF; }}
    .block-container {{
        padding-top: 0rem !important;
        padding-right: 60px !important;
        padding-left: 10px !important;
    }}
    
    /* 타이틀 및 날짜 선택 영역 콤팩트화 */
    .header-area {{
        padding-top: 10px;
        padding-bottom: 5px;
    }}
    .header-area h3 {{
        margin-bottom: 0px;
        font-size: 1.2rem;
        color: #333;
    }}

    /* 메인 카드: 크기와 여백 대폭 축소 */
    .main-card {{
        background-color: {soft_c};
        height: 380px; /* 카드 크기 축소 */
        border: 2px solid {bold_c};
        border-radius: 12px 0 0 12px;
        padding: 15px; /* 내부 여백 축소 */
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-align: center;
        margin-top: 5px;
    }}

    /* 인덱스 버튼: 카드와 벌어지지 않게 고정 */
    .stButton button {{
        position: fixed;
        right: 0px; /* 오른쪽 끝에 밀착 */
        width: 50px !important;
        height: 75px !important; /* 인덱스 높이 축소 */
        writing-mode: vertical-rl !important;
        text-orientation: upright !important;
        color: white !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 0 8px 8px 0 !important;
        z-index: 9999;
        padding: 0 !important;
        font-size: 13px !important;
    }}
    </style>
""", unsafe_allow_html=True)

# 5. 상단 구성 (타이틀 및 날짜)
st.markdown('<div class="header-area"><h3>🍴 오늘의 식사</h3></div>', unsafe_allow_html=True)
selected_date = st.selectbox("날짜", list(menu_data.keys()), label_visibility="collapsed")

# 6. 메인 카드 출력
menu = menu_data[selected_date].get(st.session_state.selected_meal, ["정보 없음"])
st.markdown(f"""
    <div class="main-card">
        <h2 style="color: {bold_c}; font-size: 22px; margin: 0;">{st.session_state.selected_meal}</h2>
        <div style="height: 1px; background-color: {bold_c}; opacity: 0.2; margin: 12px 0;"></div>
        <p style="font-size: 20px; font-weight: bold; color: #333; margin-bottom: 10px;">{menu[0]}</p>
        <p style="font-size: 15px; color: #666; line-height: 1.6;">{' / '.join(menu[1:])}</p>
    </div>
""", unsafe_allow_html=True)

# 7. 우측 밀착 인덱스 버튼 (상단부터 배치)
meals = ["조식", "간편식", "중식", "석식", "야식"]
for i, label in enumerate(meals):
    b_color, _ = color_map[label]
    # 타이틀과 날짜 선택 영역 아래부터 인덱스 시작 (위치 조정)
    top_pos = 105 + (i * 77) 
    
    st.markdown(f"""
        <style>
        div[data-testid="stVerticalBlock"] > div:nth-child({i+4}) button {{
            top: {top_pos}px !important;
            background-color: {b_color} !important;
        }}
        </style>
    """, unsafe_allow_html=True)
    
    if st.button(label, key=f"tab_{label}"):
        st.session_state.selected_meal = label
        st.rerun()
