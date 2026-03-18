import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, time
from zoneinfo import ZoneInfo

# 1. 기초 설정 및 시간대
KST = ZoneInfo("Asia/Seoul")
def get_now(): return datetime.now(KST)

st.set_page_config(page_title="성의교정 식단 가이드", page_icon="🍴", layout="centered")

# [데이터 로딩 캐싱]
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
            structured_data[d_str][m_type] = {"menu": row['menu'], "side": row['side']}
        return structured_data
    except: return {}

# 2. 세션 초기화 및 데이터 로드
CSV_URL = "https://docs.google.com/spreadsheets/d/1l07s4rubmeB5ld8oJayYrstL34UPKtxQwYptIocgKV0/export?format=csv"
meal_data = load_meal_data(CSV_URL)
now = get_now()

if 'target_date' not in st.session_state:
    st.session_state.target_date = now.date()

color_theme = {"조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"}

if 'selected_meal' not in st.session_state:
    t = now.time()
    if t < time(9, 0): st.session_state.selected_meal = "조식"
    elif t < time(14, 0): st.session_state.selected_meal = "중식"
    elif t < time(19, 20): st.session_state.selected_meal = "석식"
    else: st.session_state.selected_meal = "중식"

# 3. CSS (스크린샷 디자인 재현 및 깨짐 방지)
st.markdown(f"""
<style>
    .block-container {{ padding: 1rem 1rem !important; max-width: 480px !important; }}
    header {{ visibility: hidden; }}
    
    /* 날짜 헤더 */
    .header-date {{ text-align: center; font-size: 24px; font-weight: 800; color: #333; margin: 10px 0; }}
    
    /* 식단 카드: 상단 굵은 컬러 테두리 */
    .menu-card {{ 
        border: 2px solid #ddd; border-top: 15px solid var(--c); /* 상단 컬러 띠 강조 */
        border-radius: 20px; padding: 30px 15px; text-align: center; 
        background: white; min-height: 180px; margin-bottom: 5px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }}
    
    /* 탭 바 레이아웃 (스크린샷 복구) */
    .tab-bar {{ display: flex; width: 100%; border-radius: 5px; overflow: hidden; margin-bottom: -10px; }}
    .tab-item {{ flex: 1; text-align: center; padding: 10px 0; font-size: 12px; font-weight: bold; color: white; border: 0.5px solid rgba(255,255,255,0.2); }}

    /* 라디오 버튼을 투명하게 만들어 탭과 겹치기 */
    div[data-testid="stRadio"] > div {{ 
        display: flex !important; flex-direction: row !important; 
        gap: 0px !important; background: transparent !important; padding: 0 !important;
    }}
    div[data-testid="stRadio"] label {{ 
        flex: 1; justify-content: center !important; background: #f8f9fa; 
        border: 1px solid #eee; border-radius: 0 0 10px 10px !important; padding: 8px 0 !important;
    }}
    div[data-testid="stRadio"] label p {{ font-size: 11px !important; font-weight: 800; }}
    
    /* 선택된 라디오 효과 */
    div[data-testid="stRadio"] label[data-selected="true"] {{ background: #eee !important; border-top: 2px solid #333; }}

    .msg-box {{ text-align: center; background: #f1f3f5; padding: 12px; border-radius: 12px; font-size: 14px; font-weight: bold; color: #444; margin-top: 15px; }}
</style>
""", unsafe_allow_html=True)

# 4. 화면 구현
d = st.session_state.target_date
w_list = ["월","화","수","목","금","토","일"]

st.markdown(f'<div class="header-date">📅 {d.strftime("%m월 %d일")} ({w_list[d.weekday()]})</div>', unsafe_allow_html=True)

# 날짜 네비게이션
c1, c2, c3 = st.columns(3)
with c1: 
    if st.button("◀ 이전날", use_container_width=True): st.session_state.target_date -= timedelta(1); st.rerun()
with c2:
    if st.button("오늘", use_container_width=True): st.session_state.target_date = now.date(); st.rerun()
with c3:
    if st.button("다음날 ▶", use_container_width=True): st.session_state.target_date += timedelta(1); st.rerun()

# 식단 정보 가져오기
meal_info = meal_data.get(d.strftime("%Y-%m-%d"), {}).get(st.session_state.selected_meal, {"menu": "정보 없음", "side": "식단 정보가 없습니다."})
sel_color = color_theme[st.session_state.selected_meal]

# 식단 카드 표시
st.markdown(f"""
    <div class="menu-card" style="--c: {sel_color};">
        <div style="color: {sel_color}; font-size: 15px; font-weight: 800; margin-bottom: 10px;">{st.session_state.selected_meal}</div>
        <div style="font-size: 26px; font-weight: 800; color: #111; margin-bottom: 15px;">{meal_info['menu']}</div>
        <div style="color: #444; font-size: 16px; line-height: 1.5; word-break: keep-all;">{meal_info['side']}</div>
    </div>
""", unsafe_allow_html=True)

# [스크린샷 디자인 재현] 상단 컬러 탭 바
tab_html = '<div class="tab-bar">'
for m, c in color_theme.items():
    opacity = "1" if m == st.session_state.selected_meal else "0.4"
    tab_html += f'<div class="tab-item" style="background:{c}; opacity:{opacity};">{m}</div>'
tab_html += '</div>'
st.markdown(tab_html, unsafe_allow_html=True)

# 실제 동작용 라디오 버튼
selected = st.radio("select", options=list(color_theme.keys()), 
                    index=list(color_theme.keys()).index(st.session_state.selected_meal), 
                    horizontal=True, label_visibility="collapsed")

if selected != st.session_state.selected_meal:
    st.session_state.selected_meal = selected
    st.rerun()

# 5. 시간 메시지
st.markdown(f'<div class="msg-box">⏳ 현재 {st.session_state.selected_meal} 배식 시간대를 확인 중입니다.</div>', unsafe_allow_html=True)
