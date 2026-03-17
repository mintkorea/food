import streamlit as st

# 1. 색상 테마 정의
color_theme = {
    "조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"
}

# 2. CSS: 인덱스 탭과 라디오 버튼의 일체화
st.markdown(f"""
<style>
    .main .block-container {{ 
        max-width: 500px !important; 
        padding: 15px 10px !important; 
    }}

    /* 상단 인덱스 탭 */
    .index-tabs {{
        display: flex;
        width: 100%;
        margin-bottom: -5px; /* 카드와 밀착 */
        position: relative;
        z-index: 2;
    }}

    .tab-item {{
        flex: 1;
        text-align: center;
        padding: 10px 0;
        border-radius: 12px 12px 0 0;
        font-size: 13px;
        font-weight: bold;
        color: white;
        transition: all 0.3s;
    }}

    /* 메인 카드 영역 */
    .menu-card {{
        border: 3px solid var(--card-color);
        border-radius: 0 0 15px 15px;
        padding: 35px 15px;
        text-align: center;
        background-color: white;
        position: relative;
        z-index: 1;
    }}

    /* [중요] 라디오 버튼 스타일 수정 (안 보이던 문제 해결) */
    div[data-testid="stRadio"] {{
        background-color: #f1f3f5;
        border-radius: 20px;
        padding: 5px 10px !important;
        margin-top: 10px !important;
    }}

    div[data-testid="stRadio"] > div {{
        display: flex !important;
        flex-direction: row !important;
        justify-content: space-around !important;
    }}

    /* 라디오 버튼의 텍스트를 투명하게 하고 동그라미만 강조 */
    div[data-testid="stRadio"] label {{
        padding: 0 !important;
        min-width: 50px;
        justify-content: center !important;
    }}

    div[data-testid="stRadio"] label p {{
        color: transparent !important; /* 텍스트 숨김 */
        font-size: 0px !important;
    }}

    /* 선택된 라디오 버튼 색상을 현재 테마색으로 변경 */
    div[data-testid="stRadio"] div[data-testid="stMarkdownContainer"] {{
        display: none;
    }}
</style>
""", unsafe_allow_html=True)

# 초기 선택 상태
if 'selected_meal' not in st.session_state:
    st.session_state.selected_meal = "중식"

# 3. 상단 인덱스 UI (이미지 3번 스타일)
tabs_html = '<div class="index-tabs">'
for meal, color in color_theme.items():
    opacity = "1.0" if meal == st.session_state.selected_meal else "0.3"
    # 선택된 탭은 위로 살짝 올라오게 효과
    margin = "-5px" if meal == st.session_state.selected_meal else "0px"
    tabs_html += f'<div class="tab-item" style="background-color: {color}; opacity: {opacity}; margin-top: {margin};">{meal}</div>'
tabs_html += '</div>'
st.markdown(tabs_html, unsafe_allow_html=True)

# 4. 카드 UI
selected_color = color_theme[st.session_state.selected_meal]
st.markdown(f"""
    <div class="menu-card" style="--card-color: {selected_color};">
        <h1 style="color: {selected_color}; margin: 0; font-size: 30px;">{st.session_state.selected_meal}</h1>
        <p style="color: #666; margin-top: 5px; font-size: 14px;">선택한 식단의 메뉴를 확인하세요</p>
    </div>
""", unsafe_allow_html=True)

# 5. 하단 컨트롤러 (이미지 3번 하단 라디오 버튼 스타일)
# 이제 margin-top으로 숨기지 않고 카드 바로 아래에 배치하여 '버튼' 역할을 하게 합니다.
selected = st.radio(
    "식단 선택", 
    options=list(color_theme.keys()), 
    index=list(color_theme.keys()).index(st.session_state.selected_meal),
    horizontal=True,
    label_visibility="collapsed"
)

if selected != st.session_state.selected_meal:
    st.session_state.selected_meal = selected
    st.rerun()
