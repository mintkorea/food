import streamlit as st

# 1. 초기 상태 설정
if 'selected_meal' not in st.session_state:
    st.session_state.selected_meal = "중식"

color_map = {
    "조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"
}

# 2. [핵심] 모바일 강제 가로 정렬 CSS
st.markdown(f"""
<style>
    /* 1. 컬럼들이 세로로 쌓이는 것을 원천 차단 */
    div[data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 5px !important;
    }}
    
    /* 2. 각 버튼 칸의 최소 너비를 없애고 5등분 강제 */
    div[data-testid="column"] {{
        min-width: 0px !important;
        flex: 1 !important;
    }}

    /* 3. 버튼 디자인 (글자 크기를 줄여서 한 칸에 쏙 들어가게 함) */
    button {{
        width: 100% !important;
        height: 40px !important;
        padding: 0 !important;
        font-size: 11px !important; /* 비상연락망처럼 폰트 축소 */
        font-weight: 800 !important;
        border-radius: 6px !important;
    }}
</style>
""", unsafe_allow_html=True)

# 3. 식단 표시 카드 (상단 레이어)
selected = st.session_state.selected_meal
st.markdown(f"""
    <div style="border: 1px solid #eee; border-top: 10px solid {color_map[selected]}; 
                border-radius: 12px; padding: 20px; text-align: center; background: white; 
                box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 15px;">
        <div style="color: {color_map[selected]}; font-size: 14px; font-weight: bold;">{selected}</div>
        <div style="font-size: 22px; font-weight: 800; margin: 10px 0;">오늘의 식단 메뉴</div>
        <div style="color: #666; font-size: 14px;">메뉴 정보를 연동해 주세요.</div>
    </div>
""", unsafe_allow_html=True)

# 4. [작동 보장] 가로 5열 버튼 배치
cols = st.columns(5)
meals = list(color_map.keys())

for i, m_name in enumerate(meals):
    with cols[i]:
        # 개별 버튼 생성
        if st.button(m_name, key=f"btn_{m_name}"):
            st.session_state.selected_meal = m_name
            st.rerun()

# 5. [비상연락망식] 선택된 버튼에만 테마색 입히기
st.markdown(f"""
<style>
    div[data-testid="column"]:nth-of-type({meals.index(selected) + 1}) button {{
        background-color: {color_map[selected]} !important;
        color: white !important;
        border: none !important;
    }}
</style>
""", unsafe_allow_html=True)
