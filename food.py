import streamlit as st
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="오늘의 식사", layout="centered")

# 2. 데이터
menu_data = {
    "2026-03-17(화)": {
        "조식": ["제철미나리쭈꾸미연포탕", "매운두부찜", "모둠장아찌", "누룽지"],
        "간편식": ["고로케양배추샌드위치", "삶은계란", "플레인요거트"],
        "중식": ["버섯불고기", "우엉채레몬튀김", "수수기장밥", "얼큰어묵탕", "수정과"],
        "석식": ["양배추멘치카츠", "가쓰오장국", "시저드레싱샐러드", "열무김치"],
        "야식": ["소고기미역죽", "돈육장조림", "블루베리요플레"]
    }
}

# 3. 컬러 구성
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

# 4. 여백 제로 및 초밀착 CSS
st.markdown(f"""
    <style>
    /* 1. 기본 브라우저 여백 완전히 제거 */
    .block-container {{
        padding-top: 10px !important;
        padding-right: 10px !important;
        padding-left: 10px !important;
        max-width: 100% !important;
    }}
    
    /* 2. 타이틀 및 날짜 선택기 콤팩트화 */
    .header-text {{ font-size: 1.1rem; font-weight: bold; margin-bottom: 5px; color: #333; }}
    
    /* 3. 인덱스와 카드를 묶는 컨테이너 (Flexbox) */
    .guide-wrapper {{
        display: flex;
        width: 100%;
        height: 350px; /* 전체 높이 고정 */
        margin-top: 5px;
    }}

    /* 4. 메인 카드 디자인 */
    .main-card-body {{
        flex: 1;
        background-color: {soft_c};
        border: 2px solid {bold_c};
        border-radius: 12px 0 0 12px;
        padding: 10px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-align: center;
    }}

    /* 5. 인덱스 탭 영역 (Streamlit 버튼 스타일 강제 오버라이드) */
    div[data-testid="column"] {{
        padding: 0px !important;
        margin: 0px !important;
    }}
    
    .stButton button {{
        width: 45px !important;
        height: 69px !important; /* 350px / 5개 = 약 70px */
        writing-mode: vertical-rl !important;
        text-orientation: upright !important;
        color: white !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 0 10px 10px 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        font-size: 12px !important;
        line-height: 1 !important;
        box-shadow: none !important;
    }}
    </style>
""", unsafe_allow_html=True)

# 5. 화면 구성
st.markdown('<div class="header-text">🍴 오늘의 식사</div>', unsafe_allow_html=True)
selected_date = st.selectbox("날짜", list(menu_data.keys()), label_visibility="collapsed")

# 6. 핵심 레이아웃: 컬럼 간의 간격(Gap)을 제거하기 위해 좁은 비중 사용
col_card, col_tabs = st.columns([0.84, 0.16], gap="small")

with col_card:
    menu = menu_data[selected_date].get(st.session_state.selected_meal, ["정보 없음"])
    st.markdown(f"""
        <div class="main-card-body">
            <h2 style="color: {bold_c}; font-size: 18px; margin: 0;">{st.session_state.selected_meal}</h2>
            <div style="height: 1px; background-color: {bold_c}; opacity: 0.2; margin: 10px 0;"></div>
            <p style="font-size: 19px; font-weight: bold; color: #333; margin-bottom: 5px;">🍲 {menu[0]}</p>
            <p style="font-size: 13px; color: #666; line-height: 1.4;">{' / '.join(menu[1:])}</p>
        </div>
    """, unsafe_allow_html=True)

with col_tabs:
    # 버튼 사이의 여백을 없애기 위해 CSS로 개별 위치 조정 없이 순차 배치
    for label in ["조식", "간편식", "중식", "석식", "야식"]:
        b_color, _ = color_map[label]
        # 실시간 색상 및 틈새 제거 적용
        st.markdown(f"""
            <style>
            button[key="tab_{label}"] {{
                background-color: {b_color} !important;
                margin-top: -1px !important; /* 버튼 사이 실선 겹침으로 틈새 제거 */
            }}
            </style>
        """, unsafe_allow_html=True)
        
        if st.button(label, key=f"tab_{label}"):
            st.session_state.selected_meal = label
            st.rerun()
