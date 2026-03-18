import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, time
from zoneinfo import ZoneInfo

# 1. 기초 설정 및 시간대
KST = ZoneInfo("Asia/Seoul")
def get_now(): return datetime.now(KST)

st.set_page_config(page_title="성의교정 식단 가이드", page_icon="🍴", layout="centered")

# [개선] 데이터 로딩 함수 (캐싱 강화)
@st.cache_data(ttl=600)
def load_meal_data(url):
    try:
        df = pd.read_csv(url)
        structured_data = {}
        for _, row in df.iterrows():
            d_str = str(row['date']).strip()
            m_type = str(row['meal_type']).strip()
            if d_str not in structured_data:
                structured_data[d_str] = {}
            structured_data[d_str][m_type] = {
                "menu": row['menu'],
                "side": row['side']
            }
        return structured_data
    except Exception as e:
        return {}

# 근무조 계산 함수
def get_work_shift(target_date):
    anchor = datetime(2026, 3, 13).date()
    diff = (target_date - anchor).days
    shifts = [{"n": "A조", "bg": "#FF9800"}, {"n": "B조", "bg": "#E91E63"}, {"n": "C조", "bg": "#2196F3"}]
    return shifts[diff % 3]

# 2. 데이터 불러오기 및 초기화
CSV_URL = "https://docs.google.com/spreadsheets/d/1l07s4rubmeB5ld8oJayYrstL34UPKtxQwYptIocgKV0/export?format=csv"
meal_data = load_meal_data(CSV_URL)

now = get_now()
curr_date = now.date()

# 세션 상태 관리 (속도 개선의 핵심)
if 'target_date' not in st.session_state:
    st.session_state.target_date = curr_date

def get_default_meal():
    t = now.time()
    if t < time(9, 0): return "조식"
    if t < time(14, 0): return "중식"
    if t < time(19, 20): return "석식"
    return "중식"

if 'selected_meal' not in st.session_state:
    st.session_state.selected_meal = get_default_meal()

# 3. 화면 스타일링 (모바일 최적화 CSS)
st.markdown(f"""
<style>
    .block-container {{ padding: 1rem 1.2rem !important; max-width: 500px !important; }}
    header {{ visibility: hidden; }}
    
    /* 날짜 헤더 디자인 */
    .date-box {{ text-align: center; background: #F8FAFF; padding: 15px 10px 8px; border-radius: 12px 12px 0 0; border: 1px solid #D1D9E6; border-bottom: none; }}
    .res-sub-title {{ font-size: 19px !important; font-weight: 800; color: #1E3A5F; }}
    .sat {{ color: #0000FF !important; }} .sun {{ color: #FF0000 !important; }}
    
    /* 식단 카드 디자인 */
    .menu-card {{ 
        border: 3px solid var(--c); border-radius: 20px 20px 0 0; 
        padding: 30px 15px; text-align: center; background: white; 
        min-height: 180px; display: flex; flex-direction: column; justify-content: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }}
    
    /* 라디오 버튼을 탭 버튼처럼 변환 (모바일 가로 꽉 차게) */
    div[data-testid="stRadio"] > div {{ 
        display: flex !important; flex-direction: row !important; 
        background: #f1f3f5; padding: 5px !important; border-radius: 0 0 20px 20px; gap: 4px;
    }}
    div[data-testid="stRadio"] label {{ 
        flex: 1; background: white; border-radius: 10px; padding: 8px 0 !important;
        margin: 0 !important; justify-content: center !important; border: 1px solid #e0e0e0;
    }}
    div[data-testid="stRadio"] label p {{ font-size: 13px !important; font-weight: 800 !important; color: #555; }}
    
    /* 선택된 버튼 강조 */
    div[data-testid="stRadio"] label[data-selected="true"] {{ background: #1E3A5F !important; border: none; }}
    div[data-testid="stRadio"] label[data-selected="true"] p {{ color: white !important; }}

    .msg-box {{ text-align: center; background: #f8f9fa; padding: 12px; border-radius: 12px; font-size: 14px; font-weight: bold; color: #555; margin-top: 15px; }}
</style>
""", unsafe_allow_html=True)

# 상단 제목
st.markdown('<div style="text-align:center; font-size:28px; font-weight:800; color:#1E3A5F; margin-bottom:10px;">🍽️ 성의교정 식단</div>', unsafe_allow_html=True)

# 4. 날짜 네비게이션 (새로고침 없는 방식)
d = st.session_state.target_date
shift = get_work_shift(d)
w_list = ["월","화","수","목","금","토","일"]
w_str = w_list[d.weekday()]
w_class = "sat" if d.weekday() == 5 else ("sun" if d.weekday() == 6 else "")

st.markdown(f"""
<div class="date-box">
    <span class="res-sub-title">{d.strftime("%Y.%m.%d")}.<span class="{w_class}">({w_str})</span>
    <span style="background:{shift['bg']}; color:white; padding:2px 10px; border-radius:12px; font-size:13px; margin-left:5px; vertical-align:middle;">{shift['n']}</span></span>
</div>
""", unsafe_allow_html=True)

# 버튼 클릭 시 세션 상태만 변경 (속도 향상)
col1, col2, col3 = st.columns([1,1,1])
with col1:
    if st.button("◀ 이전날", use_container_width=True):
        st.session_state.target_date -= timedelta(1)
        st.rerun()
with col2:
    if st.button("오늘", use_container_width=True):
        st.session_state.target_date = curr_date
        st.rerun()
with col3:
    if st.button("다음날 ▶", use_container_width=True):
        st.session_state.target_date += timedelta(1)
        st.rerun()

# 5. 식단 표시 및 선택
color_theme = {"조식": "#E95444", "중식": "#8BC34A", "석식": "#4A90E2", "간편식": "#F1A33B"}
meal_times = {"조식": (time(7, 0), time(9, 0)), "중식": (time(11, 20), time(14, 0)), "석식": (time(17, 20), time(19, 20))}

date_key = d.strftime("%Y-%m-%d")
day_meals = meal_data.get(date_key, {})
meal_info = day_meals.get(st.session_state.selected_meal, {"menu": "정보 없음", "side": "식단 정보가 등록되지 않았습니다."})
sel_color = color_theme.get(st.session_state.selected_meal, "#333")

# 식단 카드 렌더링
st.markdown(f"""
    <div class="menu-card" style="--c: {sel_color};">
        <div style="font-size: 26px; font-weight: 800; color: #111; margin-bottom: 12px;">{meal_info['menu']}</div>
        <div style="height: 1px; background: #eee; width: 30%; margin: 0 auto;"></div>
        <div style="color: #444; font-size: 16px; margin-top: 15px; line-height: 1.5; word-break: keep-all;">{meal_info['side']}</div>
    </div>
""", unsafe_allow_html=True)

# 탭 버튼 대용 라디오 버튼
selected = st.radio(
    "식사선택", 
    options=list(color_theme.keys()), 
    index=list(color_theme.keys()).index(st.session_state.selected_meal), 
    horizontal=True, 
    label_visibility="collapsed",
    key="meal_selector"
)

# 선택 변경 시 세션 업데이트 및 즉시 반영
if selected != st.session_state.selected_meal:
    st.session_state.selected_meal = selected
    st.rerun()

# 6. 시간 메시지 로직
msg = "💡 식단 정보를 확인 중입니다."
if st.session_state.selected_meal in meal_times:
    s_t, e_t = meal_times[st.session_state.selected_meal]
    t_dt_s = datetime.combine(d, s_t).replace(tzinfo=KST)
    t_dt_e = datetime.combine(d, e_t).replace(tzinfo=KST)

    if d < curr_date:
        msg = "🚩 배식이 종료된 식단입니다."
    elif d > curr_date:
        msg = f"🗓️ {d.strftime('%m/%d')} 배식 예정입니다."
    else:
        if now < t_dt_s:
            diff = t_dt_s - now
            msg = f"⏳ {st.session_state.selected_meal} 시작까지 {diff.seconds//3600}시간 {(diff.seconds%3600)//60}분 남음"
        elif now <= t_dt_e:
            msg = f"🍴 {st.session_state.selected_meal} 배식 중! 종료까지 {((t_dt_e-now).seconds%3600)//60}분 남음"
        else:
            msg = "🚩 오늘 배식이 종료되었습니다."

st.markdown(f'<div class="msg-box">{msg}</div>', unsafe_allow_html=True)
