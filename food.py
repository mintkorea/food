import streamlit as st
from datetime import datetime, timedelta, time
from zoneinfo import ZoneInfo

# 1. 시간대 설정 (KST)
KST = ZoneInfo("Asia/Seoul")
def today_kst(): return datetime.now(KST).date()

# 2. 페이지 설정 및 상태 관리
st.set_page_config(page_title="식단 가이드", page_icon="🍴", layout="centered")

if 'target_date' not in st.session_state:
    st.session_state.target_date = today_kst()

# URL 파라미터를 통한 날짜 연동 (대관 소스 로직)
url_params = st.query_params
if "d" in url_params:
    try:
        st.session_state.target_date = datetime.strptime(url_params["d"], "%Y-%m-%d").date()
    except: pass

# 3. CSS 스타일 (대관 현황 디자인 이식)
st.markdown("""
<style>
    .block-container { padding: 1rem 1.2rem !important; max-width: 500px !important; }
    header { visibility: hidden; }
    
    /* 날짜 표시 박스 (대관 현황 스타일) */
    .date-display-box { 
        text-align: center; background-color: #F8FAFF; padding: 15px 10px 8px 10px; 
        border-radius: 12px 12px 0 0; border: 1px solid #D1D9E6; border-bottom: none; line-height: 1.2 !important;
    }
    .res-main-title { font-size: 14px !important; font-weight: bold; color: #666; display: block; margin-bottom: 4px; }
    .res-sub-title { font-size: 22px !important; font-weight: 800; color: #1E3A5F; }
    .sat { color: #4A90E2 !important; } .sun { color: #E95444 !important; }

    /* 네비게이션 바 (Before/Today/Next) */
    .nav-link-bar {
        display: flex !important; width: 100% !important; background: white !important; 
        border: 1px solid #D1D9E6 !important; border-radius: 0 0 10px 10px !important; 
        margin-bottom: 20px !important; overflow: hidden !important;
    }
    .nav-item {
        flex: 1 !important; text-align: center !important; padding: 10px 0 !important;
        text-decoration: none !important; color: #1E3A5F !important; font-weight: bold !important; 
        border-right: 1px solid #F0F0F0 !important; font-size: 13px !important;
    }
    .nav-item:last-child { border-right: none !important; }

    /* 메뉴 카드 및 라디오 버튼 */
    .menu-card { border: 3px solid var(--card-color); border-radius: 20px; padding: 30px 15px; text-align: center; background: white; margin-bottom: 15px; }
    div[data-testid="stRadio"] > div { display: flex !important; flex-wrap: nowrap !important; justify-content: center; }
</style>
""", unsafe_allow_html=True)

# 4. 날짜 및 요일 계산
d = st.session_state.target_date
w_idx = d.weekday()
day_names = ["월", "화", "수", "목", "금", "토", "일"]
w_str = day_names[w_idx]
w_class = "sat" if w_idx == 5 else ("sun" if w_idx == 6 else "")

# 5. 상단 날짜 표시 및 네비게이션 (요청하신 로직)
st.markdown(f"""
<div class="date-display-box">
    <span class="res-main-title">오늘의 식단 가이드</span>
    <span class="res-sub-title">{d.strftime("%m월 %d일")} <span class="{w_class}">({w_str})</span></span>
</div>
<div class="nav-link-bar">
    <a href="./?d={(d-timedelta(1)).strftime('%Y-%m-%d')}" target="_self" class="nav-item">◀ Before</a>
    <a href="./?d={today_kst().strftime('%Y-%m-%d')}" target="_self" class="nav-item">Today</a>
    <a href="./?d={(d+timedelta(1)).strftime('%Y-%m-%d')}" target="_self" class="nav-item">Next ▶</a>
</div>
""", unsafe_allow_html=True)

# 6. 식단 데이터 로드 (날짜 기반 조회)
# 예시 데이터 (실제 데이터는 DB나 딕셔너리에서 호출)
meal_data = {
    "2026-03-18": {
        "조식": {"menu": "감자수제비", "side": "흰쌀밥, 돈채가지볶음, 양념고추지, 깍두기, 누룽지/원두커피"},
        "중식": {"menu": "뼈없는닭볶음탕", "side": "혼합잡곡밥, 팽이장국, 유부겨자냉채, 흑깨드레싱샐러드, 열무김치"},
    }
}

date_key = d.strftime("%Y-%m-%d")
daily_meals = meal_data.get(date_key, {"조식": {"menu": "정보 없음", "side": "식단 정보가 등록되지 않았습니다."}})

# 7. 식단 선택 및 표시
if 'selected_meal' not in st.session_state:
    st.session_state.selected_meal = "중식"

color_theme = {"조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"}
selected_color = color_theme.get(st.session_state.selected_meal, "#333")
meal_info = daily_meals.get(st.session_state.selected_meal, {"menu": "정보 없음", "side": ""})

st.markdown(f"""
    <div class="menu-card" style="--card-color: {selected_color};">
        <div style="color: {selected_color}; font-size: 14px; font-weight: bold; margin-bottom: 10px;">{st.session_state.selected_meal}</div>
        <div style="font-size: 26px; font-weight: 800; color: #111;">{meal_info['menu']}</div>
        <div style="height: 1px; background-color: #eee; width: 35%; margin: 20px auto;"></div>
        <div style="color: #444; font-size: 16px; line-height: 1.6;">{meal_info['side']}</div>
    </div>
""", unsafe_allow_html=True)

selected = st.radio("식단선택", options=list(color_theme.keys()), horizontal=True, label_visibility="collapsed")

if selected != st.session_state.selected_meal:
    st.session_state.selected_meal = selected
    st.rerun()
