import streamlit as st
import streamlit.components.v1 as components

# 1. 데이터 설정
color_theme = {
    "조식": {"idx": "#E95444", "bg": "#F9EBEA"},
    "간편식": {"idx": "#F1A33B", "bg": "#FEF5E7"},
    "중식": {"idx": "#8BC34A", "bg": "#F1F8E9"},
    "석식": {"idx": "#4A90E2", "bg": "#EBF5FB"},
    "야식": {"idx": "#673AB7", "bg": "#F4ECF7"}
}

menu_data = {
    "조식": ["제철미나리쭈꾸미연포탕", "매운두부찜", "흰쌀밥", "모둠장아찌", "누룽지"],
    "간편식": ["고로케양배추샌드위치", "삶은계란", "플레인요거트"],
    "중식": ["버섯불고기", "우엉채레몬튀김", "수수기장밥", "얼큰어묵탕", "수정과"],
    "석식": ["양배추멘치카츠", "가쓰오장국", "시저드레싱샐러드", "열무김치"],
    "야식": ["소고기미역죽", "돈육장조림", "깍두기", "블루베리요플레"]
}

# 2. 세션 관리 및 쿼리 파라미터를 이용한 상태 변경
# 버튼 클릭 시 URL 파라미터를 변경하여 페이지를 갱신하는 트릭을 씁니다.
query_params = st.query_params
if "meal" in query_params:
    st.session_state.active_meal = query_params["meal"]
elif 'active_meal' not in st.session_state:
    st.session_state.active_meal = "중식"

current_sel = st.session_state.active_meal
bold_c = color_theme[current_sel]["idx"]
soft_bg = color_theme[current_sel]["bg"]

# 3. 메인 UI (카드 디자인)
st.markdown(f"""
<style>
    .main .block-container {{
        max-width: 500px !important;
        padding-right: 70px !important;
        margin: 0 auto !important;
    }}
    .main-card {{
        background-color: {soft_bg} !important;
        border: 2.5px solid {bold_c} !important;
        border-radius: 20px !important;
        padding: 30px 15px !important;
        text-align: center;
        min-height: 380px;
    }}
</style>
<div class="main-card">
    <h2 style="color: {bold_c};">{current_sel}</h2>
    <hr style="border: 0.5px solid {bold_c}; opacity: 0.2;">
    <p style="font-size: 24px; font-weight: bold; color: #333; margin-top: 20px;">🍲 {menu_data[current_sel][0]}</p>
    <p style="font-size: 16px; color: #555; line-height: 1.8;">{' / '.join(menu_data[current_sel][1:])}</p>
</div>
""", unsafe_allow_html=True)

# 4. HTML/JS 플로팅 바 (절대 밀리지 않는 레이어)
# 이 부분은 Streamlit 레이아웃의 영향을 받지 않고 브라우저 우측에 고정됩니다.
html_code = f"""
<div id="floating-nav" style="
    position: fixed;
    right: 0px;
    top: 50%;
    transform: translateY(-50%);
    display: flex;
    flex-direction: column;
    z-index: 99999;
">
"""

for meal in ["조식", "간편식", "중식", "석식", "야식"]:
    m_color = color_theme[meal]["idx"]
    is_active = (meal == current_sel)
    opacity = 1.0 if is_active else 0.4
    
    # 클릭 시 부모창(Streamlit)의 URL을 변경하여 리로드 시킴
    html_code += f"""
    <button onclick="parent.window.location.search = '?meal={meal}'" style="
        writing-mode: vertical-rl;
        text-orientation: upright;
        height: 80px;
        width: 48px;
        background-color: {m_color};
        color: white;
        border: none;
        border-radius: 12px 0 0 12px;
        margin-bottom: 2px;
        font-weight: bold;
        opacity: {opacity};
        cursor: pointer;
        box-shadow: -2px 2px 5px rgba(0,0,0,0.2);
    ">{meal}</button>
    """

html_code += "</div>"

# 고정된 높이의 컴포넌트로 플로팅 바 삽입
components.html(html_code, height=500)
