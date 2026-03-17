import streamlit as st

# 1. 설정
menu_cfg = {
    "조": "#E95444", "간": "#F1A33B", "중": "#8BC34A", "석": "#4A90E2", "야": "#673AB7"
}

if 'active_meal' not in st.session_state:
    st.session_state.active_meal = "중"

current = st.session_state.active_meal
current_color = menu_cfg[current]

# 2. CSS: 버튼 간격과 글자 크기를 완벽하게 제어
st.markdown(f"""
<style>
    .main .block-container {{ max-width: 500px !important; padding: 10px !important; }}

    /* 탭 메뉴 컨테이너 */
    .custom-tab-bar {{
        display: flex;
        justify-content: center; /* 중앙 정렬 */
        gap: 8px; /* 여기서 버튼 사이의 실제 간격을 조절합니다 */
        width: 100%;
        margin-bottom: -4px;
    }}

    /* 개별 탭 버튼 디자인 */
    .tab-btn {{
        flex: 1;
        padding: 12px 0;
        text-align: center;
        font-size: 20px !important;
        font-weight: 900;
        border-radius: 12px 12px 0 0;
        cursor: pointer;
        border: none;
        transition: 0.3s;
        text-decoration: none;
        display: inline-block;
    }}

    /* 비활성 탭: 배경색과 글자색을 동일하게 하여 '간격용 벽' 역할 수행 */
    .tab-inactive {{
        background-color: #f0f2f6;
        color: #f0f2f6; /* 글자를 숨겨서 간격을 벌림 */
    }}

    /* 활성 탭: 테마 색상 적용 및 글자 노출 */
    .tab-active {{
        background-color: {current_color};
        color: white !important;
        box-shadow: 0 -4px 10px rgba(0,0,0,0.1);
    }}

    /* 하단 인덱스 카드 */
    .index-body {{
        border: 4px solid {current_color};
        border-radius: 0 0 20px 20px;
        padding: 50px 20px;
        text-align: center;
        background-color: white;
    }}
</style>
""", unsafe_allow_html=True)

# 3. HTML로 구현한 탭 바 (st.button 대신 query_params나 상태 업데이트 활용)
# Streamlit의 radio 대신 직접 버튼을 시뮬레이션합니다.
cols = st.columns(5)
meals = list(menu_cfg.keys())

# 버튼 배치 영역
for i, meal in enumerate(meals):
    with cols[i]:
        # 선택 여부에 따른 클래스 결정
        is_active = meal == current
        # 버튼을 누르면 상태 변경
        if st.button(meal, key=f"m_{meal}", use_container_width=True):
            st.session_state.active_meal = meal
            st.rerun()

# 4. 하단 일체형 카드 디자인
full_names = {"조": "조식", "간": "간편식", "중": "중식", "석": "석식", "야": "야식"}
st.markdown(f"""
    <div class="index-body">
        <h2 style="color: {current_color}; margin: 0; font-size: 24px;">{full_names[current]}</h2>
        <h1 style="color: {current_color}; margin: 10px 0; font-size: 48px; font-weight: 900;">MENU</h1>
    </div>
""", unsafe_allow_html=True)
