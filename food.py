import streamlit as st
from datetime import datetime, timedelta, time

# 1. 한국 시간(KST) 및 기본 설정
now = datetime.utcnow() + timedelta(hours=9)
curr_t = now.time()
weekday = now.weekday()
day_names = ["월", "화", "수", "목", "금", "토", "일"]

# 2. 식단 데이터 (사용자 제공 정상 데이터 사용)
meal_data = {
    "2026-03-16": {"조식": {"menu": "두우스프 / 단호박에그마요샌드", "side": "바게트, 잡곡식빵..."}, "중식": {"menu": "차돌해물짬뽕밥", "side": "..."}, "석식": {"menu": "어항가지돈육덮밥", "side": "..."}, "야식": {"menu": "날치알볶음밥", "side": "..."}},
    "2026-03-17": {"조식": {"menu": "제철미나리쭈꾸미연포탕", "side": "매운두부찜..."}, "중식": {"menu": "버섯불고호", "side": "..."}, "석식": {"menu": "양배추멘치카츠", "side": "..."}, "야식": {"menu": "소고기미역죽", "side": "..."}},
    "2026-03-18": {
        "조식": {"menu": "감자수제비", "side": "흰쌀밥, 돈채가지볶음, 양념고추지, 깍두기, 누룽지/원두커피"},
        "간편식": {"menu": "닭가슴살샐러드 & 바나나", "side": ""},
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

# 3. CSS (정상 작동하는 라디오 버튼 스타일 유지 + 상단 여백 보정)
day_color = "#E95444" if weekday == 6 else ("#4A90E2" if weekday == 5 else "#222")

st.markdown(f"""
<style>
    /* 상단 여백 제거 */
    .main .block-container {{ max-width: 500px !important; padding: 0px 8px !important; margin-top: -60px !important; }}
    
    .date-title {{ font-size: 20px !important; font-weight: 800; text-align: center; margin: 10px 0 !important; color: {day_color}; }}

    .menu-card {{ border: 3px solid var(--card-color); border-radius: 20px 20px 0 0; padding: 30px 15px; text-align: center; background-color: white; min-height: 220px; }}

    .side-menu {{ color: #444; font-size: 17px !important; line-height: 1.6; font-weight: 500; margin-top: 15px; }}

    .index-tabs-wrap {{ display: flex; width: 100%; overflow: hidden; margin-top: -3px; }}
    .tab-unit {{ flex: 1; text-align: center; padding: 10px 0; font-size: 13px !important; font-weight: bold; color: white; }}

    /* 라디오 버튼 (제공해주신 정상 소스 스타일) */
    div[data-testid="stRadio"] > div {{
        display: flex !important; flex-wrap: nowrap !important;
        background-color: #f1f3f5; padding: 10px 2px !important; border-radius: 0 0 20px 20px;
    }}
    div[data-testid="stRadio"] label {{ flex: 1 !important; justify-content: center !important; }}
    div[data-testid="stRadio"] label p {{ font-size: 13px !important; font-weight: 800 !important; white-space: nowrap !important; }}
    
    .timer-box {{ text-align: center; background-color: #f8f9fa; padding: 12px; border-radius: 12px; font-size: 14px; font-weight: bold; color: #555; margin: 15px 0 30px 0; }}
</style>
""", unsafe_allow_html=True)

# 4. UI 및 시간 로직 (요청하신 형식 반영)
st.markdown(f'<p class="date-title">📅 {now.strftime("%m월 %d일")} ({day_names[weekday]})</p>', unsafe_allow_html=True)

if 'selected_meal' not in st.session_state:
    st.session_state.selected_meal = auto_meal

# 카드 출력
display_date = now.strftime("%Y-%m-%d")
curr_meal_info = meal_data.get(display_date, meal_data["2026-03-18"]).get(st.session_state.selected_meal, {"menu": "정보 없음", "side": ""})
selected_color = color_theme[st.session_state.selected_meal]

st.markdown(f'<div class="menu-card" style="--card-color: {selected_color};">...</div>', unsafe_allow_html=True) # (상세 내용은 생략)

# 인덱스 탭 & 라디오 버튼
# ... (중략: 인덱스 탭 생성 코드)
selected = st.radio("식단선택", options=list(color_theme.keys()), index=list(color_theme.keys()).index(st.session_state.selected_meal), horizontal=True, label_visibility="collapsed")

# 5. 시간 계산 (몇 시간 몇 분)
if st.session_state.selected_meal in meal_times:
    s_t, e_t = meal_times[st.session_state.selected_meal]
    s_dt, e_dt = datetime.combine(now.date(), s_t), datetime.combine(now.date(), e_t)
    diff = (s_dt - now) if now < s_dt else (e_dt - now)
    
    if diff.total_seconds() > 0:
        h, m = diff.seconds // 3600, (diff.seconds % 3600) // 60
        time_text = f"{h}시간 {m}분" if h > 0 else f"{m}분"
        msg = f"{'⌛ 시작까지' if now < s_dt else '🍴 배식 종료까지'} {time_text} 남음"
    else:
        msg = f"🚩 오늘의 {st.session_state.selected_meal} 배식이 완료되었습니다."
else:
    msg = f"💡 {st.session_state.selected_meal} 메뉴를 확인 중입니다."

st.markdown(f'<div class="timer-box">{msg}</div>', unsafe_allow_html=True)
