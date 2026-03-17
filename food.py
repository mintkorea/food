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

# 3. 컬러 정의
color_map = {
    "조식": ("#E95444", "#FFF5F4"), "간편식": ("#F1A33B", "#FFF9F0"),
    "중식": ("#8BC34A", "#F9FBF2"), "석식": ("#4A90E2", "#F0F7FF"), "야식": ("#673AB7", "#F7F2FF")
}
bold_c, soft_c = color_map[st.session_state.selected_meal]

# 4. 강제 고정 CSS
st.markdown(f"""
    <style>
    /* 전체 여백 제거 */
    .block-container {{ padding: 10px !important; max-width: 100% !important; }}
    
    /* 카드 디자인: 우측 모서리 직각 */
    .fixed-card {{
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

    /* 버튼 스타일: 350px / 5개 = 70px */
    .stButton button {{
        width: 50px !important;
        height: 70px !important;
        writing-mode: vertical-rl !important;
        text-orientation: upright !important;
        border-radius: 0 10px 10px 0 !important;
        border: none !important;
        color: white !important;
        font-weight: bold !important;
        margin: 0 !important;
        padding: 0 !important;
        font-size: 13px !important;
        line-height: 1 !important;
    }}

    /* 인덱스 버튼들이 담긴 세로 블록의 간격 완전 제거 */
    [data-testid="stVerticalBlock"] {{ gap: 0rem !important; }}
    
    /* 모바일에서 컬럼이 아래로 밀리는 현상 방지 */
    [data-testid="column"] {{
        width: fit-content !important;
        flex: unset !important;
    }}
    </style>
""", unsafe_allow_html=True)

# 5. 상단 구성
st.markdown('<div style="font-size:1.2rem; font-weight:bold; margin-bottom:5px;">🍴 오늘의 식사</div>', unsafe_allow_html=True)
selected_date = st.selectbox("날짜", list(menu_data.keys()), label_visibility="collapsed")

# 6. [핵심] 테이블 구조를 흉내낸 고정 레이아웃
# 간격을 0으로 설정하여 물리적으로 결합
col_card, col_btn = st.columns([0.83, 0.17], gap="small")

with col_card:
    menu = menu_data[selected_date].get(st.session_state.selected_meal, ["정보 없음"])
    st.markdown(f"""
        <div class="fixed-card">
            <h2 style="color: {bold_c}; font-size: 20px; margin: 0;">{st.session_state.selected_meal}</h2>
            <div style="height: 1.5px; background-color: {bold_c}; opacity: 0.2; margin: 12px 0;"></div>
            <p style="font-size: 22px; font-weight: bold; color: #333; margin-bottom: 10px;">{menu[0]}</p>
            <p style="font-size: 15px; color: #666; line-height: 1.6;">{' / '.join(menu[1:])}</p>
        </div>
    """, unsafe_allow_html=True)

with col_btn:
    # 5개의 버튼을 빈틈없이 수직 배치
    for label in ["조식", "간편식", "중식", "석식", "야식"]:
        b_color, _ = color_map[label]
        # 개별 버튼 색상 적용
        st.markdown(f"""<style>button[key="tab_{label}"] {{ background-color: {b_color} !important; }}</style>""", unsafe_allow_html=True)
        if st.button(label, key=f"tab_{label}"):
            st.session_state.selected_meal = label
            st.rerun()
