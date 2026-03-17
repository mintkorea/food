import streamlit as st
from datetime import datetime, time

# 1. [데이터] 이번 주 식단 데이터 (3/16 ~ 3/22)
meal_data = {
    "2026-03-16": {"조식": {"menu": "두우스프 / 단호박에그마요샌드", "side": "바게트, 잡곡식빵&딸기잼, 버터..."}, "중식": {"menu": "차돌해물짬뽕밥", "side": "김말이튀김, 갈리강정소스, 흑향미밥..."}, "석식": {"menu": "어항가지돈육덮밥", "side": "흰쌀밥, 사골파국, 감자채햄볶음..."}},
    "2026-03-17": {"조식": {"menu": "제철미나리쭈꾸미연포탕", "side": "매운두부찜, 흰쌀밥, 모둠장아찌..."}, "중식": {"menu": "버섯불고기", "side": "우엉채레몬튀김, 수수기장밥, 얼큰어묵탕..."}, "석식": {"menu": "양배추멘치카츠", "side": "양배추카츠+구운야채, 흰쌀밥..."}},
    "2026-03-18": {"조식": {"menu": "감자수제비", "side": "흰쌀밥, 돈채가지볶음..."}, "중식": {"menu": "뼈없는닭볶음탕", "side": "혼합잡곡밥, 팽이장국, 유부겨자냉채..."}, "석식": {"menu": "하이디라오마라탕", "side": "분모자+포두부+소세지 & 탕수육..."}},
    "2026-03-19": {"조식": {"menu": "시래기장터국밥", "side": "모둠땡전, 케찹, 흰쌀밥..."}, "중식": {"menu": "통등심돈까스 & 데미소스", "side": "비빔막국수, 추가쌀밥, 미역국..."}, "석식": {"menu": "돼지목살필라프", "side": "우동장국, 삼색푸실리케찹볶음..."}},
    "2026-03-20": {"조식": {"menu": "김치해장죽 / 고구마파이", "side": "버터롤, 바게트&딸기잼, 버터..."}, "중식": {"menu": "뿌리채소영양밥 & 양념장", "side": "언양식바싹구이, 파채, 아욱된장국..."}, "석식": {"menu": "셀프쭈불비빔밥", "side": "콩보리밥+쭈불볶음+김가루..."}},
}

# 2. 배식 시간 설정 (조, 중, 석식만 운영)
meal_times = {
    "조식": (time(7, 0), time(9, 0)),
    "중식": (time(11, 20), time(14, 0)),
    "석식": (time(17, 20), time(19, 20))
}

# 3. 시간 및 요일 계산
now = datetime.now()
current_time = now.time()
current_date_str = now.strftime("%Y-%m-%d")
weekday = now.weekday() # 0:월, 5:토, 6:일

# 요일 색상 결정
day_color = "#333" # 평일
if weekday == 5: day_color = "#4A90E2" # 토요일(청색)
elif weekday == 6: day_color = "#E95444" # 일요일(적색)

# 현재 시간에 따른 자동 식단 선택 (조/중/석식 범위 내)
if current_time < meal_times["중식"][0]: auto_meal = "조식"
elif current_time < meal_times["석식"][0]: auto_meal = "중식"
else: auto_meal = "석식"

# 4. CSS: 타이틀 중앙정렬 및 폰트 최적화
st.markdown(f"""
<style>
    .main .block-container {{ max-width: 500px !important; padding: 10px 8px !important; }}
    
    .date-title {{
        font-size: 22px !important; /* 2폰트 상향 */
        font-weight: 800;
        text-align: center; /* 중앙 정렬 */
        margin-bottom: 10px !important;
        color: {day_color}; /* 요일별 색상 적용 */
    }}

    .menu-card {{
        border: 3px solid var(--card-color);
        border-radius: 15px 15px 0 0;
        padding: 35px 15px;
        text-align: center;
        background-color: white;
        min-height: 240px;
    }}

    .side-menu {{ color: #444; font-size: 17px !important; line-height: 1.6; font-weight: 500; margin-top: 15px; }}

    .timer-box {{
        text-align: center;
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 10px;
        margin-top: 10px;
        font-size: 14px;
        font-weight: bold;
        color: #555;
    }}
    
    div[data-testid="stRadio"] > div {{
        display: flex !important; flex-direction: row !important;
        justify-content: space-between !important;
        background-color: #f1f3f5; padding: 12px 5px !important; border-radius: 0 0 15px 15px;
    }}
    div[data-testid="stRadio"] label p {{ font-size: 14.5px !important; font-weight: 800 !important; }}
</style>
""", unsafe_allow_html=True)

# 5. UI 렌더링
st.markdown(f'<p class="date-title">📅 {now.strftime("%m월 %d일")} ({["월","화","수","목","금","토","일"][weekday]})</p>', unsafe_allow_html=True)

if 'selected_meal' not in st.session_state:
    st.session_state.selected_meal = auto_meal

# 데이터 표출
target_date = current_date_str if current_date_str in meal_data else "2026-03-17"
current_meal = meal_data[target_date].get(st.session_state.selected_meal, {"menu": "식단 정보가 없습니다", "side": ""})
color_theme = {"조식": "#E95444", "중식": "#8BC34A", "석식": "#4A90E2"}
selected_color = color_theme[st.session_state.selected_meal]

st.markdown(f"""
    <div class="menu-card" style="--card-color: {selected_color};">
        <div style="color: {selected_color}; font-size: 15px; font-weight: bold; margin-bottom: 10px;">{st.session_state.selected_meal}</div>
        <div style="font-size: 26px; font-weight: 800; color: #111; margin-bottom: 15px;">{current_meal['menu']}</div>
        <div style="height: 1px; background-color: #eee; width: 40%; margin: 0 auto;"></div>
        <div class="side-menu">{current_meal['side']}</div>
    </div>
""", unsafe_allow_html=True)

# 6. 하단 탭 & 라디오 버튼
st.radio("식단선택", options=["조식", "중식", "석식"], 
         index=["조식", "중식", "석식"].index(st.session_state.selected_meal),
         key="meal_selector", horizontal=True, label_visibility="collapsed")
st.session_state.selected_meal = st.session_state.meal_selector

# 7. 배식 시간 카운트다운 로직
start_t, end_t = meal_times[st.session_state.selected_meal]
start_dt = datetime.combine(now.date(), start_t)
end_dt = datetime.combine(now.date(), end_t)

if now < start_dt:
    diff = start_dt - now
    msg = f"⏳ {st.session_state.selected_meal} 배식 시작까지 {int(diff.seconds/3600)}시간 {int((diff.seconds%3600)/60)}분 남았습니다."
elif now <= end_dt:
    diff = end_dt - now
    msg = f"✅ 지금은 배식 중! 종료까지 {int(diff.seconds/60)}분 남았습니다."
else:
    msg = f"🚩 오늘의 {st.session_state.selected_meal} 배식이 종료되었습니다."

st.markdown(f'<div class="timer-box">{msg}</div>', unsafe_allow_html=True)
