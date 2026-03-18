import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# 1. 페이지 설정 및 상태 관리
KST = ZoneInfo("Asia/Seoul")
now = datetime.now(KST)
if 'target_date' not in st.session_state: st.session_state.target_date = now.date()
if 'selected_meal' not in st.session_state: st.session_state.selected_meal = "중식"

color_theme = {"조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"}

# 2. [강력 해결] CSS를 통한 가로 그리드 강제 주입
st.markdown(f"""
<style>
    /* 전체 화면 중앙 정렬 및 여백 최적화 */
    .block-container {{ padding: 1rem 0.5rem !important; max-width: 500px !important; }}
    
    /* [핵심] 가로 5열 강제 고정 (비상연락망 그리드 방식) */
    div[data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-direction: row !important; /* 무조건 가로 */
        flex-wrap: nowrap !important;   /* 줄바꿈 절대 금지 */
        gap: 4px !important;            /* 버튼 사이 간격 */
    }}
    
    /* 각 버튼 칸의 크기를 20%로 강제 지정 */
    div[data-testid="column"] {{
        width: 20% !important;
        flex: 1 1 20% !important;
        min-width: 0px !important;      /* 최소 너비 제한 해제 */
    }}

    /* 버튼 기본 스타일: 클릭 영역을 키우고 폰트 조절 */
    button {{
        height: 50px !important;
        padding: 0px !important;
        font-size: 13px !important;
        font-weight: 800 !important;
        border-radius: 8px !important;
        border: 1px solid #ddd !important;
    }}
</style>
""", unsafe_allow_html=True)

# 3. 상단 날짜 및 식단 카드 (생략 가능, 기존 로직 유지)
d = st.session_state.target_date
st.markdown(f'<div style="text-align:center; font-size:22px; font-weight:800; margin-bottom:15px;">📅 {d.strftime("%m월 %d일")}</div>', unsafe_allow_html=True)

# 식단 카드 레이어
st.markdown(f"""
    <div style="border: 1px solid #eee; border-top: 15px solid {color_theme[st.session_state.selected_meal]};
                border-radius: 15px; padding: 25px 15px; text-align: center; background: white; 
                box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 20px;">
        <div style="color: {color_theme[st.session_state.selected_meal]}; font-size: 14px; font-weight: 800;">{st.session_state.selected_meal}</div>
        <div style="font-size: 24px; font-weight: 800; margin-top: 10px;">뼈있는닭볶음탕</div>
        <div style="color: #666; font-size: 15px; margin-top: 10px;">데이터 연동 시 메뉴가 표시됩니다.</div>
    </div>
""", unsafe_allow_html=True)

# 4. [해결] 5개 버튼 배치
cols = st.columns(5)
meals = list(color_theme.keys())

for i, m_name in enumerate(meals):
    with cols[i]:
        if st.button(m_name, key=f"meal_btn_{m_name}", use_container_width=True):
            st.session_state.selected_meal = m_name
            st.rerun()

# 5. 선택된 버튼 색상 강조 (비상연락망의 컬러 구분 방식)
st.markdown(f"""
<style>
    div[data-testid="column"]:nth-of-type({meals.index(st.session_state.selected_meal) + 1}) button {{
        background-color: {color_theme[st.session_state.selected_meal]} !important;
        color: white !important;
        border: none !important;
    }}
</style>
""", unsafe_allow_html=True)
