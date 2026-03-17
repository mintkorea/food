import streamlit as st

# 1. 색상 및 데이터 설정
menu_data = {
    "조식": {"color": "#E95444", "light": "#FADEDC"},
    "간편식": {"color": "#F1A33B", "light": "#FDF0D9"},
    "중식": {"color": "#8BC34A", "light": "#E8F5E9"},
    "석식": {"color": "#4A90E2", "light": "#E3F2FD"},
    "야식": {"color": "#673AB7", "light": "#EDE7F6"}
}

if 'active_meal' not in st.session_state:
    st.session_state.active_meal = "중식"

current = st.session_state.active_meal
current_color = menu_data[current]["color"]

# 2. CSS: 이미지의 '아래쪽 안' 디자인 구현
st.markdown(f"""
<style>
    .main .block-container {{ max-width: 450px !important; padding: 10px !important; }}
    
    /* 상단 식단 카드 */
    .meal-card {{
        border: 2px solid {current_color};
        border-radius: 20px;
        padding: 30px 10px;
        text-align: center;
        background-color: white;
        margin-bottom: 20px;
    }}
    
    /* 버튼 컨테이너 (5개 가로 정렬) */
    .button-group {{
        display: flex;
        justify-content: space-between;
        gap: 5px;
    }}
    
    /* 개별 버튼 세트 (버튼 + 라디오 원형) */
    .btn-item {{
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 8px;
    }}

    /* 메뉴 버튼 스타일 */
    .menu-btn {{
        width: 100%;
        padding: 12px 0;
        border-radius: 10px;
        font-size: 13px;
        font-weight: bold;
        color: white;
        text-align: center;
        text-decoration: none;
    }}
    
    /* 라디오 버튼 모양 (원형 표시) */
    .radio-dot {{
        width: 16px;
        height: 16px;
        border: 2px solid #333;
        border-radius: 50%;
        background-color: white;
    }}
    
    .radio-dot.active {{
        background-color: {current_color}; /* 선택된 색상으로 채움 */
        border-color: {current_color};
    }}
</style>
""", unsafe_allow_html=True)

# 3. 상단 제목 및 메인 카드
st.markdown('<h2 style="text-align:center; color:#333;">🍴 오늘의 식단</h2>', unsafe_allow_html=True)
st.markdown(f"""
    <div class="meal-card">
        <h1 style="color: {current_color}; margin: 0;">{current}</h1>
        <p style="color: #666; margin-top: 10px;">원하시는 식단을 탭하세요</p>
    </div>
""", unsafe_allow_html=True)

# 4. 버튼 및 라디오 버튼 레이아웃
cols = st.columns(5)
meal_names = list(menu_data.keys())

for i, name in enumerate(meal_names):
    with cols[i]:
        # 버튼 출력
        if st.button(name, key=f"btn_{name}"):
            st.session_state.active_meal = name
            st.rerun()
        
        # 버튼 아래 원형 표시 (CSS로 active 클래스 제어)
        is_active = "active" if name == current else ""
        st.markdown(f'<div class="btn-item"><div class="radio-dot {is_active}"></div></div>', unsafe_allow_html=True)

# 5. 선택된 메뉴의 상세 식단 (예시)
st.divider()
st.subheader(f"🍱 {current} 메뉴")
st.info(f"현재 {current}에 준비된 맛있는 식단을 확인하세요!")
