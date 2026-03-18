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
        return df.set_index(['date', 'meal_type']).to_dict('index')
    except: return {}

# 2. 상태 관리
now = get_now()
if 'target_date' not in st.session_state: st.session_state.target_date = now.date()
if 'selected_meal' not in st.session_state: st.session_state.selected_meal = "중식"

CSV_URL = "https://docs.google.com/spreadsheets/d/1l07s4rubmeB5ld8oJayYrstL34UPKtxQwYptIocgKV0/export?format=csv"
meal_data = load_meal_data(CSV_URL)
color_theme = {"조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"}

# 3. CSS (카드와 버튼 밀착 및 디자인 최적화)
st.markdown(f"""
<style>
    .block-container {{ padding: 1rem 0.5rem !important; max-width: 480px !important; }}
    header {{ visibility: hidden; }}
    
    /* 식단 카드: 하단 마진 제거하여 버튼과 밀착 */
    .menu-card {{ 
        border: 1px solid #ddd; border-top: 12px solid {color_theme[st.session_state.selected_meal]};
        border-radius: 15px 15px 0 0; padding: 25px 15px; text-align: center; 
        background: white; box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 0px;
    }}

    /* 버튼 컨테이너: 카드와 붙이기 위해 여백 조정 */
    div[data-testid="stHorizontalBlock"] {{
        gap: 2px !important;
        background: #f8f9fa;
        padding: 5px;
        border: 1px solid #ddd;
        border-top: none;
        border-radius: 0 0 15px 15px;
    }}

    /* Streamlit 기본 버튼 개조 */
    div[data-testid="stHorizontalBlock"] button {{
        border: none !important;
        border-radius: 8px !important;
        height: 45px !important;
        padding: 0 !important;
        font-size: 13px !important;
        font-weight: 800 !important;
    }}
</style>
""", unsafe_allow_html=True)

# 4. 화면 구성
d = st.session_state.target_date
w_list = ["월","화","수","목","금","토","일"]
st.markdown(f'<div style="text-align:center; font-size:22px; font-weight:800; margin-bottom:15px;">📅 {d.strftime("%m월 %d일")} ({w_list[d.weekday()]})</div>', unsafe_allow_html=True)

# 상단 날짜 이동
c1, c2, c3 = st.columns(3)
with c1: 
    if st.button("◀ 이전날", use_container_width=True): st.session_state.target_date -= timedelta(1); st.rerun()
with c2:
    if st.button("오늘", use_container_width=True): st.session_state.target_date = now.date(); st.rerun()
with c3:
    if st.button("다음날 ▶", use_container_width=True): st.session_state.target_date += timedelta(1); st.rerun()

# 5. 식단 카드 (상단 부분)
key = (d.strftime("%Y-%m-%d"), st.session_state.selected_meal)
meal_info = meal_data.get(key, {"menu": "정보 없음", "side": "식단 정보가 없습니다."})

st.markdown(f"""
    <div class="menu-card">
        <div style="color: {color_theme[st.session_state.selected_meal]}; font-size: 14px; font-weight: 800; margin-bottom: 5px;">{st.session_state.selected_meal}</div>
        <div style="font-size: 24px; font-weight: 800; color: #111; margin-bottom: 12px; word-break: keep-all;">{meal_info['menu']}</div>
        <div style="color: #555; font-size: 15px; line-height: 1.4;">{meal_info['side']}</div>
    </div>
""", unsafe_allow_html=True)

# 6. 식단 선택 버튼 (카드 바로 아래에 밀착된 5열 그리드)
cols = st.columns(5)
for i, (m_name, m_color) in enumerate(color_theme.items()):
    with cols[i]:
        is_sel = (st.session_state.selected_meal == m_name)
        # 선택된 버튼은 고유 컬러 적용, 나머지는 연한 회색
        if st.button(m_name, key=f"m_{i}", use_container_width=True, 
                     type="primary" if is_sel else "secondary"):
            st.session_state.selected_meal = m_name
            st.rerun()

# 선택된 버튼 색상을 CSS로 강제 주입 (Streamlit 기본 primary 색상 변경)
st.markdown(f"""
<style>
    div[data-testid="stHorizontalBlock"] button[kind="primary"] {{
        background-color: {color_theme[st.session_state.selected_meal]} !important;
        color: white !important;
    }}
</style>
""", unsafe_allow_html=True)
