import streamlit as st
from datetime import datetime

# 1. 주간 식단 전체 데이터 (3/16 ~ 3/22)
menu_data = {
    "2026-03-16(월)": {
        "조식": ["두유스프", "단호박에그마요샌드", "바게트/잡곡식빵", "맛살마요범벅", "누룽지"],
        "간편식": ["운영 없음"],
        "중식": ["차돌해물짬뽕밥", "김말이튀김", "흑미밥", "그린샐러드", "매실주스"],
        "석식": ["어항가지돈육덮밥", "사골파국", "감자채햄볶음", "망고드레싱샐러드"],
        "야식": ["날치알볶음밥", "후랑크소시지", "참깨드레싱샐러드", "요구르트"]
    },
    "2026-03-17(화)": {
        "조식": ["제철미나리쭈꾸미연포탕", "매운두부찜", "흰쌀밥", "모둠장아찌", "누룽지"],
        "간편식": ["고로케양배추샌드위치", "삶은계란", "플레인요거트"],
        "중식": ["버섯불고기", "우엉채레몬튀김", "수수기장밥", "얼큰어묵탕", "수정과"],
        "석식": ["양배추멘치카츠", "가쓰오장국", "시저드레싱샐러드", "열무김치"],
        "야식": ["소고기미역죽", "돈육장조림", "깍두기", "블루베리요플레"]
    },
    "2026-03-18(수)": {
        "조식": ["감자수제비", "돈채가지볶음", "흰쌀밥", "양념고추지", "누룽지"],
        "간편식": ["닭가슴살샐러드", "바나나"],
        "중식": ["뼈없는닭볶음탕", "혼합잡곡밥", "유부겨자냉채", "복분자주스"],
        "석식": ["하이디라오마라탕", "탕수육", "짜사이무침", "열무김치"],
        "야식": ["돈사태떡찜", "유채된장국", "멸치볶음", "요구르트"]
    },
    "2026-03-19(목)": {
        "조식": ["시래기장터국밥", "모둠땡전", "치커리유자무침", "포도주스"],
        "간편식": ["어니언치즈베이글", "말린망고주스"],
        "중식": ["통등심돈까스", "비빔막국수", "미역국", "레몬아이스티"],
        "석식": ["돼지목살필라프", "우동장국", "삼색푸실리볶음", "포기김치"],
        "야식": ["함박스테이크", "콩가루배춧국", "실곤약초무침", "망고주스"]
    },
    "2026-03-20(금)": {
        "조식": ["김치해장죽", "고구마파이", "오리엔탈샐러드", "누룽지"],
        "간편식": ["운영 없음"],
        "중식": ["뿌리채소영양밥", "언양식바싹불고기", "아욱된장국", "식혜"],
        "석식": ["셀프쭈불비빔밥", "시금치된장국", "콩나물무침", "열무김치"],
        "야식": ["치킨토마토샌드위치", "피치우롱티"]
    },
    "2026-03-21(토)": {
        "조식": ["잡곡식빵/모닝롤", "양송이스프", "참깨드레싱샐러드"],
        "간편식": ["운영 없음"],
        "중식": ["순살닭볶음", "맑은못국", "원두커피"],
        "석식": ["순두부찌개", "군만두", "얼갈이나물", "깍두기"],
        "야식": ["고추장돈육볶음", "어묵국", "양배추찜", "쥬시쿨"]
    },
    "2026-03-22(일)": {
        "조식": ["잡곡식빵/모닝롤", "옥수수스프", "오렌지드레싱샐러드"],
        "간편식": ["운영 없음"],
        "중식": ["뚝배기들깨영양탕", "메추리알조림", "원두커피"],
        "석식": ["비프하이라이스", "통새우튀김", "미소시루"],
        "야식": ["로제찜닭", "우동국", "요구르트"]
    }
}

# 2. 색상 테마 (인덱스: 선명 / 카드: 파스텔)
color_theme = {
    "조식": {"idx": "#E95444", "bg": "#FFF5F4"},
    "간편식": {"idx": "#F1A33B", "bg": "#FFF9F0"},
    "중식": {"idx": "#8BC34A", "bg": "#F8FCF3"},
    "석식": {"idx": "#4A90E2", "bg": "#F4F9FF"},
    "야식": {"idx": "#673AB7", "bg": "#F9F6FF"}
}

if 'meal' not in st.session_state:
    st.session_state.meal = "중식"

# 3. CSS: 인덱스 고정 및 카드 스타일
bold_c = color_theme[st.session_state.meal]["idx"]
soft_bg = color_theme[st.session_state.meal]["bg"]

st.markdown(f"""
<style>
    .stApp {{ background-color: white; }}
    .main-card {{
        background-color: {soft_bg};
        border: 2.5px solid {bold_c};
        border-radius: 20px 0 0 20px;
        padding: 40px 20px;
        margin-right: 55px;
        min-height: 400px;
        text-align: center;
        box-shadow: -4px 4px 15px rgba(0,0,0,0.06);
        display: flex; flex-direction: column; justify-content: center;
    }}
    /* 우측 고정 인덱스 */
    .fixed-indices {{
        position: fixed;
        right: 0px;
        top: 180px;
        display: flex;
        flex-direction: column;
        gap: 3px;
        z-index: 1000;
    }}
</style>
""", unsafe_allow_html=True)

# 4. UI 렌더링
st.title("🗂️ 시설관리 스마트 식단")
day = st.selectbox("날짜", list(menu_data.keys()), index=1, label_visibility="collapsed")

# 레이아웃 구성
col_card, col_dummy = st.columns([8.2, 1.8])

with col_card:
    menu = menu_data[day].get(st.session_state.meal, ["정보 없음"])
    st.markdown(f"""
        <div class="main-card">
            <h2 style="color: {bold_c}; margin-bottom: 5px;">{st.session_state.meal}</h2>
            <hr style="border: 0; height: 1.5px; background: {bold_c}; opacity: 0.2; margin: 15px 0;">
            <p style="font-size: 26px; font-weight: bold; color: #333; margin-bottom: 12px;">🍲 {menu[0]}</p>
            <p style="font-size: 17px; color: #555; line-height: 1.8;">{' / '.join(menu[1:])}</p>
        </div>
    """, unsafe_allow_html=True)

# 인덱스 버튼 생성
st.markdown('<div class="fixed-indices">', unsafe_allow_html=True)
for m in ["조식", "간편식", "중식", "석식", "야식"]:
    m_color = color_theme[m]["idx"]
    st.markdown(f"""
        <style>
        div[data-testid="stVerticalBlock"] button[key="btn_{m}"] {{
            background-color: {m_color} !important;
            color: white !important;
            writing-mode: vertical-rl !important;
            text-orientation: upright !important;
            height: 85px !important;
            width: 48px !important;
            border-radius: 12px 0 0 12px !important;
            border: none !important;
            font-weight: bold !important;
            font-size: 14px !important;
            padding: 0 !important;
        }}
        </style>
    """, unsafe_allow_html=True)
    if st.button(m, key=f"btn_{m}"):
        st.session_state.meal = m
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
