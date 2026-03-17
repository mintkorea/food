import streamlit as st

# 1. 색상 테마 정의
color_theme = {
    "조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"
}

# 2. CSS: 인덱스 파일 디자인 및 라디오 버튼 가로 고정
st.markdown(f"""
<style>
    /* 메인 컨테이너 최적화 (모바일용) */
    .main .block-container {{ 
        max-width: 500px !important; 
        padding: 10px 5px !important; 
    }}

    /* [디자인] 상단 인덱스 탭 그룹 */
    .index-tabs {{
        display: flex;
        justify-content: space-around;
        width: 100%;
        margin-bottom: -3px; /* 카드와 밀착 */
    }}

    /* 각 인덱스 탭 스타일 */
    .tab-item {{
        flex: 1;
        text-align: center;
        padding: 10px 0;
        border-radius: 10px 10px 0 0; /* 윗부분만 둥글게 */
        font-size: 14px;
        font-weight: bold;
        color: white;
        text-shadow: 0 1px 2px rgba(0,0,0,0.2);
    }}

    /* [기능] 라디오 버튼 가로 고정 */
    div[data-testid="stRadio"] > div {{
        display: flex !important;
        flex-direction: row !important;
        justify-content: space-around !important;
        background-color: #f8f9fa;
        padding: 10px 5px;
        border-radius: 0 0 15px 15px; /* 아래부분만 둥글게 */
    }}

    /* 라디오 버튼 원형 크기 및 간격 조절 */
    div[data-testid="stRadio"] label div:first-child {{
        transform: scale(1.1);
        margin: 0 !important;
    }}

    /* 불필요한 레이블 숨기기 */
    div[data-testid="stRadio"] > label {{ display: none !important; }}
</style>
""", unsafe_allow_html=True)

# 초기 선택 상태 설정
if 'selected_meal' not in st.session_state:
    st.session_state.selected_meal = "중식"

# 3. 디자인 영역: HTML 인덱스 파일 디자인 (첫 번째 이미지 기반)
tabs_html = '<div class="index-tabs">'
for meal, color in color_theme.items():
    # 선택된 메뉴는 선명하게, 나머지는 불투명하게
    opacity = "1.0" if meal == st.session_state.selected_meal else "0.3"
    tabs_html += f'<div class="tab-item" style="background-color: {color}; opacity: {opacity};">{meal}</div>'
tabs_html += '</div>'

st.markdown(tabs_html, unsafe_allow_html=True)

# 4. 카드 영역 디자인
selected_color = color_theme[st.session_state.selected_meal]
st.markdown(f"""
    <div style="border: 3px solid {selected_color}; border-radius: 0 0 15px 15px; padding: 30px; text-align: center; background-color: white;">
        <h1 style="color: {selected_color}; margin: 0; font-size: 32px;">{st.session_state.selected_meal}</h1>
        <p style="color: #666; margin-top: 5px;">선택한 식단의 메뉴를 확인하세요</p>
    </div>
""", unsafe_allow_html=True)

# 5. 기능 영역: 가로 라디오 버튼 배치 (세 번째 이미지 기반)
# 레이블을 collapsed로 설정하여 불필요한 제목을 숨깁니다.
selected = st.radio(
    "meal_nav", 
    options=list(color_theme.keys()), 
    index=list(color_theme.keys()).index(st.session_state.selected_meal),
    horizontal=True,
    label_visibility="collapsed" 
)

# 선택 값이 바뀌면 세션 상태 업데이트 후 새로고침
if selected != st.session_state.selected_meal:
    st.session_state.selected_meal = selected
    st.rerun()
