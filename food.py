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

# 2. 데이터 및 상태 관리
CSV_URL = "https://docs.google.com/spreadsheets/d/1l07s4rubmeB5ld8oJayYrstL34UPKtxQwYptIocgKV0/export?format=csv"
meal_data = load_meal_data(CSV_URL)
now = get_now()

if 'target_date' not in st.session_state: st.session_state.target_date = now.date()
color_theme = {"조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"}

if 'selected_meal' not in st.session_state:
    t = now.time()
    if t < time(9, 0): st.session_state.selected_meal = "조식"
    elif t < time(14, 0): st.session_state.selected_meal = "중식"
    elif t < time(19, 20): st.session_state.selected_meal = "석식"
    else: st.session_state.selected_meal = "중식"

# 3. 커스텀 CSS (비상연락망 그리드 스타일 적용)
st.markdown(f"""
<style>
    .block-container {{ padding: 1rem 0.8rem !important; max-width: 480px !important; }}
    header {{ visibility: hidden; }}
    
    /* 날짜 헤더 */
    .header-date {{ text-align: center; font-size: 24px; font-weight: 800; color: #333; margin: 15px 0; }}
    
    /* 식단 카드 (상단 컬러 포인트) */
    .menu-card {{ 
        border: 1px solid #ddd; border-top: 12px solid var(--c);
        border-radius: 15px; padding: 30px 15px; text-align: center; 
        background: white; min-height: 180px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }}

    /* [그리드 버튼] 라디오 버튼 커스텀 */
    div[data-testid="stRadio"] > div {{ 
        display: grid !important; 
        grid-template-columns: repeat(5, 1fr) !important; 
        gap: 6px !important; 
    }}
    
    /* 기본 버튼 모양 (비상연락망 스타일) */
    div[data-testid="stRadio"] label {{ 
        background: #f8f9fa !important; border: 1px solid #eee !important;
        border-radius: 10px !important; padding: 12px 0 !important;
        justify-content: center !important; transition: all 0.2s ease;
    }}
    
    /* 라디오 버튼의 동그라미 숨기기 */
    div[data-testid="stRadio"] label div[data-testid="stMarkdownContainer"] {{ margin-left: 0 !important; }}
    div[data-testid="stRadio"] [data-testid="stWidgetLabel"] {{ display: none; }}
    div[data-testid="stRadio"] label div:first-child {{ display: none !important; }} 
    
    /* 선택된 버튼: 해당 식단 컬러로 반전 */
    div[data-testid="stRadio"] label[data-selected="true"] {{ 
        background: var(--c) !important; border: none !important; 
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }}
    div[data-testid="stRadio"] label[data-selected="true"] p {{ color: white !important; }}
    div[data-testid="stRadio"] label p {{ font-size: 13px !important; font-weight: 800; color: #666; }}

    .msg-box {{ text-align: center; background: #F0F2F6; padding: 12px; border-radius: 10px; font-size: 14px; font-weight: bold; color: #1E3A5F; margin-top: 15px; }}
</style>
""", unsafe_allow_html=True)

# 4. 화면 레이아웃
d = st.session_state.target_date
w_list = ["월","화","수","목","금","토","일"]
st.markdown(f'<div class="header-date">📅 {d.strftime("%m월 %d일")} ({w_list[d.weekday()]})</div>', unsafe_allow_html=True)

# 이전/오늘/다음 버튼
c1, c2, c3 = st.columns(3)
with c1: 
    if st.button("◀ 이전날", use_container_width=True): st.session_state.target_date -= timedelta(1); st.rerun()
with c2:
    if st.button("오늘", use_container_width=True): st.session_state.target_date = now.date(); st.rerun()
with c3:
    if st.button("다음날 ▶", use_container_width=True): st.session_state.target_date += timedelta(1); st.rerun()

# 식단 데이터 및 카드 출력
meal_info = meal_data.get(d.strftime("%Y-%m-%d"), {}).get(st.session_state.selected_meal, {"menu": "정보 없음", "side": "식단 정보가 없습니다."})
sel_color = color_theme[st.session_state.selected_meal]

st.markdown(f"""
    <div class="menu-card" style="--c: {sel_color};">
        <div style="color: {sel_color}; font-size: 15px; font-weight: 800; margin-bottom: 8px;">{st.session_state.selected_meal}</div>
        <div style="font-size: 26px; font-weight: 800; color: #111; margin-bottom: 15px; word-break: keep-all;">{meal_info['menu']}</div>
        <div style="color: #444; font-size: 16px; line-height: 1.5;">{meal_info['side']}</div>
    </div>
""", unsafe_allow_html=True)

# [그리드 메뉴] 라디오 버튼 (각 선택마다 sel_color 변수 활용)
selected = st.radio(
    "meal_select", 
    options=list(color_theme.keys()), 
    index=list(color_theme.keys()).index(st.session_state.selected_meal), 
    horizontal=True, 
    label_visibility="collapsed"
)

if selected != st.session_state.selected_meal:
    st.session_state.selected_meal = selected
    st.rerun()

st.markdown(f'<div class="msg-box">🍴 현재 {st.session_state.selected_meal} 메뉴를 표시하고 있습니다.</div>', unsafe_allow_html=True)
