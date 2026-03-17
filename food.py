import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="오늘의 식사", layout="centered")

# 2. 데이터
menu_data = {
    "2026-03-17(화)": {
        "조식": ["연포탕", "매운두부찜"], "간편식": ["샌드위치", "요거트"],
        "중식": ["버섯불고기", "우엉채레몬튀김", "수수기장밥", "얼큰어묵탕", "수정과"],
        "석식": ["멘치카츠", "가쓰오장국"], "야식": ["소고기미역죽"]
    }
}

if 'selected_meal' not in st.session_state:
    st.session_state.selected_meal = "중식"

# 3. 컬러 및 스타일 정의
color_map = {
    "조식": ("#E95444", "#FFF5F4"), "간편식": ("#F1A33B", "#FFF9F0"),
    "중식": ("#8BC34A", "#F9FBF2"), "석식": ("#4A90E2", "#F0F7FF"), "야식": ("#673AB7", "#F7F2FF")
}
bold_c, soft_c = color_map[st.session_state.selected_meal]

# 4. 모바일 대응 핵심 CSS
st.markdown(f"""
    <style>
    /* 전체 패딩 제거 */
    .block-container {{ padding: 10px !important; }}
    
    /* 카드와 버튼을 감싸는 컨테이너의 간격 강제 제거 */
    [data-testid="column"] {{
        width: calc(var(--content-width) * 1) !important;
        flex-shrink: 0 !important;
        min-width: unset !important;
    }}
    
    /* 메인 카드 디자인: 너비 80% 고정 */
    .compact-card {{
        background-color: {soft_c};
        height: 320px;
        border: 2px solid {bold_c};
        border-radius: 12px 0 0 12px;
        padding: 15px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-align: center;
        box-sizing: border-box;
    }}

    /* 버튼 컨테이너: 너비 20% 고정 및 간격 제거 */
    div[data-testid="stVerticalBlock"] {{ gap: 0rem !important; }}

    /* 버튼 개별 스타일: 높이를 카드와 정밀하게 일치 */
    .stButton button {{
        width: 100% !important;
        height: 64px !important; /* 320px / 5개 = 64px */
        writing-mode: vertical-rl !important;
        text-orientation: upright !important;
        border-radius: 0 10px 10px 0 !important;
        border: none !important;
        color: white !important;
        font-weight: bold !important;
        padding: 0 !important;
        margin: 0 !important;
        font-size: 12px !important;
        line-height: 1 !important;
    }}
    </style>
""", unsafe_allow_html=True)

# 5. 상단 구성
st.markdown('<div style="font-size:1.1rem; font-weight:bold; margin-bottom:5px;">🍴 오늘의 식사</div>', unsafe_allow_html=True)
selected_date = st.selectbox("날짜", list(menu_data.keys()), label_visibility="collapsed")

# 6. 컬럼 배치 (8:2 비율 강제 고정)
col_card, col_btn = st.columns([0.8, 0.2], gap="small")

with col_card:
    menu = menu_data[selected_date].get(st.session_state.selected_meal, ["정보 없음"])
    st.markdown(f"""
        <div class="compact-card">
            <h2 style="color: {bold_c}; font-size: 18px; margin: 0;">{st.session_state.selected_meal}</h2>
            <div style="height: 1px; background-color: {bold_c}; opacity: 0.2; margin: 10px 0;"></div>
            <p style="font-size: 18px; font-weight: bold; color: #333; margin-bottom: 5px;">{menu[0]}</p>
            <p style="font-size: 13px; color: #666; line-height: 1.5;">{' / '.join(menu[1:])}</p>
        </div>
    """, unsafe_allow_html=True)

with col_btn:
    for label in ["조식", "간편식", "중식", "석식", "야식"]:
        b_color, _ = color_map[label]
        # 각 버튼 컬러 주입
        st.markdown(f"""<style>button[key="tab_{label}"] {{ background-color: {b_color} !important; }}</style>""", unsafe_allow_html=True)
        if st.button(label, key=f"tab_{label}"):
            st.session_state.selected_meal = label
            st.rerun()
