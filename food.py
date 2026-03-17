import streamlit as st
from datetime import datetime, timedelta, time
from zoneinfo import ZoneInfo

# 1. 기초 설정 (시간대 및 날짜)
KST = ZoneInfo("Asia/Seoul")
def get_now(): return datetime.now(KST)

st.set_page_config(page_title="식단 가이드", page_icon="🍴", layout="centered")

# 근무조 계산 로직
def get_work_shift(target_date):
    anchor = datetime(2026, 3, 13).date()
    diff = (target_date - anchor).days
    shifts = [{"n": "A조", "bg": "#FF9800"}, {"n": "B조", "bg": "#E91E63"}, {"n": "C조", "bg": "#2196F3"}]
    return shifts[diff % 3]

# 2. 세션 상태 및 자동 선택 로직
now = get_now()
curr_date = now.date()
curr_time = now.time()

def get_default_meal():
    if curr_time < time(9, 0): return "조식"
    if curr_time < time(14, 0): return "중식"
    if curr_time < time(19, 20): return "석식"
    return "중식"

if 'target_date' not in st.session_state:
    st.session_state.target_date = curr_date
if 'selected_meal' not in st.session_state:
    st.session_state.selected_meal = get_default_meal()

# URL 파라미터 동기화
params = st.query_params
if "d" in params:
    try:
        st.session_state.target_date = datetime.strptime(params["d"], "%Y-%m-%d").date()
    except: pass

# 3. 통합 식단 데이터 (날짜 키 확인 필수)
meal_data = {
    "2026-03-17": {
        "중식": {"menu": "버섯불고기", "side": "혼합잡곡밥, 근대국, 쌈채소, 된장, 배추겉절이"},
        "야식": {"menu": "돈사태떡찜", "side": "흰쌀밥, 유채된장국, 땅콩드레싱샐러드, 멸치볶음, 요구르트"}
    },
    "2026-03-18": {
        "조식": {"menu": "감자수제비", "side": "흰쌀밥, 돈채가지볶음, 양념고추지, 깍두기, 누룽지/원두커피"},
        "간편식": {"menu": "닭가슴살샐러드 & 바나나", "side": "신선한 과일과 채소"},
        "중식": {"menu": "뼈없는닭볶음탕", "side": "혼합잡곡밥, 팽이장국, 유부겨자냉채, 흑깨드레싱샐러드, 열무김치, 복분자주스"},
        "석식": {"menu": "하이디라오마라탕", "side": "분모자+포두부+소세지 & 탕수육, 흰쌀밥, 짜사이무침, 열무김치"},
        "야식": {"menu": "돈사태떡찜", "side": "흰쌀밥, 유채된장국, 땅콩드레싱샐러드, 멸치볶음, 요구르트"}
    },
    "2026-03-19": {
        "조식": {"menu": "시래기장터국밥", "side": "모듬땡전, 케첩, 흰쌀밥, 치커리유자무침, 깍두기"},
        "중식": {"menu": "통등심돈까스", "side": "비빔막국수, 추가쌀밥, 미역국, 사우전드레싱샐러드, 깍두기"}
    }
}

color_theme = {"조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"}
meal_times = {"조식": (time(7, 0), time(9, 0)), "중식": (time(11, 20), time(14, 0)), "석식": (time(17, 20), time(19, 20))}

# 4. CSS 및 화면 구성
d = st.session_state.target_date
shift = get_work_shift(d)
w_list = ["월","화","수","목","금","토","일"]
w_str = w_list[d.weekday()]
w_class = "sat" if d.weekday() == 5 else ("sun" if d.weekday() == 6 else "")

st.markdown(f"""
<style>
    .block-container {{ padding: 1rem 1.2rem !important; max-width: 500px !important; }}
    header {{ visibility: hidden; }}
    .date-box {{ text-align: center; background: #F8FAFF; padding: 15px 10px 8px; border-radius: 12px 12px 0 0; border: 1px solid #D1D9E6; border-bottom: none; }}
    .res-main-title {{ font-size: 20px !important; font-weight: 800; color: #1E3A5F; display: block; }}
    .res-sub-title {{ font-size: 18px !important; font-weight: 700; color: #333; }}
    .sat {{ color: #0000FF !important; }} .sun {{ color: #FF0000 !important; }}
    .nav-bar {{ display: flex; width: 100%; background: white; border: 1px solid #D1D9E6; border-radius: 0 0 10px 10px; margin-bottom: 20px; }}
    .nav-btn {{ flex: 1; text-align: center; padding: 10px 0; text-decoration: none; color: #1E3A5F; font-weight: bold; font-size: 13px; border-right: 1px solid #F0F0F0; }}
    .menu-card {{ border: 3px solid var(--c); border-radius: 20px 20px 0 0; padding: 25px 15px; text-align: center; background: white; min-height: 200px; display: flex; flex-direction: column; justify-content: center; }}
    .tab-wrap {{ display: flex; width: 100%; margin-top: -3px; }}
    .tab-item {{ flex: 1; text-align: center; padding: 10px 0; font-size: 12px; font-weight: bold; color: white; }}
    div[data-testid="stRadio"] > div {{ display: flex !important; flex-wrap: nowrap !important; background: #f1f3f5; padding: 10px 2px !important; border-radius: 0 0 20px 20px; }}
    div[data-testid="stRadio"] label p {{ font-size: 12px !important; font-weight: 800 !important; white-space: nowrap !important; }}
    .msg-box {{ text-align: center; background: #f8f9fa; padding: 12px; border-radius: 12px; font-size: 14px; font-weight: bold; color: #555; margin-top: 15px; }}
</style>
""", unsafe_allow_html=True)

# 5. UI 출력
st.markdown(f"""
<div class="date-box">
    <span class="res-main-title">🍽️ 성의교정 주간 식단</span>
    <span class="res-sub-title">{d.strftime("%Y.%m.%d")}.<span class="{w_class}">({w_str})</span>
    <span style="background:{shift['bg']}; color:white; padding:2px 10px; border-radius:12px; font-size:14px; margin-left:5px;">{shift['n']}</span></span>
</div>
<div class="nav-bar">
    <a href="./?d={(d-timedelta(1)).strftime('%Y-%m-%d')}" target="_self" class="nav-btn">◀ Before</a>
    <a href="./?d={curr_date.strftime('%Y-%m-%d')}" target="_self" class="nav-btn">Today</a>
    <a href="./?d={(d+timedelta(1)).strftime('%Y-%m-%d')}" target="_self" class="nav-btn">Next ▶</a>
</div>
""", unsafe_allow_html=True)

# 식단 카드
date_key = d.strftime("%Y-%m-%d")
meal_info = meal_data.get(date_key, {}).get(st.session_state.selected_meal, {"menu": "정보 없음", "side": "식단 정보가 등록되지 않았습니다."})
sel_color = color_theme[st.session_state.selected_meal]

st.markdown(f"""
    <div class="menu-card" style="--c: {sel_color};">
        <div style="font-size: 26px; font-weight: 800; color: #111; margin-bottom: 12px;">{meal_info['menu']}</div>
        <div style="height: 1px; background: #eee; width: 30%; margin: 0 auto;"></div>
        <div style="color: #444; font-size: 16px; margin-top: 15px; line-height: 1.5; word-break: keep-all;">{meal_info['side']}</div>
    </div>
""", unsafe_allow_html=True)

# 탭 및 라디오 버튼
st.markdown('<div class="tab-wrap">' + "".join([f'<div class="tab-item" style="background:{c}; opacity:{"1" if m==st.session_state.selected_meal else "0.3"};">{m}</div>' for m,c in color_theme.items()]) + '</div>', unsafe_allow_html=True)

selected = st.radio("select", options=list(color_theme.keys()), index=list(color_theme.keys()).index(st.session_state.selected_meal), horizontal=True, label_visibility="collapsed")
if selected != st.session_state.selected_meal:
    st.session_state.selected_meal = selected
    st.rerun()

# 6. 시간 메시지 로직 (수정)
msg = f"💡 {st.session_state.selected_meal} 메뉴를 확인 중입니다."
if st.session_state.selected_meal in meal_times:
    s_t, e_t = meal_times[st.session_state.selected_meal]
    t_dt_s = datetime.combine(d, s_t).replace(tzinfo=KST)
    t_dt_e = datetime.combine(d, e_t).replace(tzinfo=KST)

    if d < curr_date:
        msg = "🚩 이미 배식이 종료된 식단입니다."
    elif d > curr_date:
        msg = f"🗓️ {d.strftime('%m/%d')} 배식 예정인 식단입니다."
    else:
        if now < t_dt_s:
            diff = t_dt_s - now
            msg = f"⏳ {st.session_state.selected_meal} 시작까지 {diff.seconds//3600}시간 {(diff.seconds%3600)//60}분 남음"
        elif now <= t_dt_e:
            msg = f"🍴 {st.session_state.selected_meal} 배식 중! 종료까지 {((t_dt_e-now).seconds%3600)//60}분 남음"
        else:
            msg = "🚩 이미 배식이 종료된 식단입니다."

st.markdown(f'<div class="msg-box">{msg}</div>', unsafe_allow_html=True)
