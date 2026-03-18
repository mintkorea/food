import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# 1. 기초 설정
KST = ZoneInfo("Asia/Seoul")
def get_now(): return datetime.now(KST)

st.set_page_config(page_title="성의교정 식단 가이드", page_icon="🍴", layout="centered")

# 데이터 로딩 (캐시 초기화)
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

# 2. 상태 관리
now = get_now()
if 'target_date' not in st.session_state: st.session_state.target_date = now.date()
if 'selected_meal' not in st.session_state: st.session_state.selected_meal = "중식"

CSV_URL = "https://docs.google.com/spreadsheets/d/1l07s4rubmeB5ld8oJayYrstL34UPKtxQwYptIocgKV0/export?format=csv"
meal_data = load_meal_data(CSV_URL)
color_theme = {"조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"}

# 3. CSS (가로 그리드 강제 적용)
st.markdown(f"""
<style>
    .block-container {{ padding: 1rem !important; max-width: 500px !important; }}
    
    /* 식단 카드 디자인 */
    .menu-card {{ 
        border: 1px solid #ddd; border-top: 12px solid {color_theme[st.session_state.selected_meal]};
        border-radius: 15px; padding: 30px 15px; text-align: center; 
        background: white; min-height: 160px; margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }}

    /* 버튼 컨테이너를 가로 그리드로 강제 (중요!) */
    div[data-testid="column"] {{
        display: flex;
        justify-content: center;
    }}
</style>
""", unsafe_allow_html=True)

# 4. 상단 날짜 및 네비게이션
d = st.session_state.target_date
w_list = ["월","화","수","목","금","토","일"]
st.markdown(f'<div style="text-align:center; font-size:24px; font-weight:800; margin-bottom:15px;">📅 {d.strftime("%m월 %d일")} ({w_list[d.weekday()]})</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1: 
    if st.button("◀ 이전날", use_container_width=True): st.session_state.target_date -= timedelta(1); st.rerun()
with c2:
    if st.button("오늘", use_container_width=True): st.session_state.target_date = now.date(); st.rerun()
with c3:
    if st.button("다음날 ▶", use_container_width=True): st.session_state.target_date += timedelta(1); st.rerun()

# 5. 식단 카드 표시
meal_info = meal_data.get(d.strftime("%Y-%m-%d"), {}).get(st.session_state.selected_meal, {"menu": "정보 없음", "side": "식단 정보가 없습니다."})
st.markdown(f"""
    <div class="menu-card">
        <div style="color: {color_theme[st.session_state.selected_meal]}; font-size: 15px; font-weight: 800; margin-bottom: 8px;">{st.session_state.selected_meal}</div>
        <div style="font-size: 26px; font-weight: 800; color: #111; margin-bottom: 15px;">{meal_info['menu']}</div>
        <div style="color: #555; font-size: 16px; line-height: 1.5;">{meal_info['side']}</div>
    </div>
""", unsafe_allow_html=True)

# 6. [핵심] 가로 그리드 컬러 버튼 (라디오 버튼 스타일 활용)
# 라디오 버튼을 가로로 정렬하고 각각의 색상을 CSS로 개별 지정합니다.
st.markdown("""
<style>
    div[data-testid="stRadio"] > div { display: flex !important; flex-direction: row !important; gap: 4px !important; }
    div[data-testid="stRadio"] label { 
        flex: 1; border: 1px solid #eee !important; background: #f8f9fa !important;
        border-radius: 8px !important; padding: 12px 0 !important; justify-content: center !important;
    }
    div[data-testid="stRadio"] label div:first-child { display: none !important; } /* 동그라미 숨김 */
    
    /* 각 버튼별 선택 시 고유 컬러 적용 */
    div[data-testid="stRadio"] label[data-selected="true"] { border: none !important; }
    
    /* 조식(1번째) */
    div[data-testid="stRadio"] label:nth-of-type(1)[data-selected="true"] { background: #E95444 !important; }
    /* 간편식(2번째) */
    div[data-testid="stRadio"] label:nth-of-type(2)[data-selected="true"] { background: #F1A33B !important; }
    /* 중식(3번째) */
    div[data-testid="stRadio"] label:nth-of-type(3)[data-selected="true"] { background: #8BC34A !important; }
    /* 석식(4번째) */
    div[data-testid="stRadio"] label:nth-of-type(4)[data-selected="true"] { background: #4A90E2 !important; }
    /* 야식(5번째) */
    div[data-testid="stRadio"] label:nth-of-type(5)[data-selected="true"] { background: #673AB7 !important; }
    
    div[data-testid="stRadio"] label[data-selected="true"] p { color: white !important; }
    div[data-testid="stRadio"] label p { font-size: 13px !important; font-weight: 800; }
</style>
""", unsafe_allow_html=True)

selected = st.radio("meal_choice", options=list(color_theme.keys()), 
                    index=list(color_theme.keys()).index(st.session_state.selected_meal),
                    horizontal=True, label_visibility="collapsed")

if selected != st.session_state.selected_meal:
    st.session_state.selected_meal = selected
    st.rerun()
