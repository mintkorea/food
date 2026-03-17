import streamlit as st
from datetime import datetime, timedelta, time
from zoneinfo import ZoneInfo

# 1. 기초 설정
KST = ZoneInfo("Asia/Seoul")
def today_kst(): return datetime.now(KST).date()

st.set_page_config(page_title="식단 가이드", page_icon="🍴", layout="centered")

# 근무조 계산 함수
def get_work_shift(d):
    anchor = datetime(2026, 3, 13).date()
    diff = (d - anchor).days
    shifts = [{"n": "A조", "bg": "#FF9800"}, {"n": "B조", "bg": "#E91E63"}, {"n": "C조", "bg": "#2196F3"}]
    return shifts[diff % 3]

# 2. 시간 기준 자동 선택 로직
now_dt = datetime.now(KST)
curr_t = now_dt.time()

def get_default_meal():
    if curr_t < time(9, 0): return "조식"
    if curr_t < time(14, 0): return "중식"
    if curr_t < time(19, 20): return "석식"
    return "중식"

if 'target_date' not in st.session_state:
    st.session_state.target_date = today_kst()
if 'selected_meal' not in st.session_state:
    st.session_state.selected_meal = get_default_meal()

# URL 파라미터 처리 (날짜 이동 대응)
url_params = st.query_params
if "d" in url_params:
    try:
        st.session_state.target_date = datetime.strptime(url_params["d"], "%Y-%m-%d").date()
    except: pass

# 3. 데이터 세트 (샘플 데이터 보강)
meal_data = {
    "2026-03-17": {
        "중식": {"menu": "버섯불고기", "side": "혼합잡곡밥, 근대국, 쌈채소, 배추겉절이"},
        "야식": {"menu": "돈사태떡찜", "side": "흰쌀밥, 유채된장국, 멸치볶음, 요구르트"}
    },
    "2026-03-18": {
        "조식": {"menu": "감자수제비", "side": "흰쌀밥, 돈채가지볶음, 양념고추지, 깍두기"},
        "중식": {"menu": "뼈없는닭볶음탕", "side": "혼합잡곡밥, 팽이장국, 유부겨자냉채, 열무김치, 복분자주스"},
        "석식": {"menu": "하이디라오마라탕", "side": "분모자+포두부+소세지 & 탕수육, 흰쌀밥, 짜사이, 열무김치"}
    },
    "2026-03-19": {
        "조식": {"menu": "시래기장터국밥", "side": "모듬땡전, 케첩, 흰쌀밥, 깍두기"},
        "중식": {"menu": "통등심돈까스", "side": "비빔막국수, 추가쌀밥, 미역국, 샐러드, 깍두기"}
    }
}

color_theme = {"조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"}
meal_times = {"조식": (time(7, 0), time(9, 0)), "중식": (time(11, 20), time(14, 0)), "석식": (time(17, 20), time(19, 20))}

# 4. CSS (레이아웃 고정)
d = st.session_state.target_date
shift = get_work_shift(d)
w_idx = d.weekday()
w_str, w_class = ["월","화","수","목","금","토","일"][w_idx], ("sat" if w_idx == 5 else ("sun" if w_idx == 6 else ""))

st.markdown(f"""
<style>
    .block-container {{ padding: 1rem 1.2rem !important; max-width: 500px !important; }}
    header {{ visibility: hidden; }}
    .date-display-box {{ text-align: center; background-color: #F8FAFF; padding: 15px 10px 8px 10px; border-radius: 12px 12px 0 0; border: 1px solid #D1D9E6; border-bottom: none; }}
    .res-main-title {{ font-size: 20px !important; font-weight: 800; color: #1E3A5F; display: block; margin-bottom: 4px; }}
    .res-sub-title {{ font-size: 18px !important; font-weight: 700; color: #333; }}
    .sat {{ color: #0000FF !important; }} .sun {{ color: #FF0000 !important; }}
    .nav-link-bar {{ display: flex; width: 100%; background: white; border: 1px solid #D1D9E6; border-radius: 0 0 10px 10px; margin-bottom: 25px; }}
    .nav-item {{ flex: 1; text-align: center; padding: 10px 0; text-decoration: none; color: #1E3A5F; font-weight: bold; border-right: 1px solid #F0F0F0; font-size: 13px; }}
    .menu-card {{ border: 3px solid var(--card-color); border-radius: 20px 20px 0 0; padding: 25px 15px; text-align: center; background: white; min-height: 200px; display: flex; flex-direction: column; justify-content: center; }}
    .index-tabs-wrap {{ display: flex; width: 100%; margin-top: -3px; }}
    .tab-unit {{ flex: 1; text-align: center; padding: 10px 0; font-size: 12px; font-weight: bold; color: white; }}
    div[data-testid="stRadio"] > div {{ display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important; background-color: #f1f3f5; padding: 10px 0px !important; border-radius: 0 0 20px 20px; }}
    div[data-testid="stRadio"] label p {{ font-size: 12px !important; font-weight: 800 !important; white-space: nowrap !important; }}
    .timer-box {{ text-align: center; background-color: #f8f9fa; padding: 12px; border-radius: 12px; font-size: 14px; font-weight: bold; color: #555; margin-top: 15px; }}
</style>
""", unsafe_allow_html=True)

# 5. 헤더 출력
st.markdown(f"""
<div class="date-display-box">
    <span class="res-main-title">🍽️ 성의교정 주간 식단</span>
    <span class="res-sub-title">{d.strftime("%Y.%m.%d")}.<span class="{w_class}">({w_str})</span>
    <span style="background:{shift['bg']}; color:white; padding:2px 10px; border-radius:12px; font-size:14px; margin-left:5px; vertical-align:middle;">{shift['n']}</span></span>
</div>
<div class="nav-link-bar">
    <a href="./?d={(d-timedelta(1)).strftime('%Y-%m-%d')}" target="_self" class="nav-item">◀ Before</a>
    <a href="./?d={today_kst().strftime('%Y-%m-%d')}" target="_self" class="nav-item">Today</a>
    <a href="./?d={(d+timedelta(1)).strftime('%Y-%m-%d')}" target="_self" class="nav-item">Next ▶</a>
</div>
""", unsafe_allow_html=True)

# 6. 식단 카드 출력 (데이터 부재 시 대응 로직)
date_key = d.strftime("%Y-%m-%d")
meal_info = meal_data.get(date_key, {}).get(st.session_state.selected_meal, {"menu": "정보 없음", "side": "식단 정보가 등록되지 않았습니다."})
selected_color = color_theme[st.session_state.selected_meal]

st.markdown(f"""
    <div class="menu-card" style="--card-color: {selected_color};">
        <div style="font-size: 26px; font-weight: 800; color: #111; margin-bottom: 12px;">{meal_info['menu']}</div>
        <div style="height: 1px; background-color: #eee; width: 30%; margin: 0 auto;"></div>
        <div style="color: #444; font-size: 16px; margin-top: 15px; line-height: 1.5; word-break: keep-all;">{meal_info['side']}</div>
    </div>
""", unsafe_allow_html=True)

# 7. 인덱스 탭 및 라디오 버튼
tabs_html = '<div class="index-tabs-wrap">'
for meal, color in color_theme.items():
    opacity = "1.0" if meal == st.session_state.selected_meal else "0.3"
    tabs_html += f'<div class="tab-unit" style="background-color: {color}; opacity: {opacity};">{meal}</div>'
tabs_html += '</div>'
st.markdown(tabs_html, unsafe_allow_html=True)

selected = st.radio("식단선택", options=list(color_theme.keys()), 
                    index=list(color_theme.keys()).index(st.session_state.selected_meal),
                    horizontal=True, label_visibility="collapsed")

if selected != st.session_state.selected_meal:
    st.session_state.selected_meal = selected
    st.rerun()

# 8. 시간 메시지
msg = f"💡 {st.session_state.selected_meal} 메뉴를 확인 중입니다."
if st.session_state.selected_meal in meal_times:
    s_t, e_t = meal_times[st.session_state.selected_meal]
    s_dt, e_dt = datetime.combine(d, s_t).replace(tzinfo=KST), datetime.combine(d, e_t).replace(tzinfo=KST)
    if now_dt < s_dt:
        msg = f"⏳ {st.session_state.selected_meal} 시작까지 {(s_dt-now_dt).seconds//3600}시간 {((s_dt-now_dt).seconds%3600)//60}분 남음"
    elif now_dt <= e_dt:
        msg = f"🍴 {st.session_state.selected_meal} 배식 중! 종료까지 {(e_dt-now_dt).seconds//3600}시간 {((e_dt-now_dt).seconds%3600)//60}분 남음"
    else:
        msg = f"🚩 오늘의 {st.session_state.selected_meal} 배식이 종료되었습니다."
st.markdown(f'<div class="timer-box">{msg}</div>', unsafe_allow_html=True)
