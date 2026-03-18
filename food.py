import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# 1. 기초 설정 및 데이터 로드
KST = ZoneInfo("Asia/Seoul")
def get_now(): return datetime.now(KST)

st.set_page_config(page_title="성의교정 식단", page_icon="🍴", layout="centered")

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

# 3. [핵심] 가로 5열 그리드 강제 및 디자인 CSS
st.markdown(f"""
<style>
    /* 전체 배경 및 폭 고정 */
    .block-container {{ padding: 1rem 0.5rem !important; max-width: 500px !important; }}
    header {{ visibility: hidden; }}
    
    /* 식단 카드 스타일 */
    .menu-card {{ 
        border: 1px solid #eee; border-top: 15px solid {color_theme[st.session_state.selected_meal]};
        border-radius: 15px; padding: 25px 15px; text-align: center; 
        background: white; box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    }}

    /* [강력 해결책] 버튼 컨테이너를 가로 그리드로 강제 전환 */
    div[data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important; /* 세로 줄바꿈 방지 */
        justify-content: space-between !important;
        gap: 4px !important;
    }}

    /* 각 버튼 열의 폭을 20%로 고정 */
    div[data-testid="column"] {{
        width: 19% !important;
        flex: 1 1 19% !important;
        min-width: 19% !important;
    }}

    /* 버튼 내부 텍스트 및 높이 조절 */
    button {{
        height: 48px !important;
        padding: 0 !important;
        font-size: 12px !important;
        font-weight: 800 !important;
        border-radius: 8px !important;
    }}
</style>
""", unsafe_allow_html=True)

# 4. 상단 날짜 및 네비게이션
d = st.session_state.target_date
w_list = ["월","화","수","목","금","토","일"]
st.markdown(f'<div style="text-align:center; font-size:22px; font-weight:800; margin-bottom:15px;">📅 {d.strftime("%m월 %d일")} ({w_list[d.weekday()]})</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1: 
    if st.button("◀ 이전날", use_container_width=True): st.session_state.target_date -= timedelta(1); st.rerun()
with c2:
    if st.button("오늘", use_container_width=True): st.session_state.target_date = now.date(); st.rerun()
with c3:
    if st.button("다음날 ▶", use_container_width=True): st.session_state.target_date += timedelta(1); st.rerun()

# 5. 식단 내용 표시
key = (d.strftime("%Y-%m-%d"), st.session_state.selected_meal)
meal_info = meal_data.get(key, {"menu": "정보 없음", "side": "식단 정보가 없습니다."})

st.markdown(f"""
    <div class="menu-card">
        <div style="color: {color_theme[st.session_state.selected_meal]}; font-size: 14px; font-weight: 800; margin-bottom: 8px;">{st.session_state.selected_meal}</div>
        <div style="font-size: 24px; font-weight: 800; color: #222; margin-bottom: 15px; word-break: keep-all;">{meal_info['menu']}</div>
        <div style="color: #666; font-size: 15px; line-height: 1.5; word-break: keep-all;">{meal_info['side']}</div>
    </div>
""", unsafe_allow_html=True)

# 6. [해결] 5개 버튼 강제 가로 배치
cols = st.columns(5)
for i, (m_name, m_color) in enumerate(color_theme.items()):
    with cols[i]:
        is_sel = (st.session_state.selected_meal == m_name)
        # 선택된 버튼은 테마 색상 적용, 나머지는 기본 스타일
        if st.button(m_name, key=f"btn_{i}", use_container_width=True):
            st.session_state.selected_meal = m_name
            st.rerun()

# 선택된 버튼 색상을 CSS로 강제 주입
st.markdown(f"""
<style>
    div[data-testid="column"]:nth-of-type({list(color_theme.keys()).index(st.session_state.selected_meal) + 1}) button {{
        background-color: {color_theme[st.session_state.selected_meal]} !important;
        color: white !important;
        border: none !important;
    }}
</style>
""", unsafe_allow_html=True)
