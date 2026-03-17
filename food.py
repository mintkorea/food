import streamlit as st
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="식단 가이드", layout="centered")

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

# 3. 컬러 구성 (인덱스 가이드북 컨셉)
color_map = {
    "조식": ("#E95444", "#FFF5F4"), "간편식": ("#F1A33B", "#FFF9F0"),
    "중식": ("#8BC34A", "#F9FBF2"), "석식": ("#4A90E2", "#F0F7FF"), "야식": ("#673AB7", "#F7F2FF")
}

if 'selected_meal' not in st.session_state:
    st.session_state.selected_meal = "중식"

bold_c, soft_c = color_map[st.session_state.selected_meal]

# 4. 핵심 CSS: 인덱스를 화면 우측에 강제 고정 (Fixed)
st.markdown(f"""
    <style>
    /* 메인 컨테이너 여백 조정 (오른쪽 인덱스 공간 확보) */
    .block-container {{ padding-right: 60px !important; padding-left: 10px !important; }}

    /* 메인 카드 스타일 */
    .main-card-frame {{
        background-color: {soft_c};
        height: 500px;
        border: 2px solid {bold_c};
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        display: flex;
        flex-direction: column;
        justify-content: center;
        box-shadow: -3px 3px 10px rgba(0,0,0,0.05);
    }}

    /* 플로팅 인덱스 컨테이너 (스크롤해도 고정) */
    .floating-index {{
        position: fixed;
        right: 0px;
        top: 20%;
        display: flex;
        flex-direction: column;
        gap: 2px;
        z-index: 9999;
    }}
    
    /* 실제 버튼처럼 보이기 위한 스타일 오버라이드 */
    .stButton button {{
        width: 50px !important;
        height: 80px !important;
        writing-mode: vertical-rl !important;
        text-orientation: upright !important;
        border-radius: 5px 0 0 5px !important; /* 왼쪽만 둥글게 해서 카드와 밀착 */
        border: none !important;
        color: white !important;
        font-weight: bold !important;
        padding: 0 !important;
        font-size: 14px !important;
    }}
    </style>
""", unsafe_allow_html=True)

# 5. 화면 구성
st.title("📖 주간 식단 가이드")
selected_date = st.selectbox("날짜", list(menu_data.keys()), label_visibility="collapsed")

# 메인 카드 프레임
menu = menu_data[selected_date].get(st.session_state.selected_meal, ["정보 없음"])
st.markdown(f"""
    <div class="main-card-frame">
        <h2 style="color: {bold_c};">{st.session_state.selected_meal}</h2>
        <hr style="border: 0.5px solid {bold_c}; opacity: 0.2; margin: 15px 0;">
        <p style="font-size: 24px; font-weight: bold; color: #333;">🍲 {menu[0]}</p>
        <p style="font-size: 17px; color: #666; line-height: 1.8;">{' / '.join(menu[1:])}</p>
    </div>
""", unsafe_allow_html=True)

# 6. 우측 고정 인덱스 버튼 (물리적 배치)
# HTML/CSS로 고정된 위치에 Streamlit 버튼을 렌더링하기 위해 빈 공간(Container) 활용
with st.container():
    # CSS 고정 위치를 잡기 위해 별도의 div 없이 버튼만 나열해도 
    # 위의 .stButton CSS가 위치를 강제로 잡아줍니다.
    for label in ["조식", "간편식", "중식", "석식", "야식"]:
        b_color, _ = color_map[label]
        
        # 각 버튼을 감싸는 div에 고정 위치 부여
        idx = ["조식", "간편식", "중식", "석식", "야식"].index(label)
        top_pos = 150 + (idx * 82)
        
        st.markdown(f"""
            <div style="position: fixed; right: 0; top: {top_pos}px; z-index: 10000;">
            <style>
                div[data-testid="stVerticalBlock"] > div:nth-child({idx+4}) button {{
                    background-color: {b_color} !important;
                }}
            </style>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button(label, key=f"fixed_{label}"):
            st.session_state.selected_meal = label
            st.rerun()
