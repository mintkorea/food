import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# 1. 기초 설정
KST = ZoneInfo("Asia/Seoul")
def get_now(): return datetime.now(KST)

st.set_page_config(page_title="성의교정 식단 가이드", page_icon="🍴", layout="centered")

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

# 2. 상태 및 데이터 관리
now = get_now()
if 'target_date' not in st.session_state: st.session_state.target_date = now.date()
if 'selected_meal' not in st.session_state: st.session_state.selected_meal = "중식"

CSV_URL = "https://docs.google.com/spreadsheets/d/1l07s4rubmeB5ld8oJayYrstL34UPKtxQwYptIocgKV0/export?format=csv"
meal_data = load_meal_data(CSV_URL)
color_theme = {"조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"}

# 3. [핵심] 가로 정렬 및 개별 색상 강제 CSS
st.markdown(f"""
<style>
    .block-container {{ padding: 1rem 0.5rem !important; max-width: 500px !important; }}
    header {{ visibility: hidden; }}
    
    /* 식단 카드 상단 바 색상 동기화 */
    .menu-card {{ 
        border: 1px solid #ddd; border-top: 12px solid {color_theme[st.session_state.selected_meal]};
        border-radius: 15px; padding: 25px 10px; text-align: center; 
        background: white; min-height: 160px; margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }}

    /* 라디오 버튼을 가로 5열 그리드로 강제 전환 */
    div[data-testid="stRadio"] > div {{ 
        display: flex !important; 
        flex-direction: row !important; 
        flex-wrap: nowrap !important;
        gap: 4px !important; 
    }}
    
    /* 모든 버튼 기본 스타일 */
    div[data-testid="stRadio"] label {{ 
        flex: 1 !important;
        min-width: 0 !important;
        background: #f8f9fa !important; 
        border: 1px solid #eee !important;
        border-radius: 8px !important; 
        padding: 12px 0 !important;
        justify-content: center !important; 
        margin: 0 !important;
    }}
    
    /* 동그라미 숨기기 */
    div[data-testid="stRadio"] label div:first-child {{ display: none !important; }}
    div[data-testid="stRadio"] label div[data-testid="stMarkdownContainer"] {{ margin-left: 0 !important; }}

    /* [멀티 컬러 설정] 선택된 순서에 따라 다른 색상 부여 */
    div[data-testid="stRadio"] label[data-selected="true"] {{ border: none !important; }}
    div[data-testid="stRadio"] label:nth-of-type(1)[data-selected="true"] {{ background: {color_theme['조식']} !important; }}
    div[data-testid="stRadio"] label:nth-of-type(2)[data-selected="true"] {{ background: {color_theme['간편식']} !important; }}
    div[data-testid="stRadio"] label:nth-of-type(3)[data-selected="true"] {{ background: {color_theme['중식']} !important; }}
    div[data-testid="stRadio"] label:nth-of-type(4)[data-selected="true"] {{ background: {color_theme['석식']} !important; }}
    div[data-testid="stRadio"] label:nth-of-type(5)[data-selected="true"] {{ background: {color_theme['야식']} !important; }}
    
    div[data-testid="stRadio"] label[data-selected="true"] p {{ color: white !important; }}
    div[data-testid="stRadio"] label p {{ font-size: 12px !important; font-weight: 800; color: #666; }}
</style>
""", unsafe_allow_html=True)

# 4. 화면 구성
d = st.session_state.target_date
w_list = ["월","화","수","목","금","토","일"]
st.markdown(f'<div style="text-align:center; font-size:22px; font-weight:800; margin-bottom:15px;">📅 {d.strftime("%m월 %d일")} ({w_list[d.weekday()]})</div>', unsafe_allow_html=True)

# 날짜 네비게이션
c1, c2, c3 = st.columns(3)
with c1: 
    if st.button("◀ 이전날", use_container_width=True): st.session_state.target_date -= timedelta(1); st.rerun()
with c2:
    if st.button("오늘", use_container_width=True): st.session_state.target_date = now.date(); st.rerun()
with c3:
    if st.button("다음날 ▶", use_container_width=True): st.session_state.target_date += timedelta(1); st.rerun()

# 식단 카드
meal_info = meal_data.get(d.strftime("%Y-%m-%d"), {}).get(st.session_state.selected_meal, {"menu": "정보 없음", "side": "식단 정보가 없습니다."})
st.markdown(f"""
    <div class="menu-card">
        <div style="color: {color_theme[st.session_state.selected_meal]}; font-size: 14px; font-weight: 800; margin-bottom: 5px;">{st.session_state.selected_meal}</div>
        <div style="font-size: 24px; font-weight: 800; color: #111; margin-bottom: 12px; word-break: keep-all;">{meal_info['menu']}</div>
        <div style="color: #555; font-size: 15px; line-height: 1.4;">{meal_info['side']}</div>
    </div>
""", unsafe_allow_html=True)

# 5. 그리드 메뉴 (선택 시 상단 카드와 색상 연동)
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
