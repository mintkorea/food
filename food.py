import streamlit as st
from datetime import datetime, timedelta, time

# 1. 시간 설정 및 날짜 범위 생성
now = datetime.utcnow() + timedelta(hours=9)
today_date = now.date()
day_names = ["월", "화", "수", "목", "금", "토", "일"]

# 이번 주 월요일부터 일요일까지의 날짜 리스트 생성 (3/16 ~ 3/22)
start_of_week = today_date - timedelta(days=today_date.weekday())
week_dates = [start_of_week + timedelta(days=i) for i in range(7)]
week_options = {d.strftime("%Y-%m-%d"): f"{d.month}/{d.day} ({day_names[d.weekday()]})" for d in week_dates}

# 2. 식단 데이터 (이미지에서 추출된 실제 데이터)
meal_data = {
    "2026-03-16": {"조식": {"menu": "두우스프", "side": "..."}, "중식": {"menu": "차돌해물짬뽕밥", "side": "..."}, "석식": {"menu": "어항가지돈육덮밥", "side": "..."}, "야식": {"menu": "날치알볶음밥", "side": "..."}},
    "2026-03-17": {"조식": {"menu": "연포탕", "side": "..."}, "중식": {"menu": "버섯불고기", "side": "..."}, "석식": {"menu": "멘치카츠", "side": "..."}, "야식": {"menu": "미역죽", "side": "..."}},
    "2026-03-18": {
        "조식": {"menu": "감자수제비", "side": "흰쌀밥, 돈채가지볶음, 양념고추지, 깍두기, 누룽지/원두커피"},
        "간편식": {"menu": "닭가슴살샐러드 & 바나나", "side": ""},
        "중식": {"menu": "뼈없는닭볶음탕", "side": "혼합잡곡밥, 팽이장국, 유부겨자냉채, 흑깨드레싱샐러드, 열무김치, 복분자주스"},
        "석식": {"menu": "하이디라오마라탕", "side": "분모자+포두부+소세지 & 탕수육, 후르츠소스, 흰쌀밥, 짜사이무침, 열무김치"},
        "야식": {"menu": "돈사태떡찜", "side": "흰쌀밥, 유채된장국, 땅콩드레싱샐러드, 멸치볶음, 양파장아찌, 요구르트"}
    },
    "2026-03-19": {"조식": {"menu": "시래기장터국밥", "side": "..."}, "중식": {"menu": "통등심돈까스", "side": "..."}, "석식": {"menu": "돼지목살필라프", "side": "..."}, "야식": {"menu": "함박스테이크", "side": "..."}},
    "2026-03-20": {"조식": {"menu": "김치해장죽", "side": "..."}, "중식": {"menu": "뿌리채소영양밥", "side": "..."}, "석식": {"menu": "셀프쭈불비빔밥", "side": "..."}, "야식": {"menu": "치킨토마토샌드위치", "side": "..."}}
}

color_theme = {"조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"}

# 3. UI 설정 (CSS)
st.markdown(f"""
<style>
    .main .block-container {{ max-width: 500px !important; padding: 0px 8px !important; margin-top: -60px !important; }}
    .date-selector-ui {{ background-color: #f1f3f5; padding: 5px; border-radius: 15px; margin-bottom: 10px; }}
    /* 라디오 버튼 한 줄 고정 */
    div[data-testid="stRadio"] > div {{ display: flex !important; flex-wrap: nowrap !important; background-color: #f1f3f5; padding: 10px 2px !important; border-radius: 0 0 20px 20px; }}
    div[data-testid="stRadio"] label p {{ font-size: 13px !important; font-weight: 800 !important; white-space: nowrap !important; }}
</style>
""", unsafe_allow_html=True)

# 4. 날짜 선택 인터페이스
st.write("") # 간격 조절
selected_date_str = st.selectbox("날짜 선택", options=list(week_options.keys()), 
                                 format_func=lambda x: week_options[x], 
                                 index=list(week_options.keys()).index(today_date.strftime("%Y-%m-%d")))

# 5. 식단 선택 및 표시
if 'selected_meal' not in st.session_state:
    st.session_state.selected_meal = "중식"

# 카드 출력
meal_info = meal_data.get(selected_date_str, {}).get(st.session_state.selected_meal, {"menu": "정보 없음", "side": "해당 날짜의 식단 데이터가 없습니다."})
selected_color = color_theme[st.session_state.selected_meal]

st.markdown(f"""
    <div style="text-align:center; font-weight:800; font-size:20px; color:{selected_color}; margin-bottom:10px;">
        📅 {week_options[selected_date_str]}
    </div>
    <div class="menu-card" style="border:3px solid {selected_color}; border-radius:20px 20px 0 0; padding:30px 15px; text-align:center; background-color:white;">
        <div style="color:{selected_color}; font-size:14px; font-weight:bold;">{st.session_state.selected_meal}</div>
        <div style="font-size:26px; font-weight:800; margin-top:10px;">{meal_info['menu']}</div>
        <div style="height:1px; background-color:#eee; width:35%; margin:15px auto;"></div>
        <div style="color:#444; font-size:16px;">{meal_info['side']}</div>
    </div>
""", unsafe_allow_html=True)

# 라디오 버튼 (식단 종류 선택)
selected_meal = st.radio("식단선택", options=list(color_theme.keys()), horizontal=True, label_visibility="collapsed")

if selected_meal != st.session_state.selected_meal:
    st.session_state.selected_meal = selected_meal
    st.rerun()
