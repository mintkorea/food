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

# 3. 컬러 구성 (가이드북 컨셉)
color_map = {
    "조식": ("#E95444", "#FFF5F4"),
    "간편식": ("#F1A33B", "#FFF9F0"),
    "중식": ("#8BC34A", "#F9FBF2"),
    "석식": ("#4A90E2", "#F0F7FF"),
    "야식": ("#673AB7", "#F7F2FF")
}

if 'selected_meal' not in st.session_state:
    st.session_state.selected_meal = "중식"

bold_c, soft_c = color_map[st.session_state.selected_meal]

# 4. [핵심] 초밀착 레이아웃 CSS
st.markdown(f"""
    <style>
    /* 기본 여백 완전 제거 */
    .block-container {{ padding: 10px !important; }}
    
    /* 카드와 인덱스를 감싸는 컨테이너 간격 제거 */
    div[data-testid="column"] {{
        width: float !important;
        flex: unset !important;
        min-width: unset !important;
    }}
    
    /* 메인 카드 디자인: 높이 고정 및 우측 모서리 직각 */
    .compact-card {{
        background-color: {soft_c};
        height: 350px;
        width: 100%;
        border: 2px solid {bold_c};
        border-radius: 15px 0 0 15px;
        padding: 15px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-align: center;
    }}

    /* 버튼 스타일: 카드 높이(350px) / 5개 = 70px */
    .stButton button {{
        width: 48px !important;
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
        box-shadow: none !important;
        display: block !important;
    }}

    /* 버튼 사이의 미세 여백 제거 */
    div[data-testid="stVerticalBlock"] > div {{
        gap: 0rem !important;
    }}
    </style>
""", unsafe_allow_html=True)

# 5. 상단 구성
st.markdown('<h3 style="margin-bottom:5px; font-size:1.2rem;">🍴 오늘의 식사</h3>', unsafe_allow_html=True)
selected_date = st.selectbox("날짜", list(menu_data.keys()), label_visibility="collapsed")

# 6. 컬럼 레이아웃 (gap="0")
# 모바일에서 밀리지 않도록 비중을 아주 타이트하게 설정
col_main, col_idx = st.columns([0.83, 0.17])

with col_main:
    menu = menu_data[selected_date].get(st.session_state.selected_meal, ["정보 없음"])
    st.markdown(f"""
        <div class="compact-card">
            <h2 style="color: {bold_c}; font-size: 18px; margin: 0;">{st.session_state.selected_meal}</h2>
            <div style="height: 1px; background-color: {bold_c}; opacity: 0.2; margin: 10px 0;"></div>
            <p style="font-size: 20px; font-weight: bold; color: #333; margin-bottom: 5px;">🍲 {menu[0]}</p>
            <p style="font-size: 14px; color: #666; line-height: 1.5;">{' / '.join(menu[1:])}</p>
        </div>
    """, unsafe_allow_html=True)

with col_idx:
    # 5개 버튼 순차 배치
    for label in ["조식", "간편식", "중식", "석식", "야식"]:
        b_color, _ = color_map[label]
        # 개별 버튼 컬러 적용
        st.markdown(f"""<style>button[key="tab_{label}"] {{ background-color: {b_color} !important; }}</style>""", unsafe_allow_html=True)
        
        if st.button(label, key=f"tab_{label}"):
            st.session_state.selected_meal = label
            st.rerun()
