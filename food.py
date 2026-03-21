import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, time
from zoneinfo import ZoneInfo

# 1. 기초 설정
KST = ZoneInfo("Asia/Seoul")
def get_now(): return datetime.now(KST)

st.set_page_config(page_title="성의교정 주간식단", page_icon="🍽️", layout="centered")

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

# 3. 날짜 및 상태 관리
params = st.query_params
now_dt = get_now()
today_date = now_dt.date()
d = datetime.strptime(params["d"], "%Y-%m-%d").date() if "d" in params else today_date
selected = params.get("meal", "중식")

# 4. 배식 안내 로직 (기존 스타일)
is_weekend = d.weekday() >= 5
lunch_start = time(11, 30) if is_weekend else time(11, 20)
meal_schedule = {
    "조식": {"start": time(7, 0), "end": time(9, 0)},
    "간편식": {"start": time(7, 0), "end": time(11, 0)}, 
    "중식": {"start": lunch_start, "end": time(14, 0)},
    "석식": {"start": time(17, 20), "end": time(19, 20)},
    "야식": {"start": time(18, 0), "end": time(19, 20)}
}

def get_realtime_status(selected_meal):
    if d != today_date: return f"📅 {d.strftime('%m월 %d일')} {selected_meal} 식단입니다."
    now_t = get_now().time()
    sched = meal_schedule[selected_meal]
    if sched["start"] <= now_t <= sched["end"]:
        return f"✅ 지금은 <span style='color:#8BC34A;'>{selected_meal} 배식 중</span>입니다."
    if now_t < sched["start"]:
        target_dt = datetime.combine(today_date, sched["start"], tzinfo=KST)
        diff = target_dt - get_now()
        h, m = divmod(int(diff.total_seconds() // 60), 60)
        t_str = f"{h}시간 {m}분" if h > 0 else f"{m}분"
        return f"⏳ {selected_meal} 제공까지 {t_str} 남았습니다."
    return f"🏁 {selected_meal} 배식이 종료되었습니다."

# 5. 근무조 및 테마
def get_shift(target_d):
    anchor = datetime(2026, 3, 13).date()
    arr = [{"n":"A조","bg":"#FF9800"}, {"n":"B조","bg":"#E91E63"}, {"n":"C조","bg":"#2196F3"}]
    return arr[(target_d - anchor).days % 3]

weekday_names = ["월", "화", "수", "목", "금", "토", "일"]
wd = d.weekday()
wd_color = "#2196F3" if wd == 5 else "#E91E63" if wd == 6 else "#1E3A5F"
s, colors = get_shift(d), {"조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"}
sel_c = colors.get(selected, "#8BC34A")

# 6. 여백 집중 보정 CSS
st.markdown(f"""
<style>
    [data-testid="stAppViewBlockContainer"] {{ 
        max-width: 400px !important; margin: 0 auto !important; 
        padding-top: 1rem !important; padding-bottom: 1rem !important;
        padding-left: 10px !important; padding-right: 10px !important;
    }}
    header {{ visibility: hidden; }}
    div[data-testid="stVerticalBlock"] {{ gap: 0rem !important; }}

    .main-title {{
        text-align: center; font-size: 24px; font-weight: 900; color: #1E3A5F;
        padding: 5px 0; margin-bottom: 8px; line-height: 1.2;
    }}
    
    .date-box {{ 
        text-align: center; background: #F4F7FF; 
        padding: 6px 10px; border-radius: 15px; font-weight: 800; 
        border: 1px solid #D6DCEC; font-size: 17px; margin-bottom: 5px; line-height: 1.2; 
    }}
    
    .status-msg {{ text-align: center; font-size: 13px; font-weight: 700; color: #555; margin: 10px 0; min-height: 20px; line-height: 1.4; }}
    
    /* 네비게이션 버튼 슬림화 (날짜박스 수준) */
    .nav-row {{ display: flex; justify-content: space-between; gap: 8px; margin-bottom: 12px; }}
    .nav-btn {{ 
        flex: 1; text-align: center; padding: 6px 0; 
        background: white; border: 1px solid #EEE; border-radius: 10px; 
        text-decoration: none; color: #1E3A5F; font-size: 13px; font-weight: 800; 
    }}
    
    .tab-container {{ display: flex; width: 100%; gap: 1px; }}
    .tab-item {{ flex: 1; text-align: center; padding: 12px 0; font-size: 12px; font-weight: 800; color: #333 !important; text-decoration: none; border-radius: 8px 8px 0 0; opacity: 0.5; }}
    .tab-item.active {{ opacity: 1; color: white !important; }}
    
    /* 카드 상단 여백 확보 (텍스트 밀어내기) */
    .menu-card {{
        border: 2px solid {sel_c}; border-top: 4px solid {sel_c}; border-radius: 0 0 15px 15px;
        min-height: 220px; display: flex; flex-direction: column; 
        justify-content: flex-start; /* 위에서부터 배치 */
        align-items: center;
        padding: 40px 20px 20px 20px; /* 상단 패딩(40px)으로 탭과의 간격 확보 */
        background: white; box-shadow: 0 5px 15px rgba(0,0,0,0.05); text-align: center;
    }}
    .main-menu {{ font-size: 20px; font-weight: 900; color: #111; line-height: 1.5; margin-bottom: 15px; }}
    .side-menu {{ color: #666; font-size: 15px; line-height: 1.6; }}
    
    button[title="Manage app"], #MainMenu, footer, .stDeployButton {{ display: none !important; }}
</style>
""", unsafe_allow_html=True)

# 7. UI 구성
st.markdown('<div class="main-title">🍽️ 성의교정 주간식단</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="date-box">
    {d.strftime("%Y.%m.%d")} (<span style="color:{wd_color}">{weekday_names[wd]}</span>)
    <span style="background:{s['bg']}; color:white; padding:2px 8px; border-radius:10px; font-size:12px; margin-left:5px; vertical-align:middle;">{s['n']}</span>
</div>
<div class="status-msg">{get_realtime_status(selected)}</div>

<div class="nav-row">
    <a href="?d={(d-timedelta(1)).strftime('%Y-%m-%d')}&meal={selected}" class="nav-btn" target="_self">PREV</a>
    <a href="?d={today_date}&meal={selected}" class="nav-btn" target="_self">TODAY</a>
    <a href="?d={(d+timedelta(1)).strftime('%Y-%m-%d')}&meal={selected}" class="nav-btn" target="_self">NEXT</a>
</div>
""", unsafe_allow_html=True)

tabs_html = '<div class="tab-container">'
for m, c in colors.items():
    tabs_html += f'<a href="?d={d}&meal={m}" class="tab-item {"active" if m == selected else ""}" style="background:{c}" target="_self">{m}</a>'
st.markdown(tabs_html + '</div>', unsafe_allow_html=True)

# 8. 식단 출력
meal_info = data.get(d.strftime("%Y-%m-%d"), {}).get(selected)
if meal_info and str(meal_info['menu']).strip() not in ["", "nan", "None"]:
    main_m, side_m = meal_info['menu'], meal_info['side']
else:
    main_m = "식단 정보 없음"
    side_m = ""

st.markdown(f"""
<div class="menu-card">
    <div class="main-menu">{main_m}</div>
    <div style="width:30%; height:1px; background:#EEE; margin:15px auto;"></div>
    <div class="side-menu">{side_m}</div>
</div>
""", unsafe_allow_html=True)
