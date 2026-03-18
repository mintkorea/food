import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# 1. 기초 설정 및 시간대
KST = ZoneInfo("Asia/Seoul")
def get_now(): return datetime.now(KST)

st.set_page_config(page_title="성의교정 식단 가이드", page_icon="🍴", layout="centered")

@st.cache_data(ttl=0)
def load_meal_data(url):
    try:
        df = pd.read_csv(url)
        return df.set_index(['date', 'meal_type']).to_dict('index')
    except: return {}

# 2. 데이터 및 상태 관리
CSV_URL = "https://docs.google.com/spreadsheets/d/1l07s4rubmeB5ld8oJayYrstL34UPKtxQwYptIocgKV0/export?format=csv"
meal_data = load_meal_data(CSV_URL)
now = get_now()

if 'target_date' not in st.session_state: st.session_state.target_date = now.date()
if 'selected_meal' not in st.session_state: st.session_state.selected_meal = "중식"

color_theme = {"조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"}

# 3. [강력 해결] 가로 정렬 및 개별 컬러 CSS
st.markdown(f"""
<style>
    /* 전체 배경 및 컨테이너 조정 */
    .block-container {{ padding: 1rem 0.5rem !important; max-width: 500px !important; }}
    header {{ visibility: hidden; }}
    
    /* 날짜 표시 디자인 */
    .date-title {{ text-align: center; font-size: 22px; font-weight: 800; margin-bottom: 10px; }}

    /* 식단 카드 스타일 */
    .menu-card {{ 
        border: 1px solid #ddd; border-top: 15px solid {color_theme[st.session_state.selected_meal]};
        border-radius: 20px; padding: 30px 15px; text-align: center; 
        background: white; box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 25px;
    }}

    /* [중요] 버튼을 가로로 강제 배치하는 그리드 */
    .grid-container {{
        display: grid;
        grid-template-columns: repeat(5, 1fr); /* 무조건 5열 */
        gap: 5px;
        width: 100%;
    }}
    
    .grid-item {{
        border: 1px solid #eee; border-radius: 8px;
        padding: 12px 0; text-align: center; font-size: 13px; font-weight: 800;
        cursor: pointer; background: #f8f9fa; color: #666;
    }}
</style>
""", unsafe_allow_html=True)

# 4. 화면 구성
d = st.session_state.target_date
w_list = ["월","화","수","목","금","토","일"]
st.markdown(f'<div class="date-title">📅 {d.strftime("%m월 %d일")} ({w_list[d.weekday()]})</div>', unsafe_allow_html=True)

# 날짜 네비게이션
c1, c2, c3 = st.columns(3)
with c1: 
    if st.button("◀ 이전날", use_container_width=True): st.session_state.target_date -= timedelta(1); st.rerun()
with c2:
    if st.button("오늘", use_container_width=True): st.session_state.target_date = now.date(); st.rerun()
with c3:
    if st.button("다음날 ▶", use_container_width=True): st.session_state.target_date += timedelta(1); st.rerun()

# 식단 카드 출력
key = (d.strftime("%Y-%m-%d"), st.session_state.selected_meal)
meal_info = meal_data.get(key, {"menu": "정보 없음", "side": "식단 정보가 없습니다."})

st.markdown(f"""
    <div class="menu-card">
        <div style="color: {color_theme[st.session_state.selected_meal]}; font-size: 15px; font-weight: 800; margin-bottom: 10px;">{st.session_state.selected_meal}</div>
        <div style="font-size: 26px; font-weight: 800; color: #111; margin-bottom: 15px;">{meal_info['menu']}</div>
        <div style="color: #444; font-size: 16px; line-height: 1.5; word-break: keep-all;">{meal_info['side']}</div>
    </div>
""", unsafe_allow_html=True)

# 5. [해결] 클릭 시 색상이 변하는 가로 그리드 버튼 세트
st.write('<div class="grid-container">', unsafe_allow_html=True)
cols = st.columns(5)
for i, (m_name, m_color) in enumerate(color_theme.items()):
    with cols[i]:
        # 현재 선택된 버튼이면 고유의 배경색 적용
        is_sel = (st.session_state.selected_meal == m_name)
        btn_style = f"background-color: {m_color} !important; color: white !important;" if is_sel else ""
        
        # 실제 클릭 감지용 Streamlit 버튼 (디자인은 CSS로 덮어씌움)
        if st.button(m_name, key=f"btn_{m_name}", use_container_width=True):
            st.session_state.selected_meal = m_name
            st.rerun()
st.write('</div>', unsafe_allow_html=True)

# 6. 추가 스타일 (Streamlit 기본 버튼을 그리드 아이템처럼 보이게 강제)
st.markdown(f"""
<style>
    div[data-testid="column"] button {{
        height: 50px !important;
        border: 1px solid #eee !important;
        font-size: 12px !important;
    }}
</style>
""", unsafe_allow_html=True)
