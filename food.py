import streamlit as st
from datetime import datetime

# 1. 데이터 (전체 일주일치로 확장 가능)
# 업데이트 자체를 자동화하는 방식 (이미지 → JSON)을 활용하면 편리합니다.
menu_data = {
    "2026-03-17(화)": {
        "조식": ["제철미나리쭈꾸미연포탕", "매운두부찜", "흰쌀밥", "모둠장아찌", "누룽지"],
        "간편식": ["고로케양배추샌드위치", "삶은계란", "플레인요거트"],
        "중식": ["버섯불고기", "우엉채레몬튀김", "수수기장밥", "얼큰어묵탕", "수정과"],
        "석식": ["양배추멘치카츠", "흰쌀밥", "가쓰오장국", "시저드레싱샐러드", "열무김치"],
        "야식": ["소고기미역죽", "돈육장조림", "깍두기", "블루베리요플레"]
    }
}

# 2. 초기 세팅
if 'selected_meal' not in st.session_state:
    st.session_state.selected_meal = "중식" # 테스트용 초기값

# 3. CSS 적용 (모바일 한 화면 구성 및 인덱스 스타일)
st.markdown("""
    <style>
    /* 전체 배경 정리 */
    .stApp { background-color: #F0F2F5; }
    .block-container { padding-top: 1rem; padding-bottom: 0rem; }
    
    /* 인덱스 버튼 스타일 */
    .stButton > button {
        width: 100%; 
        border-radius: 5px; 
        height: 4em; 
        font-weight: bold;
        color: white !important;
        margin-bottom: 2px;
    }
    
    /* 식사별 컬러 매칭 */
    div[data-testid="stVerticalBlock"] > div:nth-child(1) button { background-color: #ff9800; } 
    div[data-testid="stVerticalBlock"] > div:nth-child(2) button { background-color: #fbc02d; color: black !important; } 
    div[data-testid="stVerticalBlock"] > div:nth-child(3) button { background-color: #8bc34a; } 
    div[data-testid="stVerticalBlock"] > div:nth-child(4) button { background-color: #3f51b5; } 
    div[data-testid="stVerticalBlock"] > div:nth-child(5) button { background-color: #9c27b0; }

    /* 메인 카드 스타일 */
    .selected-card {
        background-color: #ffffff;
        padding: 25px;
        border: 2px solid #ff4b4b;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-top: -10px;
    }
    </style>
""", unsafe_allow_html=True)

# 4. 화면 구성
st.title("🗂️ 스마트 식단 가이드")

# [프레임 1] 글로벌 컨트롤: 날짜 선택
selected_date = st.selectbox("날짜 선택", list(menu_data.keys()), label_visibility="collapsed")

# 레이아웃: 메인 카드(8) : 인덱스 탭(2) 비율
col_card, col_tab = st.columns([8, 2])

# [프레임 2] 중앙 상세 식단: 메인 카드 출력
with col_card:
    menu = menu_data[selected_date].get(st.session_state.selected_meal, ["정보 없음"])
    st.markdown(f"""
        <div class="selected-card">
            <h1 style="color: #333; font-size: 26px; margin-bottom: 5px;">{st.session_state.selected_meal}</h1>
            <div style="height: 1px; background-color: #EEE; margin: 15px 0;"></div>
            <p style="font-size: 22px; font-weight: bold; color: #ff4b4b;">🍲 {menu[0]}</p>
            <p style="font-size: 16px; color: #666; line-height: 1.8;">{' / '.join(menu[1:])}</p>
        </div>
    """, unsafe_allow_html=True)

# [프레임 3] 우측 인덱스 탭: 식사 시간 변경 버튼
with col_tab:
    for label in ["조식", "간편식", "중식", "석식", "야식"]:
        if st.button(label, key=label):
            st.session_state.selected_meal = label
            st.rerun() # 세션 상태 업데이트 후 화면 리로드

st.caption("💡 오른쪽 인덱스를 터치하여 식사 시간을 변경하세요.")
