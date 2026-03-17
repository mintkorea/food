import streamlit as st
from datetime import datetime

# 1. 데이터 세팅 (테스트용)
menu_data = {
    "2026-03-17(화)": {
        "조식": ["연포탕", "매운두부찜", "모둠장아찌", "깍두기", "누룽지"],
        "간편식": ["고로케양배추샌드위치", "삶은계란", "플레인요거트"],
        "중식": ["버섯불고기", "우엉채레몬튀김", "수수기장밥", "얼큰어묵탕", "수정과"],
        "석식": ["양배추멘치카츠", "가쓰오장국", "시저드레싱샐러드", "열무김치"],
        "야식": ["소고기미역죽", "돈육장조림", "깍두기", "블루베리요플레"]
    }
}

# 2. 현재 시간 기준 초기 식사 설정
now = datetime.now()
curr_hour = now.hour
if curr_hour < 9: default_meal = "조식"
elif 9 <= curr_hour < 11: default_meal = "간편식"
elif 11 <= curr_hour < 14: default_meal = "중식"
elif 14 <= curr_hour < 19: default_meal = "석식"
else: default_meal = "야식"

# 3. 화면 레이아웃 및 CSS 설정
st.set_page_config(page_title="인덱스 식단", layout="centered")

# CSS를 이용해 다이어리 인덱스 형태 구현
st.markdown("""
    <style>
    /* 전체 배경을 다이어리처럼 설정 */
    .stApp { background-color: #f5f5f5; }
    
    /* 인덱스 탭 스타일 (이미지의 물리적인 탭 느낌) */
    .stButton > button {
        width: 100%; 
        border-radius: 5px; 
        height: 3.5em; 
        font-weight: bold;
        color: white !important;
        margin-bottom: 5px;
    }
    
    /* 인덱스별 테마 색상 (이미지 참고) */
    /* 1. 조식 (주황색) */
    div.row-widget.stButton:nth-of-type(1) > button { background-color: #ff9800; } 
    /* 2. 간편식 (노란색) */
    div.row-widget.stButton:nth-of-type(2) > button { background-color: #fbc02d; color: black !important;} 
    /* 3. 중식 (초록색) */
    div.row-widget.stButton:nth-of-type(3) > button { background-color: #8bc34a; } 
    /* 4. 석식 (파란색) */
    div.row-widget.stButton:nth-of-type(4) > button { background-color: #3f51b5; } 
    /* 5. 야식 (보라색) */
    div.row-widget.stButton:nth-of-type(5) > button { background-color: #9c27b0; }

    /* 메인 카드 (상세 내용 영역) */
    .selected-card {
        background-color: #ffffff;
        padding: 30px;
        border: 2px solid #ff4b4b;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        margin-top: -10px; /* 인덱스 카드 위로 올라오는 효과 */
    }
    </style>
""", unsafe_allow_html=True)

st.title("📖 Index Daily Menu")

# 4. 상단 날짜 선택 (드롭다운)
col_date, _ = st.columns([2, 3]) # 날짜 선택을 좁게
with col_date:
    selected_date = st.selectbox("📅 날짜 선택", list(menu_data.keys()), label_visibility="collapsed")

# 5. 핵심: 인덱스 탭과 메인 카드 레이아웃
if 'selected_meal' not in st.session_state:
    st.session_state.selected_meal = default_meal

col_main, col_tabs = st.columns([3, 1]) # 메인 카드 3, 인덱스 탭 1 비율

# 좌측: 메인 카드 (상세 내용 출력)
with col_main:
    target_day_content = menu_data[selected_date]
    target_meal_menu = target_day_content.get(st.session_state.selected_meal, ["정보 없음"])

    st.markdown(f"""
        <div class="selected-card">
            <h2 style="color: #333; margin-bottom: 5px;">{st.session_state.selected_meal}</h2>
            <hr style="margin: 15px 0;">
            <p style="font-size: 24px; font-weight: bold; margin: 20px 0;">🍲 {target_meal_menu[0]}</p>
            <div style="color: #666; font-size: 18px; line-height: 1.6;">
                {' / '.join(target_meal_menu[1:])}
            </div>
        </div>
    """, unsafe_allow_html=True)

# 우측: 인덱스 탭 (세로 버튼 배치)
with col_tabs:
    meal_tabs = ["조식", "간편식", "중식", "석식", "야식"]
    for tab_label in meal_tabs:
        # 버튼 클릭 시 세션 상태를 변경하여 화면을 리로드합니다.
        if st.button(tab_label):
            st.session_state.selected_meal = tab_label
