import streamlit as st
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="식단 가이드", layout="centered")

# 2. 데이터 (이미지 기반 일주일치 요약)
menu_data = {
    "2026-03-17(화)": {
        "조식": ["제철미나리쭈꾸미연포탕", "매운두부찜", "모둠장아찌", "누룽지"],
        "간편식": ["고로케양배추샌드위치", "삶은계란", "플레인요거트"],
        "중식": ["버섯불고기", "우엉채레몬튀김", "수수기장밥", "얼큰어묵탕", "수정과"],
        "석식": ["양배추멘치카츠", "가쓰오장국", "시저드레싱샐러드", "열무김치"],
        "야식": ["소고기미역죽", "돈육장조림", "블루베리요플레"]
    }
}

# 3. 현재 시간 기반 초기값
if 'selected_meal' not in st.session_state:
    curr_hour = datetime.now().hour
    if curr_hour < 9: st.session_state.selected_meal = "조식"
    elif 11 <= curr_hour < 14: st.session_state.selected_meal = "중식"
    else: st.session_state.selected_meal = "석식"

# 4. 컬러 맵
color_map = {
    "조식": ("#E95444", "#FFF5F4"),
    "간편식": ("#F1A33B", "#FFF9F0"),
    "중식": ("#8BC34A", "#F9FBF2"),
    "석식": ("#4A90E2", "#F0F7FF"),
    "야식": ("#673AB7", "#F7F2FF")
}
bold_c, soft_c = color_map[st.session_state.selected_meal]

# 5. [핵심] 밀림 방지 CSS - 절대 위치 고정
st.markdown(f"""
    <style>
    /* 메인 컨테이너 여백 강제 확보 (우측 인덱스 자리를 미리 비움) */
    .block-container {{
        padding-right: 70px !important; 
        padding-left: 15px !important;
    }}

    /* 메인 카드 프레임 */
    .main-card {{
        background-color: {soft_c};
        height: 550px;
        border: 2px solid {bold_c};
        border-radius: 20px 0 0 20px; /* 오른쪽은 직선으로 해서 탭과 밀착 */
        padding: 25px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-align: center;
        box-shadow: -5px 5px 15px rgba(0,0,0,0.05);
    }}

    /* 버튼 스타일 오버라이드: 세로형 인덱스 */
    .stButton button {{
        position: fixed;
        right: 5px;
        width: 55px !important;
        height: 90px !important;
        writing-mode: vertical-rl !important;
        text-orientation: upright !important;
        color: white !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 0 10px 10px 0 !important;
        z-index: 9999;
        padding: 0 !important;
    }}
    </style>
""", unsafe_allow_html=True)

# 6. 화면 상단 구성
st.subheader("📖 시설관리 식단 가이드")
selected_date = st.selectbox("날짜", list(menu_data.keys()), label_visibility="collapsed")

# 7. 메인 카드 출력
menu = menu_data[selected_date].get(st.session_state.selected_meal, ["정보 없음"])
st.markdown(f"""
    <div class="main-card">
        <h2 style="color: {bold_c}; margin-bottom: 0;">{st.session_state.selected_meal}</h2>
        <div style="height: 1.5px; background-color: {bold_c}; opacity: 0.2; margin: 20px 0;"></div>
        <p style="font-size: 24px; font-weight: bold; color: #333; margin-bottom: 15px;">🍲 {menu[0]}</p>
        <p style="font-size: 16px; color: #666; line-height: 1.8;">{' / '.join(menu[1:])}</p>
    </div>
""", unsafe_allow_html=True)

# 8. 우측 인덱스 버튼 배치 (고정 위치 지정)
meals = ["조식", "간편식", "중식", "석식", "야식"]
for i, label in enumerate(meals):
    b_color, _ = color_map[label]
    top_margin = 160 + (i * 92) # 버튼 위치를 위에서부터 아래로 순차 배치
    
    # CSS로 각 버튼의 위치와 색상을 개별 고정
    st.markdown(f"""
        <style>
        div[data-testid="stVerticalBlock"] > div:nth-child({i+4}) button {{
            top: {top_margin}px !important;
            background-color: {b_color} !important;
        }}
        </style>
    """, unsafe_allow_html=True)
    
    if st.button(label, key=f"fixed_btn_{label}"):
        st.session_state.selected_meal = label
        st.rerun()
