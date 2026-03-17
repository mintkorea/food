import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="오늘의 식사", layout="centered")

# 2. 데이터 및 컬러 정의
menu_data = {
    "2026-03-17(화)": {
        "조식": ["연포탕", "매운두부찜"], "간편식": ["샌드위치", "요거트"],
        "중식": ["버섯불고기", "우엉채레몬튀김", "수수기장밥", "얼큰어묵탕", "수정과"],
        "석식": ["멘치카츠", "가쓰오장국"], "야식": ["소고기미역죽"]
    }
}
color_map = {
    "조식": ("#E95444", "#FFF5F4"), "간편식": ("#F1A33B", "#FFF9F0"),
    "중식": ("#8BC34A", "#F9FBF2"), "석식": ("#4A90E2", "#F0F7FF"), "야식": ("#673AB7", "#F7F2FF")
}

if 'selected_meal' not in st.session_state:
    st.session_state.selected_meal = "중식"

# 3. CSS 수정: 실제 버튼을 인덱스 탭처럼 디자인
bold_c, soft_c = color_map[st.session_state.selected_meal]

st.markdown(f"""
    <style>
    /* 전체 레이아웃 정렬 */
    [data-testid="stHorizontalBlock"] {{
        gap: 0px !important;
    }}
    
    /* 카드 본체 디자인 */
    .menu-card {{
        background-color: {soft_c};
        border: 3px solid {bold_c};
        border-right: none;
        border-radius: 20px 0 0 20px;
        padding: 30px 20px;
        text-align: center;
        height: 400px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }}

    /* 오른쪽 버튼(인덱스) 세로 정렬 및 디자인 */
    div[data-testid="stColumn"] > div > div > div > button {{
        writing-mode: vertical-rl;
        text-orientation: upright;
        height: 80px !important; /* 400px / 5개 */
        width: 45px !important;
        margin: 0 !important;
        border-radius: 0 10px 10px 0 !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        color: white !important;
        font-weight: bold !important;
        font-size: 13px !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}
    
    /* 버튼들 사이의 간격 제거 */
    div[data-testid="stVerticalBlock"] {{
        gap: 0rem !important;
    }}
    </style>
""", unsafe_allow_html=True)

# 4. 상단 날짜 선택
st.markdown("### 🍴 오늘의 식사")
selected_date = list(menu_data.keys())[0]

# 5. 메인 레이아웃 (왼쪽 카드 + 오른쪽 세로 버튼들)
col_card, col_tabs = st.columns([8, 1])

with col_card:
    menu = menu_data[selected_date].get(st.session_state.selected_meal, ["정보 없음"])
    st.markdown(f"""
        <div class="menu-card">
            <div style="color: {bold_c}; font-weight: bold; font-size: 18px; margin-bottom: 10px;">{st.session_state.selected_meal}</div>
            <div style="font-size: 24px; font-weight: bold; color: #333; margin-bottom: 20px;">{menu[0]}</div>
            <div style="font-size: 16px; color: #666; line-height: 1.8;">{' / '.join(menu[1:])}</div>
        </div>
    """, unsafe_allow_html=True)

with col_tabs:
    # 각 버튼에 배경색을 직접 입힘
    for meal in ["조식", "간편식", "중식", "석식", "야식"]:
        b_color = color_map[meal][0]
        opacity = "1.0" if meal == st.session_state.selected_meal else "0.5"
        
        # 버튼 생성 및 클릭 이벤트
        if st.button(meal, key=f"btn_{meal}"):
            st.session_state.selected_meal = meal
            st.rerun()
        
        # 생성된 버튼에 즉시 색상 입히기 (CSS 인젝션)
        st.markdown(f"""
            <style>
            button[key="btn_{meal}"] {{
                background-color: {b_color} !important;
                opacity: {opacity} !important;
            }}
            </style>
        """, unsafe_allow_html=True)
