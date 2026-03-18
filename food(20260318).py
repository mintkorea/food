import streamlit as st
import requests
from datetime import datetime, timedelta, time
from zoneinfo import ZoneInfo

# 1. 기본 설정
KST = ZoneInfo("Asia/Seoul")
def get_now(): return datetime.now(KST)

st.set_page_config(page_title="성의교정 식단 가이드", page_icon="🍴", layout="centered")

# ✅ 2. 데이터 로딩 (초고속 버전)
@st.cache_data(ttl=3600)
def load_meal_data(url):
    try:
        res = requests.get(url)
        text = res.text.splitlines()

        headers = text[0].split(",")
        idx_date = headers.index("date")
        idx_type = headers.index("meal_type")
        idx_menu = headers.index("menu")
        idx_side = headers.index("side")

        data = {}

        for line in text[1:]:
            cols = line.split(",")

            d = cols[idx_date].strip()
            m = cols[idx_type].strip()

            if d not in data:
                data[d] = {}

            data[d][m] = {
                "menu": cols[idx_menu],
                "side": cols[idx_side]
            }

        return data

    except Exception as e:
        st.error(f"데이터 오류: {e}")
        return {}

CSV_URL = "https://docs.google.com/spreadsheets/d/1l07s4rubmeB5ld8oJayYrstL34UPKtxQwYptIocgKV0/export?format=csv"

meal_data = load_meal_data(CSV_URL)

# 3. 세션 상태
now = get_now()
curr_date = now.date()

if "target_date" not in st.session_state:
    st.session_state.target_date = curr_date

def get_default_meal():
    t = now.time()
    if t < time(9, 0): return "조식"
    if t < time(14, 0): return "중식"
    if t < time(19, 20): return "석식"
    return "중식"

if "selected_meal" not in st.session_state:
    st.session_state.selected_meal = get_default_meal()

# 4. 근무조
def get_work_shift(target_date):
    anchor = datetime(2026, 3, 13).date()
    diff = (target_date - anchor).days
    shifts = [
        {"n": "A조", "bg": "#FF9800"},
        {"n": "B조", "bg": "#E91E63"},
        {"n": "C조", "bg": "#2196F3"}
    ]
    return shifts[diff % 3]

# 5. 스타일
st.markdown("""
<style>
.block-container { padding: 1rem; max-width: 500px; }
header { visibility: hidden; }
.menu-card {
    border-radius: 20px;
    padding: 25px;
    text-align: center;
    background: white;
}
</style>
""", unsafe_allow_html=True)

# 6. 날짜 네비 (🔥 새로고침 없는 방식)
col1, col2, col3 = st.columns(3)

if col1.button("◀"):
    st.session_state.target_date -= timedelta(days=1)

if col2.button("Today"):
    st.session_state.target_date = curr_date

if col3.button("▶"):
    st.session_state.target_date += timedelta(days=1)

d = st.session_state.target_date
shift = get_work_shift(d)

st.markdown(f"""
<div style="text-align:center; font-size:20px; font-weight:bold;">
{d.strftime("%Y.%m.%d")} ({["월","화","수","목","금","토","일"][d.weekday()]})
</div>
<div style="text-align:center; margin-bottom:10px;">
<span style="background:{shift['bg']}; color:white; padding:4px 10px; border-radius:10px;">
{shift['n']}
</span>
</div>
""", unsafe_allow_html=True)

# 7. 식단 데이터
date_key = d.strftime("%Y-%m-%d")
day_meals = meal_data.get(date_key, {})

color_theme = {
    "조식": "#E95444",
    "중식": "#8BC34A",
    "석식": "#4A90E2",
    "간편식": "#F1A33B",
    "야식": "#673AB7"
}

meal_info = day_meals.get(
    st.session_state.selected_meal,
    {"menu": "정보 없음", "side": "등록되지 않음"}
)

# 8. 카드
st.markdown(f"""
<div class="menu-card" style="border:3px solid {color_theme[st.session_state.selected_meal]};">
    <div style="font-size:24px; font-weight:800;">
        {meal_info['menu']}
    </div>
    <div style="margin-top:10px; color:#555;">
        {meal_info['side']}
    </div>
</div>
""", unsafe_allow_html=True)

# 9. 식사 선택 (🔥 rerun 제거)
selected = st.radio(
    "",
    list(color_theme.keys()),
    horizontal=True,
    index=list(color_theme.keys()).index(st.session_state.selected_meal)
)

st.session_state.selected_meal = selected

# 10. 시간 메시지
meal_times = {
    "조식": (time(7, 0), time(9, 0)),
    "중식": (time(11, 20), time(14, 0)),
    "석식": (time(17, 20), time(19, 20))
}

msg = "💡 식단 확인 중"

if selected in meal_times:
    s_t, e_t = meal_times[selected]
    t_s = datetime.combine(d, s_t).replace(tzinfo=KST)
    t_e = datetime.combine(d, e_t).replace(tzinfo=KST)

    if d < curr_date:
        msg = "🚩 종료된 식단"
    elif d > curr_date:
        msg = "🗓️ 예정된 식단"
    else:
        if now < t_s:
            diff = t_s - now
            msg = f"⏳ {diff.seconds//3600}시간 {(diff.seconds%3600)//60}분 남음"
        elif now <= t_e:
            msg = "🍴 배식 중"
        else:
            msg = "🚩 종료됨"

st.markdown(f"<div style='text-align:center; margin-top:10px;'>{msg}</div>", unsafe_allow_html=True)