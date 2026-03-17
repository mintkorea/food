import streamlit as st
from datetime import datetime

# 1. 페이지 설정 (사이드바 기본 상태 조절)
st.set_page_config(
    page_title="식단 가이드", 
    layout="centered", 
    initial_sidebar_state="expanded" # 사이드바 항상 열림
)

# 2. 데이터 (전체 일주일치)
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

# 4. 사이드바를 '우측 인덱스'로 탈바꿈하는 CSS
# Streamlit의 사이드바는 기본이 왼쪽이므로 이를 오른쪽으로 옮기고 너비를 줄입니다.
st.markdown("""
    <style>
    /* 사이드바를 오른쪽으로 이동 */
    [data-testid="stSidebar"] {
        position: fixed;
        right: 0;
        left: auto;
        width: 70px !important; /* 인덱스 너비만큼만 */
        min-width: 70px !important;
        background-color: #F8F9FA;
        border-left: 1px solid #ddd;
    }
    /* 메인 컨텐츠 영역 여백 조정 */
    [data-testid="stSidebarNav"] { display: none; } /* 네비게이션 숨김 */
    section[data-testid="stSidebar"] > div { width: 70px; padding-top: 2rem; }
    
    /* 사이드바 내 버튼을 세로 인덱스처럼 */
    .stButton button {
        height: 100px !important;
        width: 50px !important;
        writing-mode: vertical-rl !important;
        text-orientation: upright !important;
        margin-left: -5px;
        border: none !important;
        color: white !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

# 5. 사이드바(인덱스 프레임) 구성
with st.sidebar:
    for label in ["조식", "간편식", "중식", "석식", "야식"]:
        b_color, _ = color_map[label]
        if st.button(label, key=f"side_{label}"):
            st.session_state.selected_meal = label
            st.rerun()
        
        # 버튼 색상 강제 주입
        st.markdown(f"""
            <style>
            div[data-testid="stSidebar"] button[key="side_{label}"] {{
                background-color: {b_color} !important;
                margin-bottom: 5px;
            }}
            </style>
        """, unsafe_allow_html=True)

# 6. 메인 화면(카드 프레임) 구성
if 'selected_meal' not in st.session_state:
    st.session_state.selected_meal = "중식"

bold_c, soft_c = color_map[st.session_state.selected_meal]

st.title("📖 주간 식단 가이드")
selected_date = st.selectbox("날짜", list(menu_data.keys()), label_visibility="collapsed")

# 카드 디자인
menu = menu_data[selected_date].get(st.session_state.selected_meal, ["정보 없음"])
st.markdown(f"""
    <div style="background-color: {soft_c}; padding: 30px; border-radius: 20px; 
                border: 2px solid {bold_c}; text-align: center; height: 500px;
                display: flex; flex-direction: column; justify-content: center;
                box-shadow: -5px 5px 15px rgba(0,0,0,0.05);">
        <h1 style="color: {bold_c};">{st.session_state.selected_meal}</h1>
        <hr style="border: 0.5px solid {bold_c}; opacity: 0.2; margin: 20px 0;">
        <p style="font-size: 26px; font-weight: bold; color: #333;">🍲 {menu[0]}</p>
        <p style="font-size: 18px; color: #666; line-height: 2.0;">{' / '.join(menu[1:])}</p>
    </div>
""", unsafe_allow_html=True)
