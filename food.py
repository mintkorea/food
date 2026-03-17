import streamlit as st
from datetime import datetime

# 1. 데이터 세팅 (테스트용)
menu_data = {
    "2026-03-17(화)": {
        "조식": ["연포탕", "매운두부찜", "모둠장아찌", "누룽지"],
        "간편식": ["고로케양배추샌드위치", "삶은계란", "플레인요거트"],
        "중식": ["버섯불고기", "우엉채레몬튀김", "수수기장밥", "얼큰어묵탕", "수정과"],
        "석식": ["양배추멘치카츠", "가쓰오장국", "시저드레싱샐러드", "열무김치"],
        "야식": ["소고기미역죽", "돈육장조림", "블루베리요플레"]
    }
}

# 2. 현재 시간 기준 초기 식사 설정
now = datetime.now()
curr_hour = now.hour
if curr_hour < 9: initial_idx = 0
elif 9 <= curr_hour < 11: initial_idx = 1
elif 11 <= curr_hour < 14: initial_idx = 2
elif 14 <= curr_hour < 19: initial_idx = 3
else: initial_idx = 4

# 3. 화면 레이아웃 설정
st.set_page_config(page_title="식단 매니저", layout="centered")

# 모바일 전용 CSS: 여백 최소화 및 라벨 버튼 스타일
st.markdown("""
    <style>
    .main { padding-top: 10px; }
    .stButton > button { 
        width: 100%; 
        border-radius: 5px; 
        height: 3em; 
        font-weight: bold;
        margin-bottom: -10px;
    }
    .selected-card {
        background-color: #ffffff;
        padding: 20px;
        border: 2px solid #ff4b4b;
        border-radius: 15px;
        text-align: center;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 4. 상단 날짜 선택 (공간 절약을 위해 드롭다운)
selected_date = st.selectbox("📅 날짜", list(menu_data.keys()), label_visibility="collapsed")

# 5. 핵심: 5개의 라벨(버튼)을 가로로 배치 (세로 모드에서도 가독성 유지)
# 세션 상태를 이용해 어떤 라벨이 클릭되었는지 추적합니다.
if 'selected_meal' not in st.session_state:
    st.session_state.selected_meal = ["조식", "간편식", "중식", "석식", "야식"][initial_idx]

cols = st.columns(5)
meal_labels = ["조식", "간편식", "중식", "석식", "야식"]

for i, label in enumerate(meal_labels):
    if cols[i].button(label):
        st.session_state.selected_meal = label

# 6. 결과 출력: 선택된 라벨에 대한 메뉴만 크게 노출
target_day = menu_data[selected_date]
target_meal_content = target_day.get(st.session_state.selected_meal, ["정보 없음"])

st.markdown(f"""
    <div class="selected-card">
        <h2 style="color: #ff4b4b; margin-bottom: 5px;">{st.session_state.selected_meal}</h2>
        <hr style="margin: 10px 0;">
        <p style="font-size: 22px; font-weight: bold; margin: 15px 0;">{target_meal_content[0]}</p>
        <div style="color: #666; font-size: 16px;">
            {' / '.join(target_meal_content[1:])}
        </div>
    </div>
""", unsafe_allow_html=True)

# 7. 하단 날짜 간편 전환 (선택 사항)
st.write("")
st.caption("💡 상단 버튼을 눌러 다른 시간대 식단을 바로 확인하세요.")
