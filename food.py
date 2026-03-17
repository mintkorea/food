import streamlit as st
from datetime import datetime, timedelta, time

# 1. 한국 시간(KST) 설정 및 시차 보정
# 서버 시간에 9시간을 더해 한국 표준시를 계산합니다.
now = datetime.utcnow() + timedelta(hours=9)
curr_t = now.time()
weekday = now.weekday()
day_names = ["월", "화", "수", "목", "금", "토", "일"]

# 2. 식단 데이터 (3/18일 기준)
meal_data = {
    "2026-03-18": {
        "조식": {"menu": "감자수제비", "side": "흰쌀밥, 돈채가지볶음, 양념고추지, 깍두기, 누룽지/원두커피"},
        "간편식": {"menu": "닭가슴살샐러드 & 바나나", "side": "건강한 한 끼를 즐기세요"},
        "중식": {"menu": "뼈없는닭볶음탕", "side": "혼합잡곡밥, 팽이장국, 유부겨자냉채, 흑깨드레싱샐러드, 열무김치, 복분자주스"},
        "석식": {"menu": "하이디라오마라탕", "side": "분모자+포두부+소세지 & 탕수육, 후르츠소스, 흰쌀밥, 짜사이무침, 열무김치"},
        "야식": {"menu": "돈사태떡찜", "side": "흰쌀밥, 유채된장국, 땅콩드레싱샐러드, 멸치볶음, 양파장아찌, 요구르트"}
    }
}

color_theme = {"조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"}
meal_times = {
    "조식": (time(7, 0), time(9, 0)),
    "중식": (time(11, 20), time(14, 0)),
    "석식": (time(17, 20), time(19, 20))
}

# 자동 식단 선택
if curr_t < meal_times["중식"][0]: auto_meal = "조식"
elif curr_t < meal_times["석식"][0]: auto_meal = "중식"
else: auto_meal = "석식"

# 3. CSS: 상하단 여백 정밀 조정
day_color = "#E95444" if weekday == 6 else ("#4A90E2" if weekday == 5 else "#222")

st.markdown(f"""
<style>
    /* 상단 기본 여백 완전 제거 및 폰트 설정 */
    .main .block-container {{ 
        max-width: 500px !important; 
        padding: 0px 10px 50px 10px !important; /* 하단 패딩 50px로 확보 */
        margin-top: -60px !important; 
    }}
    
    .date-title {{
        font-size: 20px !important; font-weight: 800; text-align: center;
        margin: 5px 0 10px 0 !important; color: {day_color};
    }}

    /* 메뉴 카드: 상단 라운드 유지 */
    .menu-card {{
        border: 3px solid var(--card-color); border-radius: 20px 20px 0 0;
        padding: 30px 15px; text-align: center; background-color: white; 
        min-height: 220px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }}

    .side-menu {{ color: #444; font-size: 17px !important; line-height: 1.6; font-weight: 500; margin-top: 15px; word-break: keep-all; }}

    /* 인덱스 탭: 카드 바로 아래 밀착 */
    .index-tabs-wrap {{ display: flex; width: 100%; margin-top: -3px; }}
    .tab-unit {{
        flex: 1; text-align: center; padding: 10px 0;
        font-size: 13px !important; font-weight: bold; color: white;
    }}

    /* 라디오 버튼: 탭 하단에 자연스럽게 연결 */
    div[data-testid="stRadio"] > div {{
        display: flex !important; flex-wrap: nowrap !important;
        background-color: #f1f3f5; padding: 12px 2px !important; border-radius: 0 0 20px 20px;
    }}
    div[data-testid="stRadio"] label {{ flex: 1 !important; justify-content: center !important; }}
    div[data-testid="stRadio"] label p {{ font-size: 13.5px !important; font-weight: 800 !important; }}
    
    /* 하단 안내 박스: 여백 확보 */
    .timer-box {{
        text-align: center; background-color: #f8f9fa; padding: 15px;
        border-radius: 12px; font-size: 15px; font-weight: bold; color: #555; 
        margin-top: 20px; border: 1px solid #eee;
    }}
</style>
""", unsafe_allow_html=True)

# 4. 상단 날짜 출력
st.markdown(f'<p class="date-title">📅 {now.strftime("%m월 %d일")} ({day_names[weekday]})</p>', unsafe_allow_html=True)

if 'selected_meal' not in st.session_state:
    st.session_state.selected_meal = auto_meal

# [A] 메뉴 카드 출력
display_date = now.strftime("%Y-%m-%d")
meal_info = meal_data.get(display_date, meal_data["2026-03-18"]).get(st.session_state.selected_meal, {"menu": "정보 없음", "side": ""})
selected_color = color_theme[st.session_state.selected_meal]

st.markdown(f"""
    <div class="menu-card" style="--card-color: {selected_color};">
        <div style="color: {selected_color}; font-size: 14px; font-weight: bold; margin-bottom: 5px;">{st.session_state.selected_meal}</div>
        <div style="font-size: 26px; font-weight: 800; color: #111; margin-bottom: 12px;">{meal_info['menu']}</div>
        <div style="height: 1px; background-color: #eee; width: 35%; margin: 0 auto;"></div>
        <div class="side-menu">{meal_info['side']}</div>
    </div>
""", unsafe_allow_html=True)

# [B] 인덱스 탭 (카드 하단 부착)
tabs_html = '<div class="index-tabs-wrap">'
for meal, color in color_theme.items():
    opacity = "1.0" if meal == st.session_state.selected_meal else "0.3"
    tabs_html += f'<div class="tab-unit" style="background-color: {color}; opacity: {opacity};">{meal}</div>'
tabs_html += '</div>'
st.markdown(tabs_html, unsafe_allow_html=True)

# [C] 라디오 버튼 (탭 하단 부착)
selected = st.radio("식단선택", options=list(color_theme.keys()), 
                    index=list(color_theme.keys()).index(st.session_state.selected_meal),
                    horizontal=True, label_visibility="collapsed")

if selected != st.session_state.selected_meal:
    st.session_state.selected_meal = selected
    st.rerun()

# 5. 시간 계산 로직 (X시간 Y분 형식)
if st.session_state.selected_meal in meal_times:
    s_t, e_t = meal_times[st.session_state.selected_meal]
    s_dt, e_dt = datetime.combine(now.date(), s_t), datetime.combine(now.date(), e_t)
    
    if now < s_dt:
        td = s_dt - now
        h, m = td.seconds // 3600, (td.seconds % 3600) // 60
        time_str = f"{h}시간 {m}분" if h > 0 else f"{m}분"
        msg = f"⏳ {st.session_state.selected_meal} 시작까지 {time_str} 남음"
    elif now <= e_dt:
        td = e_dt - now
        h, m = td.seconds // 3600, (td.seconds % 3600) // 60
        time_str = f"{h}시간 {m}분" if h > 0 else f"{m}분"
        msg = f"🍴 {st.session_state.selected_meal} 배식 중! 종료까지 {time_str} 남음"
    else:
        msg = f"🚩 오늘의 {st.session_state.selected_meal} 배식이 종료되었습니다."
else:
    msg = f"💡 {st.session_state.selected_meal} 메뉴를 확인 중입니다."

st.markdown(f'<div class="timer-box">{msg}</div>', unsafe_allow_html=True)
