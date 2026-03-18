import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, time
from zoneinfo import ZoneInfo

# 1. 기초 설정
KST = ZoneInfo("Asia/Seoul")
def get_now(): return datetime.now(KST)

st.set_page_config(page_title="성의교정 식단 가이드", page_icon="🍴", layout="centered")

# 데이터 로딩 (캐싱)
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

# 2. 상태 관리 및 데이터 로드
CSV_URL = "https://docs.google.com/spreadsheets/d/1l07s4rubmeB5ld8oJayYrstL34UPKtxQwYptIocgKV0/export?format=csv"
meal_data = load_meal_data(CSV_URL)
now = get_now()

if 'target_date' not in st.session_state:
    st.session_state.target_date = now.date()

if 'selected_meal' not in st.session_state:
    t = now.time()
    if t < time(9, 0): st.session_state.selected_meal = "조식"
    elif t < time(14, 0): st.session_state.selected_meal = "중식"
    elif t < time(19, 20): st.session_state.selected_meal = "석식"
    else: st.session_state.selected_meal = "중식"

# 3. CSS 수정 (깨짐 방지 핵심)
st.markdown("""
<style>
    .block-container { padding: 1rem 0.8rem !important; max-width: 450px !important; }
    header { visibility: hidden; }
    
    /* 날짜 및 조 표시 */
    .date-box { text-align: center; background: #F8FAFF; padding: 12px 5px; border-radius: 12px; border: 1px solid #D1D9E6; margin-bottom: 10px; }
    .res-sub-title { font-size: 18px !important; font-weight: 800; color: #1E3A5F; }
    
    /* 식단 카드 */
    .menu-card { 
        border: 2.5px solid var(--c); border-radius: 15px; 
        padding: 25px 10px; text-align: center; background: white; 
        min-height: 160px; margin-bottom: 10px;
    }
    
    /* 라디오 버튼 모바일 최적화 (한 줄 유지) */
    div[data-testid="stRadio"] > div { 
        display: flex !important; flex-direction: row !important; 
        background: #f1f3f5; padding: 3px !important; border-radius: 12px; gap: 3px;
    }
    div[data-testid="stRadio"] label { 
        flex: 1; background: white; border-radius: 8px; padding: 6px 0 !important;
        margin: 0 !important; justify-content: center !important; 
        min-width: 0px !important; /* 너비 제한 해제 */
    }
    div[data-testid="stRadio"] label p { 
        font-size: 11px !important; /* 글자 크기를 더 줄여서 깨짐 방지 */
        font-weight: 800 !important; 
    }
    
    /* 선택 강조 */
    div[data-testid="stRadio"] label[data-selected="true"] { background: #1E3A5F !important; }
    div[data-testid="stRadio"] label[data-selected="true"] p { color: white !important; }

    .msg-box { text-align: center; background: #f8f9fa; padding: 10px; border-radius: 10px; font-size: 13px; font-weight: bold; color: #666; }
</style>
""", unsafe_allow_html=True)

# 4. 화면 구성
st.markdown('<div style="text-align:center; font-size:24px; font-weight:800; color:#1E3A5F; margin-bottom:10px;">🍽️ 성의교정 식단</div>', unsafe_allow_html=True)

# 날짜 네비게이션
d = st.session_state.target_date
w_list = ["월","화","수","목","금","토","일"]
st.markdown(f'<div class="date-box"><span class="res-sub-title">{d.strftime("%Y.%m.%d")}.({w_list[d.weekday()]})</span></div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("◀ 이전", use_container_width=True):
        st.session_state.target_date -= timedelta(1); st.rerun()
with col2:
    if st.button("오늘", use_container_width=True):
        st.session_state.target_date = now.date(); st.rerun()
with col3:
    if st.button("다음 ▶", use_container_width=True):
        st.session_state.target_date += timedelta(1); st.rerun()

# 식단 표시
color_theme = {"조식": "#E95444", "중식": "#8BC34A", "석식": "#4A90E2", "간편식": "#F1A33B"}
meal_info = meal_data.get(d.strftime("%Y-%m-%d"), {}).get(st.session_state.selected_meal, {"menu": "정보 없음", "side": "등록된 식단이 없습니다."})

st.markdown(f"""
    <div class="menu-card" style="--c: {color_theme.get(st.session_state.selected_meal, '#ccc')};">
        <div style="font-size: 22px; font-weight: 800; color: #111; margin-bottom: 10px;">{meal_info['menu']}</div>
        <div style="color: #555; font-size: 15px; line-height: 1.4;">{meal_info['side']}</div>
    </div>
""", unsafe_allow_html=True)

# 식사 선택 라디오 (아이콘/설명 제거하여 부피 축소)
selected = st.radio("select", options=list(color_theme.keys()), 
                    index=list(color_theme.keys()).index(st.session_state.selected_meal), 
                    horizontal=True, label_visibility="collapsed")

if selected != st.session_state.selected_meal:
    st.session_state.selected_meal = selected
    st.rerun()

st.markdown(f'<div class="msg-box">현재 {st.session_state.selected_meal} 메뉴를 확인 중입니다.</div>', unsafe_allow_html=True)

