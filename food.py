import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import streamlit.components.v1 as components

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

# 2. 상태 및 데이터 관리
now = get_now()
if 'target_date' not in st.session_state: st.session_state.target_date = now.date()
if 'selected_meal' not in st.session_state: st.session_state.selected_meal = "중식"

CSV_URL = "https://docs.google.com/spreadsheets/d/1l07s4rubmeB5ld8oJayYrstL34UPKtxQwYptIocgKV0/export?format=csv"
meal_data = load_meal_data(CSV_URL)
color_theme = {"조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"}

# 3. [핵심] 가로 5열 강제 고정용 CSS 및 HTML 설계
st.markdown(f"""
<style>
    .block-container {{ padding: 1rem 0.5rem !important; max-width: 480px !important; }}
    header {{ visibility: hidden; }}
    
    /* 식단 카드 디자인 */
    .menu-card {{ 
        border: 1px solid #eee; border-top: 15px solid {color_theme[st.session_state.selected_meal]};
        border-radius: 15px; padding: 25px 15px; text-align: center; 
        background: white; box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }}
</style>
""", unsafe_allow_html=True)

# 4. 화면 상단 구성 (날짜)
d = st.session_state.target_date
w_list = ["월","화","수","목","금","토","일"]
st.markdown(f'<div style="text-align:center; font-size:22px; font-weight:800; margin-bottom:15px;">📅 {d.strftime("%m월 %d일")} ({w_list[d.weekday()]})</div>', unsafe_allow_html=True)

# 날짜 이동 버튼 (이 부분은 가독성을 위해 3열 유지)
c1, c2, c3 = st.columns(3)
with c1: 
    if st.button("◀ 이전날", use_container_width=True): st.session_state.target_date -= timedelta(1); st.rerun()
with c2:
    if st.button("오늘", use_container_width=True): st.session_state.target_date = now.date(); st.rerun()
with c3:
    if st.button("다음날 ▶", use_container_width=True): st.session_state.target_date += timedelta(1); st.rerun()

# 5. 식단 카드 출력
key = (d.strftime("%Y-%m-%d"), st.session_state.selected_meal)
meal_info = meal_data.get(key, {"menu": "정보 없음", "side": "식단 정보가 없습니다."})

st.markdown(f"""
    <div class="menu-card">
        <div style="color: {color_theme[st.session_state.selected_meal]}; font-size: 14px; font-weight: 800; margin-bottom: 5px;">{st.session_state.selected_meal}</div>
        <div style="font-size: 24px; font-weight: 800; color: #111; margin-bottom: 12px;">{meal_info['menu']}</div>
        <div style="color: #555; font-size: 15px; line-height: 1.4;">{meal_info['side']}</div>
    </div>
""", unsafe_allow_html=True)

# 6. [강력 해결] HTML 그리드를 통한 가로 5열 버튼 강제 배치
# Streamlit의 columns는 모바일에서 깨지기 쉬우므로, 직접 HTML을 그려서 클릭 이벤트를 받습니다.
button_options = list(color_theme.keys())
cols = st.columns(5) # 일단 5열을 만들고 CSS로 강제 정렬

for i, m_name in enumerate(button_options):
    with cols[i]:
        is_sel = (st.session_state.selected_meal == m_name)
        # 각 컬럼의 폭을 강제로 20%로 고정하는 트릭
        st.markdown(f"""
            <style>
                div[data-testid="column"]:nth-of-type({i+1}) {{
                    width: 19% !important;
                    flex: 1 1 19% !important;
                    min-width: 19% !important;
                }}
            </style>
        """, unsafe_allow_html=True)
        
        if st.button(m_name, key=f"btn_{m_name}", use_container_width=True):
            st.session_state.selected_meal = m_name
            st.rerun()

# 선택된 버튼 색상 강조를 위한 추가 스타일
st.markdown(f"""
<style>
    /* 선택된 식단 이름에 맞춰 버튼 배경색 변경 */
    div[data-testid="column"]:nth-of-type({button_options.index(st.session_state.selected_meal) + 1}) button {{
        background-color: {color_theme[st.session_state.selected_meal]} !important;
        color: white !important;
        border: none !important;
    }}
</style>
""", unsafe_allow_html=True)
