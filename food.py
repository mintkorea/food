import streamlit as st
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="오늘의 식사", layout="centered")

# 2. 데이터
menu_data = {
    "2026-03-17(화)": {
        "조식": ["제철미나리쭈꾸미연포탕", "매운두부찜", "모둠장아찌", "누룽지"],
        "간편식": ["고로케양배추샌드위치", "삶은계란", "플레인요거트"],
        "중식": ["버섯불고기", "우엉채레몬튀김", "수수기장밥", "얼큰어묵탕", "수정과"],
        "석식": ["양배추멘치카츠", "가쓰오장국", "시저드레싱샐러드", "열무김치"],
        "야식": ["소고기미역죽", "돈육장조림", "블루베리요플레"]
    }
}

if 'selected_meal' not in st.session_state:
    st.session_state.selected_meal = "중식"

# 3. 컬러 구성
color_map = {
    "조식": ("#E95444", "#FFF5F4"), "간편식": ("#F1A33B", "#FFF9F0"),
    "중식": ("#8BC34A", "#F9FBF2"), "석식": ("#4A90E2", "#F0F7FF"), "야식": ("#673AB7", "#F7F2FF")
}
bold_c, soft_c = color_map[st.session_state.selected_meal]

# 4. 일체형 레이아웃 CSS
st.markdown(f"""
    <style>
    /* 기본 여백 및 배경 */
    .block-container {{ padding: 10px !important; }}
    
    /* 카드와 버튼을 감싸는 전체 부모 박스 */
    .guide-container {{
        display: flex;
        align-items: flex-start;
        justify-content: center;
        width: 100%;
        margin-top: 5px;
    }}

    /* 메인 카드: 너비를 80%로 고정 */
    .main-card-frame {{
        flex: 0 0 80%;
        background-color: {soft_c};
        height: 350px;
        border: 2px solid {bold_c};
        border-radius: 15px 0 0 15px;
        padding: 20px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-align: center;
        box-sizing: border-box;
    }}

    /* 인덱스 버튼들이 들어갈 공간: 너비를 20%로 고정 */
    .index-bar {{
        flex: 0 0 20%;
        display: flex;
        flex-direction: column;
        height: 350px;
    }}

    /* 버튼 스타일 강제 교정 */
    .stButton button {{
        width: 100% !important;
        height: 70px !important;
        writing-mode: vertical-rl !important;
        text-orientation: upright !important;
        border-radius: 0 10px 10px 0 !important;
        border: none !important;
        color: white !important;
        font-weight: bold !important;
        padding: 0 !important;
        margin: 0 !important;
        font-size: 13px !important;
        line-height: 1 !important;
        box-shadow: none !important;
    }}
    
    /* 버튼 간의 미세한 틈새 제거 */
    div[data-testid="column"] {{ gap: 0 !important; }}
    div[data-testid="stVerticalBlock"] {{ gap: 0 !important; }}
    </style>
""", unsafe_allow_html=True)

# 5. 상단 구성
st.markdown('<h3 style="font-size:1.2rem; margin-bottom:5px;">🍴 오늘의 식사</h3>', unsafe_allow_html=True)
selected_date = st.selectbox("날짜", list(menu_data.keys()), label_visibility="collapsed")

# 6. [핵심] 억지로 붙이기 레이아웃
# 좌측(카드)와 우측(인덱스)을 하나의 컬럼 셋으로 묶되 간격을 0으로 설정
col_left, col_right = st.columns([0.8, 0.2], gap="small")

with col_left:
    menu = menu_data[selected_date].get(st.session_state.selected_meal, ["정보 없음"])
    st.markdown(f"""
        <div class="main-card-frame">
            <h2 style="color: {bold_c}; font-size: 18px; margin: 0;">{st.session_state.selected_meal}</h2>
            <div style="height: 1px; background-color: {bold_c}; opacity: 0.2; margin: 12px 0;"></div>
            <p style="font-size: 22px; font-weight: bold; color: #333; margin-bottom: 8px;">{menu[0]}</p>
            <p style="font-size: 14px; color: #666; line-height: 1.6;">{' / '.join(menu[1:])}</p>
        </div>
    """, unsafe_allow_html=True)

with col_right:
    # 5개의 버튼을 빈틈없이 수직 배치
    for label in ["조식", "간편식", "중식", "석식", "야식"]:
        b_color, _ = color_map[label]
        # 각 버튼 컬러를 해당 루프에서 즉시 주입
        st.markdown(f"""<style>button[key="tab_{label}"] {{ background-color: {b_color} !important; }}</style>""", unsafe_allow_html=True)
        if st.button(label, key=f"tab_{label}"):
            st.session_state.selected_meal = label
            st.rerun()
