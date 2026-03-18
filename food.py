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

# 3. [핵심] 모바일 가로 5열 강제 CSS
st.markdown(f"""
<style>
    /* 전체 레이아웃 폭 조정 */
    .block-container {{ padding: 1rem 0.5rem !important; max-width: 500px !important; }}
    header {{ visibility: hidden; }}
    
    /* 식단 카드: 하단 마진 제거하여 버튼 바와 연결 */
    .menu-card {{ 
        border: 1px solid #ddd; border-top: 15px solid {color_theme[st.session_state.selected_meal]};
        border-radius: 15px 15px 0 0; padding: 25px 10px; text-align: center; 
        background: white; box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 0px;
    }}

    /* 버튼 컨테이너: 모바일에서도 가로 5열 강제 */
    .button-grid {{
        display: flex !important;
        flex-direction: row !important;
        width: 100%;
        gap: 4px;
        padding: 5px;
        background: #f8f9fa;
        border: 1px solid #ddd;
        border-top: none;
        border-radius: 0 0 15px 15px;
    }}
    
    /* Streamlit 컬럼 내부의 버튼들이 세로로 쌓이는 것을 방지 */
    [data-testid="column"] {{
        width: calc(20% - 4px) !important;
        flex: 1 1 calc(20% - 4px) !important;
        min-width: calc(20% - 4px) !important;
    }}

    button {{
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

# 날짜 변경 (상단)
c1, c2, c3 = st.columns(3)
with c1: 
    if st.button("◀ 이전날", use_container_width=True): st.session_state.target_date -= timedelta(1); st.rerun()
with c2:
    if st.button("오늘", use_container_width=True): st.session_state.target_date = now.date(); st.rerun()
with c3:
    if st.button("다음날 ▶", use_container_width=True): st.session_state.target_date += timedelta(1); st.rerun()

# 5. 식단 카드 표시
key = (d.strftime("%Y-%m-%d"), st.session_state.selected_meal)
meal_info = meal_data.get(key, {"menu": "정보 없음", "side": "식단 정보가 없습니다."})

st.markdown(f"""
    <div class="menu-card">
        <div style="color: {color_theme[st.session_state.selected_meal]}; font-size: 14px; font-weight: 800; margin-bottom: 5px;">{st.session_state.selected_meal}</div>
        <div style="font-size: 24px; font-weight: 800; color: #111; margin-bottom: 12px; word-break: keep-all;">{meal_info['menu']}</div>
        <div style="color: #555; font-size: 15px; line-height: 1.4;">{meal_info['side']}</div>
    </div>
""", unsafe_allow_html=True)

# 6. [해결] 버튼 그리드
# st.container와 columns를 조합하고 CSS로 가로를 강제합니다.
with st.container():
    cols = st.columns(5)
    for i, (m_name, m_color) in enumerate(color_theme.items()):
        with cols[i]:
            is_sel = (st.session_state.selected_meal == m_name)
            if st.button(m_name, key=f"btn_{i}", use_container_width=True):
                st.session_state.selected_meal = m_name
                st.rerun()

# 선택된 버튼 색상을 CSS로 개별 주입
st.markdown(f"""
<style>
    /* 선택된 버튼에만 해당 식단 고유 컬러 적용 */
    div[data-testid="column"]:nth-of-type({list(color_theme.keys()).index(st.session_state.selected_meal) + 1}) button {{
        background-color: {color_theme[st.session_state.selected_meal]} !important;
        color: white !important;
        border: none !important;
    }}
</style>
""", unsafe_allow_html=True)
