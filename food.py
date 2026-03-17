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

# 3. 컬러 구성
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

# 4. 레이아웃 고정 CSS
st.markdown(f"""
    <style>
    /* 전체 여백 및 배경 */
    .stApp {{ background-color: #f8f9fa; }}
    .block-container {{ padding-top: 10px !important; padding-bottom: 0px !important; }}
    
    /* 헤더 */
    .header-box {{ font-size: 1.2rem; font-weight: bold; margin-bottom: 5px; color: #333; }}

    /* 전체 프레임 컨테이너 */
    .flex-container {{
        display: flex;
        align-items: flex-start;
        justify-content: center;
        width: 100%;
        margin-top: 5px;
    }}

    /* 메인 카드 디자인 */
    .main-card {{
        flex: 1;
        background-color: {soft_c};
        height: 340px;
        border: 2.5px solid {bold_c};
        border-radius: 15px 0 0 15px;
        padding: 20px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-align: center;
        z-index: 1;
    }}

    /* 인덱스 탭 영역 (카드 바로 옆에 붙음) */
    .index-area {{
        display: flex;
        flex-direction: column;
        width: 50px;
    }}

    /* Streamlit 버튼 스타일 강제 변경 */
    .stButton > button {{
        width: 50px !important;
        height: 68px !important;
        writing-mode: vertical-rl !important;
        text-orientation: upright !important;
        border-radius: 0 10px 10px 0 !important;
        border: none !important;
        color: white !important;
        font-weight: bold !important;
        margin-bottom: 0px !important; /* 틈새 제거 */
        font-size: 13px !important;
        padding: 0 !important;
        line-height: 1 !important;
    }}
    </style>
""", unsafe_allow_html=True)

# 5. 화면 구성
st.markdown('<div class="header-box">🍴 오늘의 식사</div>', unsafe_allow_html=True)
selected_date = st.selectbox("날짜", list(menu_data.keys()), label_visibility="collapsed")

# 6. 카드와 인덱스를 감싸는 실제 레이아웃
# columns 비중을 고정하여 모바일에서 밀림 방지
col_main, col_idx = st.columns([0.82, 0.18])

with col_main:
    menu = menu_data[selected_date].get(st.session_state.selected_meal, ["정보 없음"])
    st.markdown(f"""
        <div class="main-card">
            <h2 style="color: {bold_c}; font-size: 20px; margin: 0;">{st.session_state.selected_meal}</h2>
            <div style="height: 1.5px; background-color: {bold_c}; opacity: 0.2; margin: 12px 0;"></div>
            <p style="font-size: 20px; font-weight: bold; color: #333; margin-bottom: 10px;">{menu[0]}</p>
            <p style="font-size: 14px; color: #666; line-height: 1.6;">{' / '.join(menu[1:])}</p>
        </div>
    """, unsafe_allow_html=True)

with col_idx:
    # 탭 간의 틈새를 줄이기 위해 루프 안에서 버튼 배치
    for label in ["조식", "간편식", "중식", "석식", "야식"]:
        b_color, _ = color_map[label]
        # 개별 버튼 색상 적용
        st.markdown(f"""<style>button[key="tab_{label}"] {{ background-color: {b_color} !important; }}</style>""", unsafe_allow_html=True)
        
        if st.button(label, key=f"tab_{label}"):
            st.session_state.selected_meal = label
            st.rerun()
