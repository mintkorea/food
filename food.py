import streamlit as st
from datetime import datetime

# 1. 일주일 전체 데이터 (업로드하신 이미지를 기반으로 보강)
menu_data = {
    "2026-03-16(월)": {
        "조식": ["두유스프", "단호박에그마요샌드", "바게트/잡곡식빵", "맛살마요범벅"],
        "간편식": ["운영 없음"],
        "중식": ["차돌해물짬뽕밥", "김말이튀김", "흑미밥", "그린샐러드", "매실주스"],
        "석식": ["어항가지돈육덮밥", "사골파국", "감자채햄볶음", "망고드레싱샐러드"],
        "야식": ["날치알볶음밥", "후랑크소시지", "참깨드레싱샐러드", "요구르트"]
    },
    "2026-03-17(화)": {
        "조식": ["제철미나리쭈꾸미연포탕", "매운두부찜", "모둠장아찌", "누룽지"],
        "간편식": ["고로케양배추샌드위치", "삶은계란", "플레인요거트"],
        "중식": ["버섯불고기", "우엉채레몬튀김", "수수기장밥", "얼큰어묵탕", "수정과"],
        "석식": ["양배추멘치카츠", "가쓰오장국", "시저드레싱샐러드", "열무김치"],
        "야식": ["소고기미역죽", "돈육장조림", "블루베리요플레"]
    },
    # 나머지 요일(수~일)도 동일한 구조로 추가 가능
}

# 2. 초기 세팅
if 'selected_meal' not in st.session_state:
    st.session_state.selected_meal = "중식"

# 식사별 선명한 인덱스 컬러 정의
colors = {
    "조식": {"bold": "#E95444", "soft": "#FDECEA"}, # 빨강
    "간편식": {"bold": "#F1A33B", "soft": "#FFF4E5"}, # 주황
    "중식": {"bold": "#8BC34A", "soft": "#F1F8E9"}, # 초록
    "석식": ["#4A90E2", "#EBF3FB"], # 파랑
    "야식": ["#673AB7", "#F3E5F5"] # 보라
}
# 딕셔너리 접근 편의를 위해 통일
color_map = {
    "조식": ("#E95444", "#FDECEA"),
    "간편식": ("#F1A33B", "#FFF4E5"),
    "중식": ("#8BC34A", "#F1F8E9"),
    "석식": ("#4A90E2", "#EBF3FB"),
    "야식": ("#673AB7", "#F3E5F5")
}

# 3. CSS 적용 (인덱스 고정 및 카드 색상 반영)
bold_c, soft_c = color_map[st.session_state.selected_meal]

st.markdown(f"""
    <style>
    .stApp {{ background-color: #FFFFFF; }}
    .block-container {{ padding: 1rem; }}
    
    /* 인덱스 탭 스타일 */
    .stButton > button {{
        height: 80px;
        width: 45px;
        writing-mode: vertical-rl;
        text-orientation: upright;
        border: none;
        color: white !important;
        border-radius: 0px 10px 10px 0px;
        margin-bottom: 4px;
        font-weight: bold;
        transition: 0.3s;
    }}
    
    /* 선택된 탭은 약간 더 튀어나오게 */
    .selected-tab {{
        transform: translateX(5px);
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }}

    /* 메인 카드 스타일: 부드러운 배경색 적용 */
    .main-card {{
        background-color: {soft_c};
        height: 450px;
        border-radius: 20px 0px 0px 20px;
        border: 2px solid {bold_c};
        padding: 30px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-align: center;
        box-shadow: -5px 5px 15px rgba(0,0,0,0.05);
    }}
    </style>
""", unsafe_allow_html=True)

# 4. 화면 구성
st.title("🗂️ 주간 식단 가이드")

selected_date = st.selectbox("날짜 선택", list(menu_data.keys()), index=1, label_visibility="collapsed")

col_card, col_tab = st.columns([8.5, 1.5])

with col_card:
    menu = menu_data[selected_date].get(st.session_state.selected_meal, ["정보 없음"])
    st.markdown(f"""
        <div class="main-card">
            <h2 style="color: {bold_c};">{st.session_state.selected_meal}</h2>
            <div style="height: 1px; background-color: {bold_c}; opacity: 0.3; margin: 20px 0;"></div>
            <p style="font-size: 24px; font-weight: bold; color: #333;">🍲 {menu[0]}</p>
            <p style="font-size: 17px; color: #555; line-height: 1.8;">{' / '.join(menu[1:])}</p>
        </div>
    """, unsafe_allow_html=True)

with col_tab:
    for label in ["조식", "간편식", "중식", "석식", "야식"]:
        b_color, _ = color_map[label]
        # 각 버튼의 색상을 개별 지정하기 위해 markdown과 button 조합
        if st.button(label, key=f"btn_{label}"):
            st.session_state.selected_meal = label
            st.rerun()
        
        # 버튼 색상 강제 주입 (Streamlit 기본 버튼 색상 오버라이드)
        st.markdown(f"""
            <style>
            div[data-testid="stVerticalBlock"] > div:nth-child({["조식", "간편식", "중식", "석식", "야식"].index(label)+1}) button {{
                background-color: {b_color} !important;
            }}
            </style>
        """, unsafe_allow_html=True)
