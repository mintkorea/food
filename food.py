import streamlit as st
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="식단 가이드", layout="centered")

# 2. 이번 주 전체 데이터 (이미지 분석 반영)
menu_data = {
    "2026-03-16(월)": {"조식": ["두유스프", "단호박샌드"], "간편식": ["없음"], "중식": ["차돌짬뽕밥"], "석식": ["어항가지덮밥"], "야식": ["날치알볶음밥"]},
    "2026-03-17(화)": {
        "조식": ["제철미나리쭈꾸미연포탕", "매운두부찜", "모둠장아찌", "누룽지"],
        "간편식": ["고로케양배추샌드위치", "삶은계란", "플레인요거트"],
        "중식": ["버섯불고기", "우엉채레몬튀김", "수수기장밥", "얼큰어묵탕", "수정과"],
        "석식": ["양배추멘치카츠", "가쓰오장국", "시저드레싱샐러드", "열무김치"],
        "야식": ["소고기미역죽", "돈육장조림", "블루베리요플레"]
    },
    "2026-03-18(수)": {"조식": ["감자수제비"], "간편식": ["닭가슴살샐러드"], "중식": ["뼈없는닭볶음탕"], "석식": ["마라탕"], "야식": ["돈사태떡찜"]}
}

# 3. 컬러 테마 (인덱스: 선명 / 카드: 부드러움)
color_map = {
    "조식": ("#E95444", "#FFF5F4"), "간편식": ("#F1A33B", "#FFF9F0"),
    "중식": ("#8BC34A", "#F9FBF2"), "석식": ("#4A90E2", "#F0F7FF"), "야식": ("#673AB7", "#F7F2FF")
}

# 4. 세션 상태 및 현재 시간 자동 감지
if 'selected_meal' not in st.session_state:
    curr_hour = datetime.now().hour
    if curr_hour < 9: st.session_state.selected_meal = "조식"
    elif 11 <= curr_hour < 14: st.session_state.selected_meal = "중식"
    else: st.session_state.selected_meal = "석식"

bold_c, soft_c = color_map[st.session_state.selected_meal]

# 5. 핵심: 우측 고정 인덱스 프레임 CSS
st.markdown(f"""
    <style>
    /* 전체 레이아웃 조정 */
    .block-container {{ padding: 1rem 4rem 1rem 1rem !important; }}
    
    /* 메인 카드 프레임 */
    .main-card-frame {{
        background-color: {soft_c};
        height: 520px;
        border: 2.5px solid {bold_c};
        border-radius: 20px 0 0 20px;
        padding: 25px;
        text-align: center;
        display: flex;
        flex-direction: column;
        justify-content: center;
        box-shadow: -5px 5px 15px rgba(0,0,0,0.05);
    }}

    /* 우측 고정 인덱스 탭 프레임 */
    .fixed-index-container {{
        position: fixed;
        right: 10px;
        top: 150px;
        display: flex;
        flex-direction: column;
        gap: 5px;
        z-index: 1000;
    }}
    
    .index-tab {{
        width: 45px;
        height: 80px;
        color: white;
        font-weight: bold;
        display: flex;
        align-items: center;
        justify-content: center;
        writing-mode: vertical-rl;
        text-orientation: upright;
        border-radius: 0 10px 10px 0;
        font-size: 14px;
        cursor: pointer;
        border: none;
    }}
    </style>
""", unsafe_allow_html=True)

# 6. 화면 구성
st.title("🗂️ 시설관리 식단 가이드")
selected_date = st.selectbox("날짜", list(menu_data.keys()), index=1, label_visibility="collapsed")

# 메인 카드 노출
menu = menu_data[selected_date].get(st.session_state.selected_meal, ["정보 없음"])
st.markdown(f"""
    <div class="main-card-frame">
        <h2 style="color: {bold_c};">{st.session_state.selected_meal}</h2>
        <hr style="border: 0.5px solid {bold_c}; opacity: 0.2; margin: 15px 0;">
        <p style="font-size: 24px; font-weight: bold; color: #333;">🍲 {menu[0]}</p>
        <p style="font-size: 17px; color: #666; line-height: 1.8;">{' / '.join(menu[1:])}</p>
    </div>
""", unsafe_allow_html=True)

# 7. 항상 열려 있는 인덱스 탭 (버튼 로직)
# Streamlit 버튼은 CSS로 위치를 고정하기 까다로우므로, 
# columns를 매우 좁게 잡아 우측에 배치하는 방식으로 구현합니다.
with st.container():
    col_empty, col_index = st.columns([8.5, 1.5])
    with col_index:
        for label in ["조식", "간편식", "중식", "석식", "야식"]:
            b_color, _ = color_map[label]
            if st.button(label, key=f"fixed_{label}"):
                st.session_state.selected_meal = label
                st.rerun()
            
            # 인덱스 버튼별 선명한 색상 강제 적용
            st.markdown(f"""
                <style>
                div[data-testid="stVerticalBlock"] > div:nth-child({["조식", "간편식", "중식", "석식", "야식"].index(label)+1}) button {{
                    background-color: {b_color} !important;
                    height: 85px !important;
                    width: 45px !important;
                    writing-mode: vertical-rl !important;
                    text-orientation: upright !important;
                    color: white !important;
                    border-radius: 0 10px 10px 0 !important;
                    padding: 0 !important;
                    margin-left: -15px !important;
                }}
                </style>
            """, unsafe_allow_html=True)

st.caption("💡 우측 인덱스 탭은 항상 열려 있습니다.")
