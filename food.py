import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, time
from zoneinfo import ZoneInfo

# 1. 기초 설정
KST = ZoneInfo("Asia/Seoul")
def get_now(): return datetime.now(KST)

st.set_page_config(page_title="성의교정 주간식단", page_icon="🍽️", layout="centered")

# 2. 데이터 로드 (구글 시트)
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

# 3. 시간 스케줄 정의 함수
def get_meal_schedule(is_weekend):
    lunch_start = time(11, 30) if is_weekend else time(11, 20)
    return {
        "조식": {"start": time(7, 0), "end": time(9, 0)},
        "간편식": {"start": time(7, 0), "end": time(11, 0)}, 
        "중식": {"start": lunch_start, "end": time(14, 0)},
        "석식": {"start": time(17, 20), "end": time(19, 20)},
        "야식": {"start": time(18, 0), "end": time(19, 20)}
    }

# 4. 날짜 및 상태 관리
params = st.query_params
now_dt = get_now()
today_date = now_dt.date()
now_t = now_dt.time()
schedule = get_meal_schedule(today_date.weekday() >= 5)

# 날짜 결정
d = datetime.strptime(params["d"], "%Y-%m-%d").date() if "d" in params else today_date
d_str = d.strftime("%Y-%m-%d")

# 식단 선택 (자동 전환 로직)
if "meal" in params:
    selected = params["meal"]
else:
    if d == today_date:
        if now_t <= schedule["조식"]["end"]: selected = "조식"
        elif now_t <= schedule["중식"]["end"]: selected = "중식"
        else: selected = "석식"
    else: selected = "중식"

# 식단 데이터 존재 여부 확인
meal_info = data.get(d_str, {}).get(selected)
meal_exists = meal_info and str(meal_info['menu']).strip() not in ["", "nan", "None", "식단 정보 없음"]

# 5. 상태 메시지 로직 (기존 유지)
def get_realtime_status(selected_meal):
    if d != today_date:
        return f"📅 {d.strftime('%m월 %d일')} {selected_meal} 식단입니다."
    
    # 공통: 현재 선택한 식단의 스케줄
    curr_sched = schedule[selected_meal]
    
    if curr_sched["start"] <= now_t <= curr_sched["end"]:
        return f"✅ 지금은 <span style='color:#8BC34A;'>{selected_meal} 배식 중</span>입니다."
    
    if now_t < curr_sched["start"]:
        diff = datetime.combine(today_date, curr_sched["start"], tzinfo=KST) - get_now()
        total_m = int(diff.total_seconds() // 60)
        h, m = divmod(total_m, 60)
        t_str = f"{h}시간 {m}분" if h > 0 else f"{m}분"
        return f"⏳ {selected_meal} 제공까지 {t_str} 남았습니다."

    if selected_meal in ["간편식", "야식"]:
        return f"🏁 오늘 {selected_meal} 배식은 종료되었습니다."
    
    main_order = ["조식", "중식", "석식"]
    next_main = None
    for m_name in main_order:
        if now_t < schedule[m_name]["start"]:
            next_main = m_name
            break
            
    if next_main:
        target_dt = datetime.combine(today_date, schedule[next_main]["start"], tzinfo=KST)
        diff = target_dt - get_now()
        total_m = int(diff.total_seconds() // 60)
        h, m = divmod(total_m, 60)
        t_str = f"{h}시간 {m}분" if h > 0 else f"{m}분"
        return f"🏁 {selected_meal} 배식 종료! 다음 {next_main}까지 {t_str} 남음"
    
    return "🌙 오늘 모든 배식이 종료되었습니다."

# 6. 근무조 및 컬러 설정 (카드 라인 색상 수정의 핵심)
def get_shift(target_d):
    anchor = datetime(2026, 3, 13).date()
    arr = [{"n":"A조","bg":"#FF9800"}, {"n":"B조","bg":"#E91E63"}, {"n":"C조","bg":"#2196F3"}]
    return arr[(target_d - anchor).days % 3]

weekday_names = ["월", "화", "수", "목", "금", "토", "일"]
wd = d.weekday()
wd_color = "#2196F3" if wd == 5 else "#E91E63" if wd == 6 else "#1E3A5F"
s = get_shift(d)

# 핵심: 탭 색상과 카드 라인 색상을 selected에 맞춰 통일
colors = {"조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"}
# 선택된 식단의 색상 가져오기 (기본값은 중식 색상)
sel_c = colors.get(selected, "#8BC34A")

# 7. 스타일 CSS (카드 테두리 색상을 sel_c 변수로 변경)
st.markdown(f"""
<style>
    [data-testid="stAppViewBlockContainer"] {{ max-width: 420px !important; margin: 0 auto !important; padding-top: 0.5rem !important; }}
    header {{ visibility: hidden; }}
    .main-title {{ text-align: center; font-size: 22px; font-weight: 900; color: #1E3A5F; margin-bottom: 24px; }}
    .date-box {{ text-align: center; background: #F4F7FF; padding: 4px; border-radius: 15px; font-weight: 800; border: 1px solid #D6DCEC; font-size: 16px; margin-bottom: 10px; }}
    .status-msg {{ text-align: center; font-size: 14px; font-weight: 700; color: #555; margin-bottom: 15px; min-height: 20px; }}
    .nav-row {{ display: flex; justify-content: space-between; gap: 8px; margin-bottom: 20px; }}
    .nav-btn {{ flex: 1; text-align: center; padding: 6px 0; background: white; border: 1px solid #EEE; border-radius: 8px; text-decoration: none; color: #1E3A5F; font-size: 13px; font-weight: 800; }}
    .tab-container {{ display: flex; width: 100%; gap: 1px; }}
    .tab-item {{ flex: 1; text-align: center; padding: 6px 0 20px 0; font-size: 12px; font-weight: 800; color: white !important; text-decoration: none; border-radius: 10px 10px 0 0; opacity: 0.6; }}
    .tab-item.active {{ opacity: 1; }}
    
    /* 핵심 수정: 카드 테두리 색상(border)을 선택된 식단의 색상({sel_c})으로 변경 */
    .menu-card {{
        border: 1.5px solid {sel_c}; /* 보라색 고정 해제 -> sel_c로 변경 */
        border-top: 5px solid {sel_c};
        border-radius: 0 0 20px 20px;
        min-height: 210px; display: flex; flex-direction: column; 
        justify-content: center; align-items: center;
        padding: 20px; background: white; text-align: center; margin-top: -1px;
    }}
    
    .main-menu {{ font-size: 20px; font-weight: 900; color: #111; margin-bottom: 15px; line-height: 1.4; }}
    .side-menu {{ color: #777; font-size: 15px; line-height: 1.6; }}
    button[title="Manage app"], #MainMenu, footer, .stDeployButton {{ display: none !important; }}
</style>
""", unsafe_allow_html=True)

# 8. UI 구성 (출력 부분)
st.markdown('<div class="main-title">🍽️ 성의교정 주간식단</div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="date-box">
    {d.strftime("%Y.%m.%d")} (<span style="color:{wd_color}">{weekday_names[wd]}</span>)
    <span style="background:{s['bg']}; color:white; padding:1px 8px; border-radius:10px; font-size:11px; margin-left:5px; vertical-align:middle;">{s['n']}</span>
</div>
<div class="status-msg">{get_realtime_status(selected)}</div>
<div class="nav-row">
    <a href="?d={(d-timedelta(1)).strftime('%Y-%m-%d')}&meal={selected}" class="nav-btn" target="_self">PREV</a>
    <a href="?d={today_date}&meal={selected}" class="nav-btn" target="_self">TODAY</a>
    <a href="?d={(d+timedelta(1)).strftime('%Y-%m-%d')}&meal={selected}" class="nav-btn" target="_self">NEXT</a>
</div>
""", unsafe_allow_html=True)

# 탭 메뉴 (여기에 colors 변수가 사용됨)
tabs_html = '<div class="tab-container">'
for m, c in colors.items():
    active_class = "active" if m == selected else ""
    tabs_html += f'<a href="?d={d_str}&meal={m}" class="tab-item {active_class}" style="background:{c}" target="_self">{m}</a>'
st.markdown(tabs_html + '</div>', unsafe_allow_html=True)

# 식단 출력
if meal_exists:
    main_m, side_m = meal_info['menu'], meal_info['side']
else:
    main_m = "오늘은 간편식을 제공하지 않습니다." if selected == "간편식" else "아직 식단 정보가 업데이트 되지 않았습니다"
    side_m = ""

# 여기에 .menu-card 클래스가 적용되어 테두리 색상이 바뀝니다.
st.markdown(f"""
<div class="menu-card">
    <div class="main-menu">{main_m}</div>
    <div style="width:40px; height:1px; background:#EEE; margin-bottom:15px;"></div>
    <div class="side-menu">{side_m}</div>
</div>
""", unsafe_allow_html=True)
