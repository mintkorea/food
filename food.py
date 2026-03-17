import streamlit as st

# 1. 데이터 및 테마 설정
color_theme = {
    "조식": {"idx": "#E95444", "bg": "#F9EBEA"},
    "간편식": {"idx": "#F1A33B", "bg": "#FEF5E7"},
    "중식": {"idx": "#8BC34A", "bg": "#F1F8E9"},
    "석식": {"idx": "#4A90E2", "bg": "#EBF5FB"},
    "야식": {"idx": "#673AB7", "bg": "#F4ECF7"}
}

if 'active_meal' not in st.session_state:
    st.session_state.active_meal = "중식"

current = st.session_state.active_meal
bold_c = color_theme[current]["idx"]
soft_bg = color_theme[current]["bg"]

# 2. CSS: 디자인 레이어와 클릭 레이어 겹치기
st.markdown(f"""
<style>
    .main .block-container {{ max-width: 450px !important; padding: 10px !important; }}
    
    /* [레이어 1] 눈에 보이는 가로 바 디자인 */
    .design-nav-bar {{
        display: flex !important;
        flex-direction: row !important;
        justify-content: space-between;
        width: 100%;
        margin-top: 20px;
        gap: 5px;
        pointer-events: none; /* 클릭이 아래(버튼)로 통과됨 */
    }}
    .nav-item {{
        flex: 1; text-align: center; padding: 12px 0;
        font-size: 13px; font-weight: bold; border-radius: 10px; color: white;
    }}

    /* [레이어 2] 실제 클릭되는 투명 버튼 위치 조정 */
    div[data-testid="stHorizontalBlock"] {{
        position: relative;
        margin-top: -45px !important; /* 디자인 바 위로 정확히 겹침 */
        z-index: 10;
        opacity: 0; /* 투명하게 만들어 디자인만 보이게 함 */
    }}
    div[data-testid="stHorizontalBlock"] button {{
        height: 45px !important;
        width: 100% !important;
        cursor: pointer !important;
    }}
    
    .meal-card {{
        background-color: {soft_bg}; border: 2px solid {bold_c};
        border-radius: 20px; padding: 30px 15px; text-align: center;
    }}
</style>
""", unsafe_allow_html=True)

# 3. UI 출력
st.title("🍴 오늘의 식사")

st.markdown(f"""
    <div class="meal-card">
        <h2 style="color: {bold_c};">{current}</h2>
        <p style="font-size: 22px; font-weight: bold; margin-top: 15px;">🍲 오늘의 추천 메뉴</p>
        <p style="color: #666; margin-top: 10px;">즉시 전환되는 식단 메뉴입니다.</p>
    </div>
""", unsafe_allow_html=True)

# 4. 가로 바 디자인 렌더링 (클릭 불가, 보기용)
nav_items = ""
for meal, info in color_theme.items():
    opacity = "1.0" if meal == current else "0.35"
    nav_items += f'<div class="nav-item" style="background-color: {info["idx"]}; opacity: {opacity};">{meal}</div>'
st.markdown(f'<div class="design-nav-bar">{nav_items}</div>', unsafe_allow_html=True)

# 5. 실제 클릭용 투명 버튼 (세로 쌓임 방지 위해 각 컬럼에 배치)
cols = st.columns(5)
for i, meal in enumerate(color_theme.keys()):
    with cols[i]:
        # 클릭 시 세션 상태만 바꾸고 새로고침은 발생하지 않음
        st.button(meal, key=f"btn_{meal}", on_click=lambda m=meal: setattr(st.session_state, 'active_meal', m), use_container_width=True)
