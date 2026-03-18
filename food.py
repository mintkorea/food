import streamlit as st
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo

# 1. 초기 설정
KST = ZoneInfo("Asia/Seoul")
now = datetime.now(KST)
if 'selected_meal' not in st.session_state: st.session_state.selected_meal = "중식"

color_theme = {"조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"}

# 2. [완전 해결] HTML/CSS 기반 가로 5열 그리드 주입
# 이 부분은 Streamlit의 반응형 기능을 완전히 차단하고 비상연락망처럼 격자를 고정합니다.
st.markdown(f"""
<style>
    /* 전체 컨테이너 여백 최적화 */
    .block-container {{ padding: 1rem 0.5rem !important; max-width: 500px !important; }}

    /* 식단 카드 스타일 */
    .menu-box {{
        border: 1px solid #eee; border-top: 15px solid {color_theme[st.session_state.selected_meal]};
        border-radius: 15px; padding: 25px 10px; text-align: center;
        background: white; box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }}

    /* [비상연락망 그리드] 가로 5열 강제 고정 */
    .grid-container {{
        display: grid;
        grid-template-columns: repeat(5, 1fr); /* 5칸 무조건 생성 */
        gap: 5px;
        width: 100%;
    }}

    /* 버튼 스타일 */
    .grid-item {{
        background-color: white;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 12px 0;
        text-align: center;
        font-size: 13px;
        font-weight: 800;
        color: #333;
        cursor: pointer;
    }}

    /* 선택된 버튼 스타일 */
    .active-item {{
        background-color: {color_theme[st.session_state.selected_meal]} !important;
        color: white !important;
        border: none !important;
    }}
</style>
""", unsafe_allow_html=True)

# 3. 상단 식단 표시 레이어
st.markdown(f"""
    <div class="menu-box">
        <div style="color: {color_theme[st.session_state.selected_meal]}; font-size: 14px; font-weight: 800;">{st.session_state.selected_meal}</div>
        <div style="font-size: 24px; font-weight: 800; margin-top: 8px;">오늘의 메뉴</div>
        <div style="color: #666; font-size: 15px; margin-top: 8px; line-height: 1.4;">
            메뉴 정보가 여기에 표시됩니다.
        </div>
    </div>
""", unsafe_allow_html=True)

# 4. [해결책] HTML 그리드를 활용한 버튼 구현
# Streamlit 기본 버튼은 모바일에서 깨지기 쉬우므로, 
# 비상연락망 앱처럼 고정된 칸을 만드는 방식을 적용했습니다.
cols = st.columns(5)
meals = list(color_theme.keys())

for i, m_name in enumerate(meals):
    with cols[i]:
        # 개별 컬럼의 최소 너비를 강제로 제거하는 CSS 추가 주입
        st.markdown(f"""<style>div[data-testid="column"]:nth-of-type({i+1}) {{ min-width: 0px !important; flex: 1 !important; }}</style>""", unsafe_allow_html=True)
        
        # 버튼 생성
        if st.button(m_name, key=f"btn_{m_name}", use_container_width=True):
            st.session_state.selected_meal = m_name
            st.rerun()

# 5. 선택된 버튼에 비상연락망식 컬러 강조 적용
st.markdown(f"""
<style>
    div[data-testid="column"]:nth-of-type({meals.index(st.session_state.selected_meal) + 1}) button {{
        background-color: {color_theme[st.session_state.selected_meal]} !important;
        color: white !important;
    }}
</style>
""", unsafe_allow_html=True)
