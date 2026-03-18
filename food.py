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

# 2. 상태 관리
now = get_now()
if 'target_date' not in st.session_state: st.session_state.target_date = now.date()
if 'selected_meal' not in st.session_state: st.session_state.selected_meal = "중식"

CSV_URL = "https://docs.google.com/spreadsheets/d/1l07s4rubmeB5ld8oJayYrstL34UPKtxQwYptIocgKV0/export?format=csv"
meal_data = load_meal_data(CSV_URL)
color_theme = {"조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"}

# 3. CSS (상단 카드 및 레이아웃)
st.markdown(f"""
<style>
    .block-container {{ padding: 1rem 0.5rem !important; max-width: 500px !important; }}
    header {{ visibility: hidden; }}
    .menu-card {{ 
        border: 1px solid #ddd; border-top: 15px solid {color_theme[st.session_state.selected_meal]};
        border-radius: 20px; padding: 25px 15px; text-align: center; 
        background: white; box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }}
    /* 모바일에서 버튼이 수직으로 쌓이는 것을 방지하기 위해 기본 버튼 숨김 처리 고려 가능 */
</style>
""", unsafe_allow_html=True)

# 4. 화면 구성
d = st.session_state.target_date
w_list = ["월","화","수","목","금","토","일"]
st.markdown(f'<div style="text-align:center; font-size:22px; font-weight:800; margin-bottom:15px;">📅 {d.strftime("%m월 %d일")} ({w_list[d.weekday()]})</div>', unsafe_allow_html=True)

# 날짜 변경 (이 부분은 기존 버튼 유지)
c1, c2, c3 = st.columns(3)
with c1: 
    if st.button("◀ 이전날", use_container_width=True): st.session_state.target_date -= timedelta(1); st.rerun()
with c2:
    if st.button("오늘", use_container_width=True): st.session_state.target_date = now.date(); st.rerun()
with c3:
    if st.button("다음날 ▶", use_container_width=True): st.session_state.target_date += timedelta(1); st.rerun()

# 식단 카드
key = (d.strftime("%Y-%m-%d"), st.session_state.selected_meal)
meal_info = meal_data.get(key, {"menu": "정보 없음", "side": "식단 정보가 없습니다."})

st.markdown(f"""
    <div class="menu-card">
        <div style="color: {color_theme[st.session_state.selected_meal]}; font-size: 14px; font-weight: 800; margin-bottom: 5px;">{st.session_state.selected_meal}</div>
        <div style="font-size: 24px; font-weight: 800; color: #111; margin-bottom: 12px;">{meal_info['menu']}</div>
        <div style="color: #555; font-size: 15px; line-height: 1.4;">{meal_info['side']}</div>
    </div>
""", unsafe_allow_html=True)

# 5. [강력 해결] HTML 컴포넌트를 이용한 가로 그리드 버튼
# Streamlit의 컬럼 제약을 벗어나기 위해 직접 HTML 그리드를 작성합니다.
button_html = f"""
<div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; font-family: sans-serif;">
    {" ".join([f'''
    <div onclick="window.parent.postMessage({{type: 'streamlit:set_component_value', value: '{m}'}}, '*')"
         style="background: {color_theme[m] if st.session_state.selected_meal == m else '#f0f2f6'};
                color: {'white' if st.session_state.selected_meal == m else '#666'};
                border-radius: 10px; padding: 15px 0; text-align: center; 
                font-weight: bold; font-size: 14px; cursor: pointer; border: 1px solid #ddd;">
        {m}
    </div>''' for m in color_theme.keys()])}
</div>
"""

# HTML 버튼의 클릭 이벤트를 Streamlit 상태와 연결
res = components.html(f"""
    <script>
    function sendValue(val) {{
        window.parent.postMessage({{
            type: 'streamlit:set_component_value',
            value: val
        }}, '*');
    }}
    </script>
    {button_html.replace("window.parent.postMessage", "sendValue")}
""", height=70)

# 만약 HTML 컴포넌트에서 값이 넘어오면 상태 업데이트 (테스트용으로 radio 대체 사용 권장)
# 현재 환경에서 가장 확실한 방법은 아래의 CSS 주입형 radio입니다.

st.markdown("""
<style>
    /* Radio 컨테이너 가로 정렬 강제 */
    div[data-testid="stRadio"] > div {
        display: flex !important;
        flex-direction: row !important;
        justify-content: space-between !important;
        width: 100% !important;
        gap: 5px !important;
    }
    div[data-testid="stRadio"] label {
        flex: 1 !important;
        background-color: #f8f9fa !important;
        border: 1px solid #eee !important;
        border-radius: 10px !important;
        padding: 10px 0 !important;
        justify-content: center !important;
    }
    div[data-testid="stRadio"] label div:first-child { display: none !important; } /* 동그라미 제거 */
    
    /* 선택된 버튼 색상 - 위에서 정의한 컬러 테마와 맞춤 */
    div[data-testid="stRadio"] label[data-selected="true"] { background-color: #1E3A5F !important; } 
    div[data-testid="stRadio"] label[data-selected="true"] p { color: white !important; }
</style>
""", unsafe_allow_html=True)

selected = st.radio("식사", options=list(color_theme.keys()), 
                    index=list(color_theme.keys()).index(st.session_state.selected_meal),
                    horizontal=True, label_visibility="collapsed")

if selected != st.session_state.selected_meal:
    st.session_state.selected_meal = selected
    st.rerun()
