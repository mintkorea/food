import streamlit as st
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="오늘의 식사", layout="centered")

# 2. 이번 주 전체 데이터 (이미지 기반 정리)
menu_data = {
    "2026-03-17(화)": {
        "조식": ["제철미나리쭈꾸미연포탕", "매운두부찜", "모둠장아찌", "누룽지"],
        "간편식": ["고로케양배추샌드위치", "삶은계란", "플레인요거트"],
        "중식": ["버섯불고기", "우엉채레몬튀김", "수수기장밥", "얼큰어묵탕", "수정과"],
        "석식": ["양배추멘치카츠", "가쓰오장국", "시저드레싱샐러드", "열무김치"],
        "야식": ["소고기미역죽", "돈육장조림", "블루베리요플레"]
    }
}

# 3. 컬러 구성 (가이드북 느낌)
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

# 4. 상단 밀착 및 인덱스 고정 CSS
st.markdown(f"""
    <style>
    /* 전체 여백 제거 */
    .stApp {{ background-color: #FFFFFF; }}
    .block-container {{
        padding-top: 0.5rem !important;
        padding-right: 55px !important; /* 인덱스 공간 */
        padding-left: 10px !important;
    }}
    
    /* 헤더 영역 */
    .header-text {{
        font-size: 1.1rem;
        font-weight: bold;
        margin-bottom: 5px;
        color: #333;
    }}

    /* 메인 카드: 상단 밀착 및 크기 축소 */
    .main-card {{
        background-color: {soft_c};
        height: 350px;
        border: 2px solid {bold_c};
        border-radius: 12px 0 0 12px;
        padding: 15px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-align: center;
    }}

    /* [핵심] 인덱스 버튼을 감싸는 컨테이너 강제 위치 고정 */
    [data-testid="stVerticalBlock"] > div:has(button) {{
        position: absolute !important;
        right: -55px !important; /* 카드 바로 옆에 붙임 */
        top: 0px !important;     /* 최상단 정렬 */
        display: flex !important;
        flex-direction: column !important;
        gap: 0px !important;     /* 인덱스 간 벌어짐 방지 */
    }}

    /* 인덱스 버튼 개별 스타일 */
    .stButton button {{
        width: 48px !important;
        height: 70px !important; /* 높이 콤팩트화 */
        writing-mode: vertical-rl !important;
        text-orientation: upright !important;
        color: white !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 0 8px 8px 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        font-size: 13px !important;
    }}
    </style>
""", unsafe_allow_html=True)

# 5. 화면 구성
st.markdown('<div class="header-text">🍴 오늘의 식사</div>', unsafe_allow_html=True)
selected_date = st.selectbox("날짜", list(menu_data.keys()), label_visibility="collapsed")

# 레이아웃을 위해 아주 좁은 컬럼 구성 (인덱스가 이 안에서 정렬됨)
col_content, col_idx = st.columns([0.85, 0.15])

with col_content:
    # 메인 카드
    menu = menu_data[selected_date].get(st.session_state.selected_meal, ["정보 없음"])
    st.markdown(f"""
        <div class="main-card">
            <h2 style="color: {bold_c}; font-size: 20px; margin: 0;">{st.session_state.selected_meal}</h2>
            <div style="height: 1px; background-color: {bold_c}; opacity: 0.2; margin: 10px 0;"></div>
            <p style="font-size: 19px; font-weight: bold; color: #333; margin-bottom: 8px;">{menu[0]}</p>
            <p style="font-size: 14px; color: #666; line-height: 1.6;">{' / '.join(menu[1:])}</p>
        </div>
    """, unsafe_allow_html=True)

with col_idx:
    # 인덱스 버튼들 (gap 없이 밀착)
    for label in ["조식", "간편식", "중식", "석식", "야식"]:
        b_color, _ = color_map[label]
        if st.button(label, key=f"tab_{label}"):
            st.session_state.selected_meal = label
            st.rerun()
        
        # 버튼 컬러 실시간 반영
        st.markdown(f"""
            <style>
            button[key="tab_{label}"] {{
                background-color: {b_color} !important;
            }}
            </style>
        """, unsafe_allow_html=True)
