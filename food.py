import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, time
from zoneinfo import ZoneInfo

# 1. 기초 설정
KST = ZoneInfo("Asia/Seoul")
def get_now(): return datetime.now(KST)

st.set_page_config(page_title="성의교정 식단", page_icon="🍽️", layout="centered")

# 2. 데이터 로드
@st.cache_data(ttl=600)
def load_data(url):
    try:
        df = pd.read_csv(url)
        result = {}
        for _, r in df.iterrows():
            d = str(r['date']).strip()
            m = str(r['meal_type']).strip()
            result.setdefault(d, {})[m] = {"menu": str(r['menu']), "side": str(r['side'])}
        return result
    except: return {}

URL = "https://docs.google.com/spreadsheets/d/1l07s4rubmeB5ld8oJayYrstL34UPKtxQwYptIocgKV0/export?format=csv"
data = load_data(URL)

# 3. 날짜 관리
params = st.query_params
now_dt = get_now()
today_date = now_dt.date()

if "d" in params:
    try: d = datetime.strptime(params["d"], "%Y-%m-%d").date()
    except: d = today_date
else: d = today_date

# 4. 식사 시간 정의 (야식 시작 시간 18:00로 수정)
is_weekend = d.weekday() >= 5
lunch_start = time(11, 30) if is_weekend else time(11, 20)

meal_schedule = {
    "조식": {"start": time(7, 0), "end": time(9, 0)},
    "간편식": {"start": time(7, 0), "end": time(11, 0)}, 
    "중식": {"start": lunch_start, "end": time(14, 0)},
    "석식": {"start": time(17, 20), "end": time(19, 20)},
    "야식": {"start": time(18, 0), "end": time(19, 20)}  # 18:00 시작으로 수정
}

# 5. 상태 메시지 로직
def get_realtime_status(selected_meal):
    if d != today_date:
        return f"📅 {d.strftime('%m월 %d일')} {selected_meal} 식단입니다."
    
    now_t = get_now().time()
    sched = meal_schedule[selected_meal]
    
    # 배식 중일 때
    if sched["start"] <= now_t <= sched["end"]:
        if selected_meal == "간편식":
            return "🍱 간편식 <span style='color:#8BC34A;'>배식 중</span> (사전예약분 및 현장판매)"
        if selected_meal == "야식":
            return "🌙 야식 <span style='color:#8BC34A;'>배식 중</span> (18:00 ~ 19:20)"
        return f"✅ 지금은 <span style='color:#8BC34A;'>{selected_meal} 배식 중</span>입니다."
    
    # 배식 전일 때
    if now_t < sched["start"]:
        target_dt = datetime.combine(today_date, sched["start"], tzinfo=KST)
        diff = target_dt - get_now()
        h, m = divmod(int(diff.total_seconds() // 60), 60)
        t_str = f"{h}시간 {m}분" if h > 0 else f"{m}분"
        
        msg = f"⏳ {selected_meal} 제공까지 {t_str} 남았습니다."
        if selected_meal == "간편식": msg += "<br><span style='font-size:11px; color:#999;'>(조식 시간부터 수령 가능)</span>"
        return msg

    return f"🏁 {selected_meal} 배식이 종료되었습니다."

selected = params.get("meal", "중식")

# 6. 근무조 및 요일
def get_shift(target_d):
    anchor = datetime(2026, 3, 13).date()
    arr = [{"n":"A조","bg":"#FF9800"}, {"n":"B조","bg":"#E91E63"}, {"n":"C조","bg":"#2196F3"}]
    return arr[(target_d - anchor).days % 3]

weekday_names = ["월", "화", "수", "목", "금", "토", "일"]
wd = d.weekday()
wd_color = "#2196F3" if wd == 5 else "#E91E63" if wd == 6 else "#1E3A5F"
s = get_shift(d)
colors = {"조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"}
sel_c = colors.get(selected, "#8BC34A")

# 7. CSS (디자인 고정)
st.markdown(f"""
<style>
    [data-testid="stAppViewBlockContainer"] {{ max-width: 400px !important; margin: 0 auto !important; padding: 1rem 10px !important; }}
    header {{ visibility: hidden; }}
    .date-box {{ text-align: center; background: #F4F7FF; padding: 15px; border-radius: 15px; font-weight: 800; border: 1px solid #D6DCEC; font-size: 18px; }}
    .status-msg {{ text-align: center; font-size: 13px; font-weight: 700; color: #555; margin: 10px 0; min-height: 40px; line-height: 1.5; }}
    .nav-row {{ display: flex; justify-content: space-between; margin-bottom: 10px; gap: 5px; }}
    .nav-btn {{ flex: 1; text-align: center; padding: 10px; background: white; border: 1px solid #EEE; border-radius: 8px; text-decoration: none; color: #1E3A5F; font-size: 13px; font-weight: 700; }}
    .tab-container {{ display: flex; width: 100%; margin-top: 5px; gap: 2px; }}
    .tab-item {{ flex: 1; text-align: center; padding: 12px 0; font-size: 12px; font-weight: 800; color: #333 !important; text-decoration: none; border-radius: 10px 10px 0 0; opacity: 0.6; transition: 0.2s; }}
    .tab-item.active {{ opacity: 1; color: white !important; transform: translateY(-2px); }}
    .menu-card {{
        border: 2px solid {sel_c}; border-top: 5px solid {sel_c}; border-radius: 0 0 20px 20px;
        height: 280px; display: flex; flex-direction: column; justify-content: center; align-items: center;
        padding: 20px; background: white; margin-top: -1px; box-shadow: 0 8px 20px rgba(0,0,0,0.05); text-align: center;
    }}
    .main-menu {{ font-size: 20px; font-weight: 900; color: #111; line-height: 1.4; margin-bottom: 15px; }}
    .side-menu {{ color: #666; font-size: 14px; line-height: 1.6; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }}
</style>
""", unsafe_allow_html=True)

# 8. UI 구성
st.markdown(f"""
<div class="date-box">
    {d.strftime("%Y.%m.%d")} (<span style="color:{wd_color}">{weekday_names[wd]}</span>)
    <span style="background:{s['bg']}; color:white; padding:2px 8px; border-radius:10px; font-size:12px; margin-left:5px; vertical-align:middle;">{s['n']}</span>
</div>
<div class="status-msg">{get_realtime_status(selected)}</div>
<div class="nav-row">
    <a href="?d={(d-timedelta(1)).strftime('%Y-%m-%d')}&meal={selected}" class="nav-btn" target="_self">◀ 이전</a>
    <a href="?d={today_date}&meal={selected}" class="nav-btn" target="_self">오늘</a>
    <a href="?d={(d+timedelta(1)).strftime('%Y-%m-%d')}&meal={selected}" class="nav-btn" target="_self">다음 ▶</a>
</div>
""", unsafe_allow_html=True)

tabs_html = '<div class="tab-container">'
for m, c in colors.items():
    is_active = "active" if m == selected else ""
    tabs_html += f'<a href="?d={d}&meal={m}" class="tab-item {is_active}" style="background:{c}" target="_self">{m}</a>'
st.markdown(tabs_html + '</div>', unsafe_allow_html=True)

# 9. 식단 출력
meal_info = data.get(d.strftime("%Y-%m-%d"), {}).get(selected)
if meal_info and str(meal_info['menu']).strip() not in ["", "nan", "None"]:
    main_m, side_m = meal_info['menu'], meal_info['side']
else:
    main_m = "오늘은 간편식을<br>제공하지 않습니다." if selected == "간편식" else "식단 정보 없음"
    side_m = "" if selected == "간편식" else "해당 일자의 식단이 등록되지 않았습니다."

st.markdown(f"""
<div class="menu-card">
    <div class="main-menu">{main_m}</div>
    <div style="width:30%; height:1.5px; background:#F0F0F0; margin:15px auto;"></div>
    <div class="side-menu">{side_m}</div>
</div>
""", unsafe_allow_html=True)
