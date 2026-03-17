import streamlit as st
from datetime import datetime, time

# 1. [데이터] 이번 주 전체 식단 데이터 (이미지 기반)
meal_data = {
    "2026-03-18": {
        "조식": {"menu": "감자수제비", "side": "흰쌀밥, 돈채가지볶음, 양념고추지, 깍두기, 누룽지/원두커피"},
        "간편식": {"menu": "닭가슴살샐러드 & 바나나", "side": ""},
        "중식": {"menu": "뼈없는닭볶음탕", "side": "혼합잡곡밥, 팽이장국, 유부겨자냉채, 흑깨드레싱샐러드, 열무김치, 복분자주스"},
        "석식": {"menu": "하이디라오마라탕", "side": "분모자+포두부+소세지 & 탕수육, 후르츠소스, 흰쌀밥, 짜사이무침, 열무김치"},
        "야식": {"menu": "돈사태떡찜", "side": "흰쌀밥, 유채된장국, 땅콩드레싱샐러드, 멸치볶음, 양파장아찌, 요구르트"}
    }
}

# 2. 배식 시간 설정
meal_times = {
    "조식": (time(7, 0), time(9, 0)),
    "중식": (time(11, 20), time(14, 0)),
    "석식": (time(17, 20), time(19, 20))
}

# 3. 현재 시간 및 요일 계산
now = datetime.now()
current_time = now.time()
weekday = now.weekday()
day_names = ["월", "화", "수", "목", "금", "토", "일"]

# 요일 색상 (토: 파랑, 일/공휴일: 빨강)
day_color = "#333"
if weekday == 5: day_color = "#4A90E2"
elif weekday == 6: day_color = "#E95444"

# [핵심 로직] 현재 시간에 따른 자동 식단 전환 (조 -> 중 -> 석)
if current_time < meal_times["중식"][0]:
    auto_meal = "조식"
elif current_time < meal_times["석식"][0]:
    auto_meal = "중식"
else:
    auto_meal = "석식"

# 4. CSS: 디자인 최적화
st.markdown(f"""
<style>
    .main .block-container {{ max-width: 500px !important; padding: 5px 8px !important; }}
    .date-title {{
        font-size: 22px !important; font-weight: 800; text-align: center;
        margin-bottom: 15px !important; color: {day_color};
    }}
    .menu-card {{
        border: 3px solid var(--card-color); border-radius: 15px 15px 0 0;
        padding: 30px 15px; text-align: center; background-color: white; min-height: 220px;
    }}
    .side-menu {{ color: #444; font-size: 17px !important; line-height: 1.6; font-weight: 500; margin-top: 15px; }}
    .timer-box {{
        text-align: center; background-color: #f8f9fa; padding: 12px;
        border-radius: 0 0 15px 15px; font-size: 14px; font-weight: bold; color: #555; margin-bottom: 20px;
    }}
    /* 라디오 버튼 가로 정렬 및 폰트 */
    div[data-testid="stRadio"] > div {{
        display: flex !important; flex-direction: row !important; flex-wrap: wrap !important;
        justify-content: center !important; gap: 5px !important;
    }}
    div[data-testid="stRadio"] label {{
        background-color: #eee; padding: 5px 12px !important; border-radius: 20px;
    }}
    div[data-testid="stRadio"] label p {{ font-size: 15px !important; font-weight: 700 !important; }}
</style>
""", unsafe_allow_html=True)

# 5. UI 출력
st.markdown(f'<p class="date-title">📅 {now.strftime("%m월 %d일")} ({day_names[weekday]})</p>', unsafe_allow_html=True)

# 세션 상태 초기화 (처음 실행 시 현재 시간대의 식단 자동 선택)
if 'selected_meal' not in st.session_state:
    st.session_state.selected_meal = auto_meal

# 식단 선택 라디오 버튼 (모든 메뉴 포함)
all_options = ["조식", "간편식", "중식", "석식", "야식"]
selected = st.radio("식단 선택", options=all_options, 
                    index=all_options.index(st.session_state.selected_meal),
                    horizontal=True, label_visibility="collapsed")
st.session_state.selected_meal = selected

# 데이터 불러오기
current_date_str = now.strftime("%Y-%m-%d")
# 테스트를 위해 데이터가 없는 경우 18일 데이터로 고정 표출
display_date = current_date_str if current_date_str in meal_data else "2026-03-18"
meal_info = meal_data[display_date].get(st.session_state.selected_meal, {"menu": "식단 정보 없음", "side": ""})

# 색상 테마
color_theme = {"조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"}
selected_color = color_theme.get(st.session_state.selected_meal, "#333")

# 식단 카드 표출
st.markdown(f"""
    <div class="menu-card" style="--card-color: {selected_color};">
        <div style="color: {selected_color}; font-size: 15px; font-weight: bold; margin-bottom: 10px;">{st.session_state.selected_meal}</div>
        <div style="font-size: 26px; font-weight: 800; color: #111; margin-bottom: 15px; word-break: keep-all;">{meal_info['menu']}</div>
        <div style="height: 1px; background-color: #eee; width: 40%; margin: 0 auto;"></div>
        <div class="side-menu">{meal_info['side']}</div>
    </div>
""", unsafe_allow_html=True)

# 6. 배식 시간 타이머 (조, 중, 석식에 대해서만 작동)
if st.session_state.selected_meal in meal_times:
    start_t, end_t = meal_times[st.session_state.selected_meal]
    start_dt = datetime.combine(now.date(), start_t)
    end_dt = datetime.combine(now.date(), end_t)

    if now < start_dt:
        diff = start_dt - now
        msg = f"⏳ {st.session_state.selected_meal} 시작까지 {diff.seconds//3600}시간 {(diff.seconds%3600)//60}분 남음"
    elif now <= end_dt:
        diff = end_dt - now
        msg = f"✅ {st.session_state.selected_meal} 배식 중! 종료까지 {diff.seconds//60}분 남음"
    else:
        msg = f"🚩 오늘의 {st.session_state.selected_meal} 배식이 종료되었습니다."
else:
    msg = f"💡 {st.session_state.selected_meal} 메뉴를 확인 중입니다."

st.markdown(f'<div class="timer-box">{msg}</div>', unsafe_allow_html=True)
