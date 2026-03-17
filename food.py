import streamlit as st

# 1. 색상 테마 정의
color_theme = {
    "조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"
}

# 2. CSS: 텍스트 강제 가로 정렬 및 모바일 최적화
st.markdown(f"""
<style>
    /* 전체 컨테이너 너비 제한 (가시성 확보) */
    .main .block-container {{ 
        max-width: 500px !important; 
        padding: 10px !important; 
    }}

    /* 메뉴 카드 디자인 */
    .menu-card {{
        border: 3px solid var(--card-color);
        border-radius: 15px 15px 0 0;
        padding: 40px 15px;
        text-align: center;
        background-color: white;
    }}

    /* 인덱스 탭 (카드 하단 부착) */
    .index-tabs-wrap {{
        display: flex;
        width: 100%;
        margin-bottom: 5px;
    }}

    .tab-unit {{
        flex: 1;
        text-align: center;
        padding: 12px 0;
        font-size: 11px !important; /* 모바일 대응 폰트 축소 */
        font-weight: bold;
        color: white;
        border-radius: 0 0 5px 5px;
    }}

    /* [핵심] 라디오 버튼 가로 강제 정렬 */
    div[data-testid="stRadio"] > div {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important; /* 절대 줄바꿈 금지 */
        justify-content: space-between !important;
        background-color: #f8f9fa;
        padding: 8px 5px !important;
        border-radius: 10px;
    }}

    /* 라디오 버튼 항목 너비 고정 */
    div[data-testid="stRadio"] label {{
        flex: 1 !important;
        white-space: nowrap !important; /* 텍스트 줄바꿈 금지 */
        justify-content: center !important;
        margin: 0 !important;
        padding: 0 !important;
    }}

    /* 텍스트 크기 조절 (중간 배치용) */
    div[data-testid="stRadio"] label p {{
        font-size: 11px !important;
        font-weight: bold;
        color: #555 !important;
    }}

    /* 라디오 버튼 원형 크기 조절 */
    div[data-testid="stRadio"] label div:first-child {{
        transform: scale(0.9);
    }}
</style>
""", unsafe_allow_html=True)

# 세션 상태 관리
if 'selected_meal' not in st.session_state:
    st.session_state.selected_meal = "중식"

# 3. 상단 메뉴 카드 UI
selected_color = color_theme[st.session_state.selected_meal]
st.markdown(f"""
    <div class="menu-card" style="--card-color: {selected_color};">
        <h1 style="color: {selected_color}; margin: 0; font-size: 28px;">{st.session_state.selected_meal}</h1>
        <p style="color: #666; margin-top: 8px; font-size: 13px;">선택한 식단의 메뉴를 확인하세요</p>
    </div>
""", unsafe_allow_html=True)

# 4. 하단 인덱스 탭 UI
tabs_html = '<div class="index-tabs-wrap">'
for meal, color in color_theme.items():
    opacity = "1.0" if meal == st.session_state.selected_meal else "0.3"
    tabs_html += f'<div class="tab-unit" style="background-color: {color}; opacity: {opacity};">{meal}</div>'
tabs_html += '</div>'
st.markdown(tabs_html, unsafe_allow_html=True)

# 5. [사용자 제안] 텍스트가 포함된 라디오 버튼 (간격 유지의 핵심)
selected = st.radio(
    "meal_selector",
    options=list(color_theme.keys()),
    index=list(color_theme.keys()).index(st.session_state.selected_meal),
    horizontal=True,
    label_visibility="collapsed"
)

if selected != st.session_state.selected_meal:
    st.session_state.selected_meal = selected
    st.rerun()
