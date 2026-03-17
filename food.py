import streamlit as st

# 1. 색상 테마 정의
color_theme = {
    "조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"
}

# 2. CSS: 인덱스와 라디오 버튼 초정밀 정렬
st.markdown(f"""
<style>
    .main .block-container {{ 
        max-width: 500px !important; 
        padding: 20px 10px !important; 
    }}

    /* 상단 인덱스 탭 */
    .index-tabs {{
        display: flex;
        width: 100%;
        margin-bottom: -1px; /* 카드와 완벽 밀착 */
    }}

    .tab-item {{
        flex: 1;
        text-align: center;
        padding: 12px 0;
        border-radius: 12px 12px 0 0;
        font-size: 14px;
        font-weight: bold;
        color: white;
    }}

    /* 메인 카드 영역 */
    .menu-card {{
        border: 3px solid var(--card-color);
        border-radius: 0 0 15px 15px;
        padding: 40px 20px;
        text-align: center;
        background-color: white;
        margin-bottom: 10px;
    }}

    /* [핵심] 라디오 버튼 정밀 배치 */
    div[data-testid="stRadio"] {{
        margin-top: -460px; /* 카드를 뚫고 위로 올림 (높이에 따라 조정 필요) */
        position: relative;
        z-index: 10;
        background: transparent !important;
    }}
    
    div[data-testid="stRadio"] > div {{
        display: flex !important;
        flex-direction: row !important;
        background: transparent !important;
        padding: 0 !important;
    }}

    /* 각 라디오 버튼 항목을 탭과 동일한 flex 비율로 설정 */
    div[data-testid="stRadio"] label {{
        flex: 1;
        justify-content: center !important;
        align-items: center !important;
        height: 45px; /* 탭의 높이와 맞춤 */
        cursor: pointer;
    }}

    /* 라디오 버튼 원형만 남기고 텍스트는 배경색(투명/흰색) 처리 */
    div[data-testid="stRadio"] label p {{
        color: transparent !important; /* 텍스트 숨김 */
        font-size: 0px !important;
    }}

    /* 라디오 버튼 위치 조정 (탭 하단 중앙) */
    div[data-testid="stRadio"] label div:first-child {{
        margin-right: 0px !important;
        transform: scale(1.2);
        background-color: rgba(255,255,255,0.3); /* 살짝 비치게 하여 위치 가이드 역할 */
        border-radius: 50%;
    }}
</style>
""", unsafe_allow_html=True)

# 초기 선택 상태
if 'selected_meal' not in st.session_state:
    st.session_state.selected_meal = "중식"

# 3. 상단 인덱스 UI
tabs_html = '<div class="index-tabs">'
for meal, color in color_theme.items():
    opacity = "1.0" if meal == st.session_state.selected_meal else "0.4"
    tabs_html += f'<div class="tab-item" style="background-color: {color}; opacity: {opacity};">{meal}</div>'
tabs_html += '</div>'
st.markdown(tabs_html, unsafe_allow_html=True)

# 4. 카드 UI
selected_color = color_theme[st.session_state.selected_meal]
st.markdown(f"""
    <div class="menu-card" style="--card-color: {selected_color};">
        <h1 style="color: {selected_color}; margin: 0; font-size: 35px;">{st.session_state.selected_meal}</h1>
        <p style="color: #888; margin-top: 10px; font-size: 15px;">오늘의 식단을 확인하세요</p>
    </div>
""", unsafe_allow_html=True)

# 5. 투명 라디오 버튼 (인덱스 탭 위에 겹쳐서 클릭 감지)
# CSS의 margin-top을 통해 위 탭 위로 정확히 겹치게 배치했습니다.
selected = st.radio(
    "nav", 
    options=list(color_theme.keys()), 
    index=list(color_theme.keys()).index(st.session_state.selected_meal),
    horizontal=True,
    label_visibility="collapsed"
)

if selected != st.session_state.selected_meal:
    st.session_state.selected_meal = selected
    st.rerun()
