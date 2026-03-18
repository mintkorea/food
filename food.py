import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, time
from zoneinfo import ZoneInfo

# 1. 기초 설정
KST = ZoneInfo("Asia/Seoul")
def get_now(): return datetime.now(KST)

st.set_page_config(page_title="성의교정 식단 가이드", page_icon="🍴", layout="centered")

@st.cache_data(ttl=600)
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

# 2. 초기 상태 설정
CSV_URL = "https://docs.google.com/spreadsheets/d/1l07s4rubmeB5ld8oJayYrstL34UPKtxQwYptIocgKV0/export?format=csv"
meal_data = load_meal_data(CSV_URL)
now = get_now()

if 'target_date' not in st.session_state: st.session_state.target_date = now.date()
if 'selected_meal' not in st.session_state:
    t = now.time()
    if t < time(9, 0): st.session_state.selected_meal = "조식"
    elif t < time(14, 0): st.session_state.selected_meal = "중식"
    elif t < time(19, 20): st.session_state.selected_meal = "석식"
    else: st.session_state.selected_meal = "중식"

color_theme = {"조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"}

# 3. CSS (그리드 버튼 디자인)
st.markdown(f"""
<style>
    .block-container {{ padding: 1rem 0.8rem !important; max-width: 500px !important; }}
    header {{ visibility: hidden; }}
    
    /* 상단 날짜 디자인 */
    .header-date {{ text-align: center; font-size: 24px; font-weight: 800; color: #333; margin-bottom: 10px; }}
    
    /* 식단 카드 (상단 컬러 바) */
    .menu-card {{ 
        border: 1px solid #eee; border-top: 12px solid var(--c);
        border-radius: 15px; padding: 25px 15px; text-align: center; 
        background: white; min-height: 160px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }}

    /* [핵심] 그리드 버튼 스타일 (라디오 버튼 변형) */
    div[data-testid="stRadio"] > div {{ 
        display: grid !important; 
        grid-template-columns: repeat(5, 1fr) !important; /* 5열 그리드 */
        gap: 5px !important; background: transparent !important; padding: 0 !important;
    }}
    div[data-testid="stRadio"] label {{ 
        flex-direction: column !important; /* 동그라미 위로 */
        background: white; border: 1px solid #ddd; border-radius: 8px;
        padding: 10px 0 !important; transition: 0.2s;
    }}
    /* 라디오 버튼 동그라미 숨기기 */
    div[data-testid="stRadio"] label div[data-testid="stMarkdownContainer"] {{ margin-left: 0 !important; }}
    div[data-testid="stRadio"] label div:first-child {{ display: none !important; }} 
    
    /* 선택된 버튼 디자인 */
    div[data-testid="stRadio"] label[data-selected="true"] {{ 
        background: var(--sel-color) !important; border: none; color: white !important;
    }}
    div[data-testid="stRadio"] label[data-selected="true"] p {{ color: white !important; }}
    div[data-testid="stRadio"] label p {{ font-size: 12px !important; font-weight: 800; }}

    .msg-box {{ text-align: center; background: #f8f9fa; padding: 12px; border-radius: 10px; font-size: 13px; font-weight: bold; margin-top: 15px; border-left: 5px solid #1E3A5F; }}
</style>
""", unsafe_allow_html=True)

# 4. 화면 구현
d = st.session_state.target_date
w_list = ["월","화","수","목","금","토","일"]
st.markdown(f'<div class="header-date">📅 {d.strftime("%m월 %d일")} ({w_list[d.weekday()]})</div>', unsafe_allow_html=True)

# 네비게이션 버튼 (그리드 형태)
col1, col2, col3 = st.columns(3)
with col1: 
    if st.button("◀ 이전날", use_container_width=True): st.session_state.target_date -= timedelta(1); st.rerun()
with col2:
    if st.button("오늘", use_container_width=True): st.session_state.target_date = now.date(); st.rerun()
with col3:
    if st.button("다음날 ▶", use_container_width=True): st.session_state.target_date += timedelta(1); st.rerun()

# 식단 카드 표시
meal_info = meal_data.get(d.strftime("%Y-%m-%d"), {}).get(st.session_state.selected_meal, {"menu": "정보 없음", "side": "식단 정보가 없습니다."})
sel_color = color_theme[st.session_state.selected_meal]

st.markdown(f"""
    <div class="menu-card" style="--c: {sel_color};">
        <div style="color: {sel_color}; font-size: 14px; font-weight: 800; margin-bottom: 8px;">{st.session_state.selected_meal}</div>
        <div style="font-size: 24px; font-weight: 800; color: #111; margin-bottom: 15px; word-break: keep-all;">{meal_info['menu']}</div>
        <div style="color: #666; font-size: 15px; line-height: 1.5;">{meal_info['side']}</div>
    </div>
""", unsafe_allow_html=True)

# [개선] 5열 그리드 메뉴 (선택된 색상이 버튼 배경색으로 반영됨)
st.markdown(f"<style>:root {{ --sel-color: {sel_color}; }}</style>", unsafe_allow_html=True)
selected = st.radio(
    "식사선택", 
    options=list(color_theme.keys()), 
    index=list(color_theme.keys()).index(st.session_state.selected_meal), 
    horizontal=True, 
    label_visibility="collapsed"
)

if selected != st.session_state.selected_meal:
    st.session_state.selected_meal = selected
    st.rerun()

# 5. 시간 안내 메시지
st.markdown(f'<div class="msg-box">🍴 선택하신 [{st.session_state.selected_meal}] 식단을 확인 중입니다.</div>', unsafe_allow_html=True)
