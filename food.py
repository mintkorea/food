import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# 1. 기초 설정
KST = ZoneInfo("Asia/Seoul")
def get_now(): return datetime.now(KST)

st.set_page_config(page_title="성의교정 식단", page_icon="🍴", layout="centered")

# 2. 상태 관리
now = get_now()
if 'target_date' not in st.session_state: st.session_state.target_date = now.date()
if 'selected_meal' not in st.session_state: st.session_state.selected_meal = "중식"

color_theme = {"조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"}

# 3. [핵심] 모바일 가로 5열 강제 고정 CSS
# Streamlit의 컬럼 레이아웃을 무시하고 가로 한 줄 배치를 강제합니다.
st.markdown(f"""
<style>
    .block-container {{ padding: 1rem 0.5rem !important; max-width: 500px !important; }}
    
    /* [해결책] 가로 줄바꿈 방지 및 5열 강제 배정 */
    div[data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-direction: row !important; /* 가로 방향 고정 */
        flex-wrap: nowrap !important;   /* 세로 줄바꿈 금지 */
        gap: 5px !important;
    }}
    
    /* 각 컬럼의 최소 폭을 제거하고 전체의 20%로 고정 */
    div[data-testid="column"] {{
        width: 20% !important;
        flex: 1 1 20% !important;
        min-width: 0px !important;
    }}

    /* 버튼 디자인 최적화 */
    button {{
        height: 42px !important;
        padding: 0 !important;
        font-size: 12px !important;
        font-weight: 800 !important;
        border-radius: 8px !important;
    }}
    
    /* 식단 카드 스타일 */
    .menu-card {{ 
        border: 1px solid #eee; 
        border-top: 15px solid {color_theme[st.session_state.selected_meal]};
        border-radius: 15px; padding: 20px 10px; text-align: center; 
        background: white; box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }}
</style>
""", unsafe_allow_html=True)

# 4. 화면 구성 (날짜 표시)
d = st.session_state.target_date
st.markdown(f'<div style="text-align:center; font-size:20px; font-weight:800; margin-bottom:15px;">📅 {d.strftime("%m월 %d일")}</div>', unsafe_allow_html=True)

# 5. 식단 카드 (상단)
# (데이터 로드 로직은 기존 코드 유지)
st.markdown(f"""
    <div class="menu-card">
        <div style="color: {color_theme[st.session_state.selected_meal]}; font-size: 13px; font-weight: 800;">{st.session_state.selected_meal}</div>
        <div style="font-size: 22px; font-weight: 800; margin-top: 10px;">오늘의 메뉴</div>
        <div style="color: #666; font-size: 15px; margin-top: 10px;">식단 정보를 불러오세요</div>
    </div>
""", unsafe_allow_html=True)

# 6. [결과] 가로 5열 버튼 그리드
cols = st.columns(5)
for i, m_name in enumerate(color_theme.keys()):
    with cols[i]:
        if st.button(m_name, key=f"btn_{i}", use_container_width=True):
            st.session_state.selected_meal = m_name
            st.rerun()

# 선택된 버튼 색상 강조
st.markdown(f"""
<style>
    div[data-testid="column"]:nth-of-type({list(color_theme.keys()).index(st.session_state.selected_meal) + 1}) button {{
        background-color: {color_theme[st.session_state.selected_meal]} !important;
        color: white !important;
    }}
</style>
""", unsafe_allow_html=True)
