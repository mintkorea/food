import streamlit as st

# 1. 상태 관리 설정
if 'selected_meal' not in st.session_state:
    st.session_state.selected_meal = "중식"

# 식단별 테마 색상
color_map = {
    "조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"
}

# 2. [핵심] 모바일 그리드 사수 CSS
# 비상연락망 앱처럼 좁은 화면에서도 줄바꿈 없이 5칸을 유지합니다.
st.markdown(f"""
<style>
    /* 전체 컨테이너 폭 최적화 */
    .block-container {{ padding: 1rem 0.5rem !important; max-width: 500px !important; }}
    
    /* 가로 배열 강제 유지 (flex-wrap 차단) */
    div[data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 4px !important;
    }}
    
    /* 각 컬럼의 최소 너비 해제 및 20% 배분 */
    div[data-testid="column"] {{
        min-width: 0px !important;
        flex: 1 1 20% !important;
    }}

    /* 버튼 스타일 (비상연락망처럼 폰트 축소 및 높이 고정) */
    button {{
        width: 100% !important;
        height: 42px !important;
        padding: 0 !important;
        font-size: 11px !important; 
        font-weight: 800 !important;
        border-radius: 8px !important;
    }}
</style>
""", unsafe_allow_html=True)

# 3. 상단 식단 카드 레이어
selected = st.session_state.selected_meal
st.markdown(f"""
    <div style="border: 1px solid #eee; border-top: 15px solid {color_map[selected]}; 
                border-radius: 15px; padding: 25px 10px; text-align: center; 
                background: white; box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 20px;">
        <div style="color: {color_map[selected]}; font-size: 14px; font-weight: 800;">{selected}</div>
        <div style="font-size: 22px; font-weight: 800; margin-top: 10px;">오늘의 메뉴</div>
        <div style="color: #666; font-size: 15px; margin-top: 10px; line-height: 1.5;">
            메뉴 정보를 연동하면<br>여기에 상세 내용이 표시됩니다.
        </div>
    </div>
""", unsafe_allow_html=True)

# 4. 버튼 그리드 레이어 배치
cols = st.columns(5)
meals = list(color_map.keys())

for i, m_name in enumerate(meals):
    with cols[i]:
        if st.button(m_name, key=f"btn_{m_name}", use_container_width=True):
            st.session_state.selected_meal = m_name
            st.rerun()

# 5. 선택된 버튼에 비상연락망식 컬러 강조
st.markdown(f"""
<style>
    div[data-testid="column"]:nth-of-type({meals.index(selected) + 1}) button {{
        background-color: {color_map[selected]} !important;
        color: white !important;
        border: none !important;
    }}
</style>
""", unsafe_allow_html=True)
