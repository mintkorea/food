import streamlit as st
from datetime import datetime, time

# 1. [데이터] 주간 식단표 (이미지 기반 최신 데이터 반영)
meal_data = {
    "2026-03-18": {
        "조식": {"menu": "감자수제비", "side": "흰쌀밥, 돈채가지볶음, 양념고추지, 깍두기, 누룽지/원두커피"},
        "간편식": {"menu": "닭가슴살샐러드 & 바나나", "side": ""},
        "중식": {"menu": "뼈없는닭볶음탕", "side": "혼합잡곡밥, 팽이장국, 유부겨자냉채, 흑깨드레싱샐러드, 열무김치, 복분자주스"},
        "석식": {"menu": "하이디라오마라탕", "side": "분모자+포두부+소세지 & 탕수육, 후르츠소스, 흰쌀밥, 짜사이무침, 열무김치"},
        "야식": {"menu": "돈사태떡찜", "side": "흰쌀밥, 유채된장국, 땅콩드레싱샐러드, 멸치볶음, 양파장아찌, 요구르트"}
    }
}

# 2. 배식 시간 설정 (자동 전환용)
meal_times = {
    "조식": (time(7, 0), time(9, 0)),
    "중식": (time(11, 20), time(14, 0)),
    "석식": (time(17, 20), time(19, 20))
}

# 3. 시간 및 요일 계산 로직
now = datetime.now()
curr_t = now.time()
weekday = now.weekday()
day_names = ["월", "화", "수", "목", "금", "토", "일"]

# 요일 색상 결정 (평일: 검정, 토: 파랑, 일: 빨강)
day_color = "#E95444" if weekday == 6 else ("#4A90E2" if weekday == 5 else "#222")

# [핵심] 현재 시각에 따른 자동 기본 식단 결정 (조 -> 중 -> 석 순차 전환)
if curr_t < meal_times["중식"][0]:
    auto_meal = "조식"
elif curr_t < meal_times["석식"][0]:
    auto_meal = "중식"
else:
    auto_meal = "석식"

# 4. CSS: 레이아웃 복구 및 디자인 최적화
st.markdown(f"""
<style>
    /* 상단 여백 제거 및 컨테이너 너비 제한 */
    .main .block-container {{ max-width: 480px !important; padding: 5px 10px !important; }}
    
    /* 제목 폰트 22px (기존 20px에서 상향) & 중앙 정렬 */
    .date-title {{
        font-size: 22px !important; font-weight: 800; text-align: center;
        margin: 15px 0 !important; color: {day_color};
    }}

    /* 메뉴 카드 디자인 */
    .menu-card {{
        border: 3px solid var(--card-color); border-radius: 20px 20px 0 0;
        padding: 30px 15px; text-align: center; background-color: white;
        min-height: 240px;
    }}

    /* 식단 텍스트 17px로 상향 */
    .side-menu {{ color: #444; font-size: 17px !important; line-height: 1.6; font-weight: 500; margin-top: 15px; word-break: keep-all; }}

    /* 라디오 버튼 디자인 보정: 개행 방지 */
    div[data-testid="stRadio"] > div {{
        display: flex !important; flex-wrap: nowrap !important;
        justify-content: space-between !important; background-color: #f1f3f5;
        padding: 10px 2px !important; border-radius: 0 0 20px 20px;
    }}
    div[data-testid="stRadio"] label {{ flex: 1 !important; min-width: 0 !important; justify-content: center !important; }}
    div[data-testid="stRadio"] label p {{ 
        font-size: 13.5px !important; font-weight: 800 !important; 
        white-space: nowrap !important; letter-spacing: -0.5px;
    }}

    /* 하단 타이머/안내 박스 */
    .timer-box {{
        text-align: center; background-color: #f8f9fa; padding: 12px;
        border-radius: 12px; font-size: 14px; font-weight: bold; color: #555; margin-top: 15px;
    }}
</style>
""", unsafe_allow_html=True)

# 5. UI 렌더링
st.markdown(f'<p class="date-title">📅 {now.strftime("%m월 %d일")} ({day_names[weekday]})</p>', unsafe_allow_html=True)

if 'selected_meal' not in st.session_state:
    st.session_state.selected_meal = auto_meal

# 모든 메뉴 선택 가능 (간편식, 야식 포함)
all_options = ["조식", "간편식", "중식", "석식", "야식"]
selected = st.radio("식단", options=all_options, 
                    index=all_options.index(st.session_state.selected_meal),
                    horizontal=True, label_visibility="collapsed")
st.session_state.selected_meal = selected

# 식단 데이터 매칭
display_date = now.strftime("%Y-%m-%d") if now.strftime("%Y-%m-%d") in meal_data else "2026-03-18"
meal_info = meal_data[display_date].get(st.session_state.selected_meal, {"menu": "정보 없음", "side": ""})
color_theme = {"조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"}
selected_color = color_theme.get(st.session_state.selected_meal, "#333")

st.markdown(f"""
    <div class="menu-card" style="--card-color: {selected_color};">
        <div style="color: {selected_color}; font-size: 15px; font-weight: bold; margin-bottom: 10px;">{st.session_state.selected_meal}</div>
        <div style="font-size: 26px; font-weight: 800; color: #111; margin-bottom: 15px;">{meal_info['menu']}</div>
        <div style="height: 1px; background-color: #eee; width: 40%; margin: 0 auto;"></div>
        <div class="side-menu">{meal_info['side']}</div>
    </div>
""", unsafe_allow_html=True)

# 6. 배식 시간 알림 (조, 중, 석식 기준)
if st.session_state.selected_meal in meal_times:
    s_time, e_time = meal_times[st.session_state.selected_meal]
    s_dt = datetime.combine(now.date(), s_time)
    e_dt = datetime.combine(now.date(), e_time)

    if now < s_dt:
        diff = s_dt - now
        msg = f"⏳ {st.session_state.selected_meal} 시작까지 {diff.seconds//3600}시간 {(diff.seconds%3600)//60}분 남음"
    elif now <= e_dt:
        diff = e_dt - now
        msg = f"🍴 지금은 배식 중! 종료까지 {diff.seconds//60}분 남음"
    else:
        msg = f"🚩 오늘의 {st.session_state.selected_meal} 배식이 종료되었습니다."
else:
    msg = f"💡 {st.session_state.selected_meal} 메뉴를 확인 중입니다."

st.markdown(f'<div class="timer-box">{msg}</div>', unsafe_allow_html=True)
