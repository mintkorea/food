import streamlit as st

# 1. 색상 테마 정의
color_theme = {
    "조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"
}

# 2. CSS: 모바일 전용 레이아웃 및 폰트 최적화
st.markdown(f"""
<style>
    /* 전체 컨테이너 폭 고정 (PC에서도 모바일처럼 보이게) */
    .main .block-container {{ 
        max-width: 450px !important; 
        padding: 10px !important; 
    }}

    /* 메인 카드: 하단 모서리 직각 (탭과 결합용) */
    .menu-card {{
        border: 3px solid var(--card-color);
        border-radius: 15px 15px 0 0;
        padding: 40px 15px;
        text-align: center;
        background-color: white;
        margin-bottom: 0px;
    }}

    /* 하단 인덱스 탭 그룹 */
    .index-tabs-bottom {{
        display: flex;
        width: 100%;
        gap: 2px; /* 버튼 사이 아주 미세한 간격 */
    }}

    /* 각 인덱스 탭 스타일: 폰트 크기 축소 */
    .tab-item-bottom {{
        flex: 1;
        text-align: center;
        padding: 12px 0;
        border-radius: 0 0 12px 12px; /* 아래쪽만 둥글게 */
        font-size: 12px !important; /* 모바일 대응 폰트 축소 */
        font-weight: bold;
        color: white;
        transition: all 0.2s;
    }}

    /* 라디오 버튼 영역: 완전 숨김 처리 (클릭 감지용으로만 작동) */
    div[data-testid="stRadio"] {{
        position: absolute;
        top: -1000px;
    }}
</style>
""", unsafe_allow_html=True)

# 초기 선택 상태
if 'selected_meal' not in st.session_state:
    st.session_state.selected_meal = "중식"

# 3. 상단 카드 UI
selected_color = color_theme[st.session_state.selected_meal]
st.markdown(f"""
    <div class="menu-card" style="--card-color: {selected_color};">
        <h1 style="color: {selected_color}; margin: 0; font-size: 28px;">{st.session_state.selected_meal}</h1>
        <p style="color: #666; margin-top: 8px; font-size: 13px;">선택한 식단의 메뉴를 확인하세요</p>
    </div>
""", unsafe_allow_html=True)

# 4. 하단 결합형 인덱스 UI (메뉴 아래로 이동)
tabs_html = '<div class="index-tabs-bottom">'
for meal, color in color_theme.items():
    # 선택된 탭은 진하게, 나머지는 연하게
    opacity = "1.0" if meal == st.session_state.selected_meal else "0.4"
    # 선택된 탭은 약간 더 길게 내려오도록 효과
    padding = "15px 0" if meal == st.session_state.selected_meal else "12px 0"
    tabs_html += f'<div class="tab-item-bottom" style="background-color: {color}; opacity: {opacity}; padding: {padding};">{meal}</div>'
tabs_html += '</div>'
st.markdown(tabs_html, unsafe_allow_html=True)

# 5. 실제 작동을 위한 버튼 (라디오 버튼 대신 클릭이 확실한 버튼 사용)
st.write("") # 간격 조절
cols = st.columns(5)
for i, meal in enumerate(color_theme.keys()):
    with cols[i]:
        # 버튼 텍스트를 숨기거나 작게 하여 인덱스 탭 위치와 매칭
        if st.button("●", key=f"btn_{meal}", help=f"{meal} 선택"):
            st.session_state.selected_meal = meal
            st.rerun()

# 버튼 스타일 미세 조정
st.markdown("""
    <style>
    div.stButton > button {
        width: 100%;
        border: none !important;
        background: transparent !important;
        color: #ddd !important;
        font-size: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)
