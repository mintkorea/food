import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, time
from zoneinfo import ZoneInfo

# 1. 기초 설정 (KST 시간대)
KST = ZoneInfo("Asia/Seoul")
def get_now(): return datetime.now(KST)

st.set_page_config(page_title="성의교정 식단 가이드", page_icon="🍴", layout="centered")

# [캐시 설정 변경] ttl을 0으로 설정하여 테스트 시 즉각 반영되도록 함
@st.cache_data(ttl=0) 
def load_meal_data(url):
    try:
        df = pd.read_csv(url)
        structured_data = {}
        for _, row in df.iterrows():
            d_str = str(row['date']).strip()
            m_type = str(row['meal_type']).strip()
            if d_str not in structured_data: structured_data[d_str] = {}
            structured_data[d_str][m_type] = {"menu": row['menu'], "side": row['side']}
        return structured_data
    except: return {}

# 2. 상태 관리 (Session State)
now = get_now()
if 'target_date' not in st.session_state: st.session_state.target_date = now.date()
if 'selected_meal' not in st.session_state: st.session_state.selected_meal = "중식"

CSV_URL = "https://docs.google.com/spreadsheets/d/1l07s4rubmeB5ld8oJayYrstL34UPKtxQwYptIocgKV0/export?format=csv"
meal_data = load_meal_data(CSV_URL)

# 3. CSS (그리드 버튼 디자인 최적화)
st.markdown(f"""
<style>
    .block-container {{ padding: 1rem !important; max-width: 450px !important; }}
    header {{ visibility: hidden; }}
    
    /* 날짜 표시 */
    .header-date {{ text-align: center; font-size: 22px; font-weight: 800; color: #333; margin-bottom: 15px; }}
    
    /* 식단 카드 */
    .menu-card {{ 
        border: 1px solid #ddd; border-top: 10px solid var(--c);
        border-radius: 15px; padding: 25px 15px; text-align: center; 
        background: white; min-height: 150px; margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }}
    
    /* 버튼 스타일 (비상연락망 느낌) */
    .stButton > button {{
        border-radius: 8px !important;
        height: 45px !important;
        font-weight: 800 !important;
        font-size: 13px !important;
    }}
</style>
""", unsafe_allow_html=True)

# 4. 화면 구현
d = st.session_state.target_date
w_list = ["월","화","수","목","금","토","일"]
st.markdown(f'<div class="header-date">📅 {d.strftime("%m월 %d일")} ({w_list[d.weekday()]})</div>', unsafe_allow_html=True)

# 날짜 변경 버튼
c1, c2, c3 = st.columns(3)
with c1: 
    if st.button("◀ 이전날", use_container_width=True): 
        st.session_state.target_date -= timedelta(1)
        st.rerun()
with c2:
    if st.button("오늘", use_container_width=True): 
        st.session_state.target_date = now.date()
        st.rerun()
with c3:
    if st.button("다음날 ▶", use_container_width=True): 
        st.session_state.target_date += timedelta(1)
        st.rerun()

# 5. 그리드 메뉴 버튼 (핵심 변화 부분)
color_theme = {"조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"}
cols = st.columns(5)
meal_names = list(color_theme.keys())

for i, m_name in enumerate(meal_names):
    with cols[i]:
        # 현재 선택된 버튼은 강조색, 아니면 기본색
        is_selected = (st.session_state.selected_meal == m_name)
        if st.button(m_name, key=f"btn_{m_name}", use_container_width=True, type="primary" if is_selected else "secondary"):
            st.session_state.selected_meal = m_name
            st.rerun()

# 6. 식단 카드 출력
meal_info = meal_data.get(d.strftime("%Y-%m-%d"), {}).get(st.session_state.selected_meal, {"menu": "정보 없음", "side": "식단 정보가 없습니다."})
sel_color = color_theme[st.session_state.selected_meal]

st.markdown(f"""
    <div class="menu-card" style="--c: {sel_color};">
        <div style="color: {sel_color}; font-size: 14px; font-weight: 800; margin-bottom: 5px;">{st.session_state.selected_meal}</div>
        <div style="font-size: 24px; font-weight: 800; color: #111; margin-bottom: 12px;">{meal_info['menu']}</div>
        <div style="color: #555; font-size: 15px; line-height: 1.4; word-break: keep-all;">{meal_info['side']}</div>
    </div>
""", unsafe_allow_html=True)
