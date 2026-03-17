import streamlit as st

# 1. 색상 테마
color_theme = {
    "조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"
}

# 2. CSS: 모바일에서 절대 줄바꿈 금지 및 클릭 최적화
st.markdown(f"""
<style>
    /* 메인 컨테이너 폭 고정 */
    .main .block-container {{ 
        max-width: 500px !important; 
        padding: 10px !important; 
    }}

    /* 메뉴 카드 디자인 */
    .menu-card {{
        border: 3px solid var(--card-color);
        border-radius: 15px 15px 0 0;
        padding: 45px 15px;
        text-align: center;
        background-color: white;
    }}

    /* 인덱스 탭 디자인 (카드 아래 밀착) */
    .index-tabs-wrap {{
        display: flex;
        width: 100%;
        background-color: #eee;
        border-radius: 0 0 15px 15px;
        overflow: hidden;
    }}

    .tab-unit {{
        flex: 1;
        text-align: center;
        padding: 12px 0;
        font-size: 12px;
        font-weight: bold;
        color: white;
        border-right: 1px solid rgba(255,255,255,0.1);
    }}

    /* [핵심] 라디오 버튼 한 줄 강제 고정 및 텍스트 숨김 */
    div[data-testid="stRadio"] {{
        margin-top: 5px;
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 5px 0 !important;
    }}
    
    div[data-testid="stRadio"] > div {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important; /* 절대 줄바꿈 금지 */
        justify-content: space-around !important;
    }}

    /* 각 라디오 버튼의 클릭 영역을 20%로 균등 배분 */
    div[data-testid="stRadio"] label {{
        flex: 1 !important;
        min-width: unset !important;
        justify-content: center !important;
        margin: 0 !important;
        padding: 10px 0 !important;
    }}

    /* 라디오 버튼 옆의 텍스트를 숨겨서 동그라미만 보이게 */
    div[data-testid="stRadio"] label p {{
        display: none !important;
    }}

    /* 라디오 버튼 동그라미 크기 키우기 */
    div[data-testid="stRadio"] label div:first-child {{
        transform: scale(1.4);
    }}
</style>
""", unsafe_allow_html=True)

# 세션 상태
if 'selected_meal' not in st.session_state:
    st.session_state.selected_meal = "중식"

# 3. 상단 메뉴 카드
selected_color = color_theme[st.session_state.selected_meal]
st.markdown(f"""
    <div class="menu-card" style="--card-color: {selected_color};">
        <h1 style="color: {selected_color}; margin: 0; font-size: 30px;">{st.session_state.selected_meal}</h1>
        <p style="color: #666; margin-top: 8px; font-size: 14px;">선택한 식단의 메뉴를 확인하세요</p>
    </div>
""", unsafe_allow_html=True)

# 4. 하단 인덱스 탭 (카드와 붙음)
tabs_html = '<div class="index-tabs-wrap">'
for meal, color in color_theme.items():
    opacity = "1.0" if meal == st.session_state.selected_meal else "0.3"
    tabs_html += f'<div class="tab-unit" style="background-color: {color}; opacity: {opacity};">{meal}</div>'
tabs_html += '</div>'
st.markdown(tabs_html, unsafe_allow_html=True)

# 5. 선택용 라디오 버튼 (한 줄 고정)
# label_visibility="collapsed"로 제목을 숨기고 horizontal=True로 가로 배치
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
