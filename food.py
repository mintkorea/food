import streamlit as st
from datetime import datetime, timedelta, time
from zoneinfo import ZoneInfo

# 1. 시간대 및 날짜 설정
KST = ZoneInfo("Asia/Seoul")
def today_kst(): return datetime.now(KST).date()

st.set_page_config(page_title="성의교정 식단 가이드", page_icon="🍴", layout="centered")

# 세션 상태 초기화
if 'target_date' not in st.session_state:
    st.session_state.target_date = today_kst()
if 'selected_meal' not in st.session_state:
    st.session_state.selected_meal = "중식"

# URL 파라미터 연동 (대관 현황 로직)
url_params = st.query_params
if "d" in url_params:
    try:
        st.session_state.target_date = datetime.strptime(url_params["d"], "%Y-%m-%d").date()
    except: pass

# 2. 데이터 세트 (제공된 이미지 기반 식단 데이터)
meal_data = {
    "2026-03-18": {
        "조식": {"menu": "감자수제비", "side": "흰쌀밥, 돈채가지볶음, 양념고추지, 깍두기, 누룽지/원두커피"},
        "간편식": {"menu": "닭가슴살샐러드 & 바나나", "side": "신선한 과일과 채소"},
        "중식": {"menu": "뼈없는닭볶음탕", "side": "혼합잡곡밥, 팽이장국, 유부겨자냉채, 흑깨드레싱샐러드, 열무김치, 복분자주스"},
        "석식": {"menu": "하이디라오마라탕", "side": "분모자+포두부+소세지 & 탕수육, 후르츠소스, 흰쌀밥, 짜사이무침, 열무김치"},
        "야식": {"menu": "돈사태떡찜", "side": "흰쌀밥, 유채된장국, 땅콩드레싱샐러드, 멸치볶음, 양파장아찌, 요구르트"}
    },
    "2026-03-19": {
        "조식": {"menu": "시래기장터국밥", "side": "모듬땡전, 케첩, 흰쌀밥, 치커리유자무침, 깍두기"},
        "중식": {"menu": "통등심돈까스 & 데미소스", "side": "비빔막국수, 추가쌀밥, 미역국, 사우전드레싱샐러드, 깍두기"},
        "석식": {"menu": "돼지목살필라프", "side": "우동장국, 삼색푸실리케찹볶음, 단무지무침, 포기김치"},
        "야식": {"menu": "함박스테이크", "side": "흰쌀밥, 콩가루배춧국, 실곤약초무침, 오복채, 열무김치"}
    }
}

color_theme = {"조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"}
meal_times = {
    "조식": (time(7, 0), time(9, 0)),
    "중식": (time(11, 20), time(14, 0)),
    "석식": (time(17, 20), time(19, 20))
}

# 3. CSS (대관 현황 헤더 + 식단 앱 인덱스 탭 통합)
d = st.session_state.target_date
w_idx = d.weekday()
w_str, w_class = ["월","화","수","목","금","토","일"][w_idx], ("sat" if w_idx == 5 else ("sun" if w_idx == 6 else ""))

st.markdown(f"""
<style>
    .block-container {{ padding: 1rem 1.2rem !important; max-width: 500px !important; }}
    header {{ visibility: hidden; }}
    
    /* 대관 현황 스타일 헤더 */
    .date-display-box {{ 
        text-align: center; background-color: #F8FAFF; padding: 15px 10px 8px 10px; 
        border-radius: 12px 12px 0 0; border: 1px solid #D1D9E6; border-bottom: none;
    }}
    .res-main-title {{ font-size: 20px !important; font-weight: 800; color: #1E3A5F; display: block; margin-bottom: 4px; }}
    .res-sub-title {{ font-size: 18px !important; font-weight: 700; color: #333; }}
    .sat {{ color: #0000FF !important; }} .sun {{ color: #FF0000 !important; }}

    .nav-link-bar {{
        display: flex !important; width: 100% !important; background: white !important; 
        border: 1px solid #D1D9E6 !important; border-radius: 0 0 10px 10px !important; 
        margin-bottom: 25px !important; overflow: hidden !important;
    }}
    .nav-item {{
        flex: 1 !important; text-align: center !important; padding: 10px 0 !important;
        text-decoration: none !important; color: #1E3A5F !important; font-weight: bold !important; 
        border-right: 1px solid #F0F0F0 !important; font-size: 13px !important;
    }}

    /* 식단 카드 및 인덱스 탭 */
    .menu-card {{ border: 3px solid var(--card-color); border-radius: 20px 20px 0 0; padding: 30px 15px; text-align: center; background: white; }}
    .index-tabs-wrap {{ display: flex; width: 100%; margin-top: -3px; }}
    .tab-unit {{ flex: 1; text-align: center; padding: 10px 0; font-size: 13px !important; font-weight: bold; color: white; }}

    /* 라디오 버튼 한 줄 고정 고정 */
    div[data-testid="stRadio"] > div {{
        display: flex !important; flex-wrap: nowrap !important; 
        background-color: #f1f3f5; padding: 10px 2px !important; border-radius: 0 0 20px 20px;
    }}
    div[data-testid="stRadio"] label p {{ font-size: 13px !important; font-weight: 800 !important; white-space: nowrap !important; }}
    
    .timer-box {{ text-align: center; background-color: #f8f9fa; padding: 12px; border-radius: 12px; font-size: 14px; font-weight: bold; color: #555; margin-top: 15px; }}
</style>
""", unsafe_allow_html=True)

# 4. 상단 네비게이션 출력
st.markdown(f"""
<div class="date-display-box">
    <span class="res-main-title">🍽️ 성의교정 주간 식단</span>
    <span class="res-sub-title">{d.strftime("%Y.%m.%d")}.<span class="{w_class}">({w_str})</span></span>
</div>
<div class="nav-link-bar">
    <a href="./?d={(d-timedelta(1)).strftime('%Y-%m-%d')}" target="_self" class="nav-item">◀ Before</a>
    <a href="./?d={today_kst().strftime('%Y-%m-%d')}" target="_self" class="nav-item">Today</a>
    <a href="./?d={(d+timedelta(1)).strftime('%Y-%m-%d')}" target="_self" class="nav-item">Next ▶</a>
</div>
""", unsafe_allow_html=True)

# 5. 식단 카드 표시
date_key = d.strftime("%Y-%m-%d")
meal_info = meal_data.get(date_key, {}).get(st.session_state.selected_meal, {"menu": "정보 없음", "side": "식단 정보가 등록되지 않았습니다."})
selected_color = color_theme[st.session_state.selected_meal]

st.markdown(f"""
    <div class="menu-card" style="--card-color: {selected_color};">
        <div style="color: {selected_color}; font-size: 14px; font-weight: bold; margin-bottom: 8px;">{st.session_state.selected_meal}</div>
        <div style="font-size: 26px; font-weight: 800; color: #111; margin-bottom: 12px;">{meal_info['menu']}</div>
        <div style="height: 1px; background-color: #eee; width: 35%; margin: 0 auto;"></div>
        <div style="color: #444; font-size: 16px; margin-top: 15px; line-height: 1.6; word-break: keep-all;">{meal_info['side']}</div>
    </div>
""", unsafe_allow_html=True)

# 6. 인덱스 탭 (복구)
tabs_html = '<div class="index-tabs-wrap">'
for meal, color in color_theme.items():
    opacity = "1.0" if meal == st.session_state.selected_meal else "0.3"
    tabs_html += f'<div class="tab-unit" style="background-color: {color}; opacity: {opacity};">{meal}</div>'
tabs_html += '</div>'
st.markdown(tabs_html, unsafe_allow_html=True)

# 7. 라디오 버튼 (복구 및 한 줄 고정)
selected = st.radio("식단선택", options=list(color_theme.keys()), 
                    index=list(color_theme.keys()).index(st.session_state.selected_meal),
                    horizontal=True, label_visibility="collapsed")

if selected != st.session_state.selected_meal:
    st.session_state.selected_meal = selected
    st.rerun()

# 8. 식사 제공 시간 및 남은 시간 표시 (복구)
now_dt = datetime.now(KST)
curr_t = now_dt.time()
msg = f"💡 {st.session_state.selected_meal} 메뉴를 확인 중입니다."

if st.session_state.selected_meal in meal_times:
    s_t, e_t = meal_times[st.session_state.selected_meal]
    s_dt, e_dt = datetime.combine(d, s_t).replace(tzinfo=KST), datetime.combine(d, e_t).replace(tzinfo=KST)
    
    if now_dt < s_dt:
        diff = s_dt - now_dt
        msg = f"⏳ {st.session_state.selected_meal} 시작까지 {diff.seconds//3600}시간 {(diff.seconds%3600)//60}분 남음"
    elif now_dt <= e_dt:
        diff = e_dt - now_dt
        msg = f"🍴 {st.session_state.selected_meal} 배식 중! 종료까지 {diff.seconds//3600}시간 {(diff.seconds%3600)//60}분 남음"
    else:
        msg = f"🚩 {d.strftime('%m/%d')} {st.session_state.selected_meal} 배식이 종료되었습니다."

st.markdown(f'<div class="timer-box">{msg}</div>', unsafe_allow_html=True)
