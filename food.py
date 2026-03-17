import streamlit as st
from datetime import datetime

# 1. 페이지 설정 (모바일 브라우저 최적화)
st.set_page_config(page_title="주간 식단 가이드", layout="centered")

# 2. 일주일 전체 데이터 (이미지 분석 결과 반영)
menu_data = {
    "2026-03-16(월)": {
        "조식": ["두유스프", "단호박에그마요샌드", "바게트/잡곡식빵", "맛살마요범벅", "누룽지"],
        "간편식": ["운영 없음"],
        "중식": ["차돌해물짬뽕밥", "김말이튀김", "흑미밥", "그린샐러드", "매실주스"],
        "석식": ["어항가지돈육덮밥", "사골파국", "감자채햄볶음", "망고드레싱샐러드"],
        "야식": ["날치알볶음밥", "후랑크소시지", "참깨드레싱샐러드", "요구르트"]
    },
    "2026-03-17(화)": {
        "조식": ["제철미나리쭈꾸미연포탕", "매운두부찜", "모둠장아찌", "깍두기", "누룽지"],
        "간편식": ["고로케양배추샌드위치", "삶은계란", "플레인요거트"],
        "중식": ["버섯불고기", "우엉채레몬튀김", "수수기장밥", "얼큰어묵탕", "수정과"],
        "석식": ["양배추멘치카츠", "가쓰오장국", "시저드레싱샐러드", "열무김치"],
        "야식": ["소고기미역죽", "돈육장조림", "깍두기", "블루베리요플레"]
    },
    "2026-03-18(수)": {
        "조식": ["감자수제비", "흰쌀밥", "돈채가지볶음", "양념고추지", "누룽지"],
        "간편식": ["닭가슴살샐러드", "바나나"],
        "중식": ["뼈없는닭볶음탕", "혼합잡곡밥", "유부겨자냉채", "복분자주스"],
        "석식": ["하이디라오마라탕", "탕수육", "짜사이무침", "열무김치"],
        "야식": ["돈사태떡찜", "유채된장국", "멸치볶음", "요구르트"]
    },
    "2026-03-19(목)": {
        "조식": ["시래기장터국밥", "모둠땡전", "치커리유자무침", "포도쥬스"],
        "간편식": ["어니언치즈베이글샌드위치", "말린망고쥬스"],
        "중식": ["통등심돈까스", "비빔막국수", "미역국", "레몬아이스티"],
        "석식": ["돼지목살필라프", "우동장국", "삼색푸실리볶음", "포기김치"],
        "야식": ["함박스테이크", "콩가루배춧국", "실곤약초무침", "망고주스"]
    },
    "2026-03-20(금)": {
        "조식": ["김치해장죽", "고구마파이", "오리엔탈샐러드", "누룽지"],
        "간편식": ["운영 없음"],
        "중식": ["뿌리채소영양밥", "언양식바싹불고기", "도토리묵무침", "식혜"],
        "석식": ["셀프쭈불비빔밥", "시금치된장국", "콩나물무침", "열무김치"],
        "야식": ["치킨토마토샌드위치", "피치우롱티"]
    },
    "2026-03-21(토)": {
        "조식": ["잡곡식빵&모닝롤", "양송이스프", "참깨드레싱샐러드", "누룽지"],
        "간편식": ["운영 없음"],
        "중식": ["순살닭볶음", "맑은못국", "멕시칸마요범벅", "원두커피"],
        "석식": ["순두부찌개", "군만두", "얼갈이나물", "깍두기"],
        "야식": ["고추장돈육볶음", "어묵국", "마카로니샐러드", "쥬시쿨"]
    },
    "2026-03-22(일)": {
        "조식": ["잡곡식빵&모닝롤", "옥수수스프", "오렌지드레싱샐러드", "누룽지"],
        "간편식": ["운영 없음"],
        "중식": ["뚝배기들깨영양탕", "메추리알조림", "키위드레싱샐러드", "원두커피"],
        "석식": ["비프하이라이스", "통새우튀김", "야채쫄면무침", "미소시루"],
        "야식": ["로제찜닭", "우동국", "요거트샐러드", "요구르트"]
    }
}

# 3. 컬러 테마 정의 (인덱스: 선명하게, 카드: 부드럽게)
color_map = {
    "조식": ("#E95444", "#FFF5F4"),
    "간편식": ("#F1A33B", "#FFF9F0"),
    "중식": ("#8BC34A", "#F9FBF2"),
    "석식": ("#4A90E2", "#F0F7FF"),
    "야식": ("#673AB7", "#F7F2FF")
}

# 4. 현재 시간 기반 초기값 설정
if 'selected_meal' not in st.session_state:
    now = datetime.now()
    curr_hour = now.hour
    if curr_hour < 9: st.session_state.selected_meal = "조식"
    elif 9 <= curr_hour < 11: st.session_state.selected_meal = "간편식"
    elif 11 <= curr_hour < 14: st.session_state.selected_meal = "중식"
    elif 14 <= curr_hour < 19: st.session_state.selected_meal = "석식"
    else: st.session_state.selected_meal = "야식"

# 5. CSS 적용 (인덱스 고정 및 프레임 분할)
bold_c, soft_c = color_map[st.session_state.selected_meal]

st.markdown(f"""
    <style>
    .stApp {{ background-color: #FFFFFF; }}
    .block-container {{ padding: 0.5rem; }}
    
    /* 인덱스 탭 스타일 */
    .stButton > button {{
        height: 75px;
        width: 48px;
        writing-mode: vertical-rl;
        text-orientation: upright;
        border: none;
        color: white !important;
        border-radius: 0px 10px 10px 0px;
        margin-bottom: 3px;
        font-weight: bold;
        font-size: 14px;
        transition: 0.2s;
    }}
    
    /* 메인 상세 식단 프레임 (카드) */
    .main-card {{
        background-color: {soft_c};
        height: 480px;
        border-radius: 20px 0px 0px 20px;
        border: 2px solid {bold_c};
        padding: 20px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-align: center;
        box-shadow: -5px 5px 15px rgba(0,0,0,0.05);
    }}
    </style>
""", unsafe_allow_html=True)

# 6. 화면 레이아웃 구성
st.subheader("📂 주간 식단 가이드")

# [프레임 1] 날짜 선택
selected_date = st.selectbox("날짜", list(menu_data.keys()), index=1, label_visibility="collapsed")

# [프레임 2 & 3] 카드와 인덱스 탭 분할
col_card, col_tab = st.columns([8.2, 1.8])

with col_card:
    # 상세 내용 프레임
    menu = menu_data[selected_date].get(st.session_state.selected_meal, ["운영 정보 없음"])
    st.markdown(f"""
        <div class="main-card">
            <h2 style="color: {bold_c}; margin-bottom: 0;">{st.session_state.selected_meal}</h2>
            <div style="height: 1.5px; background-color: {bold_c}; opacity: 0.2; margin: 20px 0;"></div>
            <p style="font-size: 24px; font-weight: bold; color: #333; margin-bottom: 15px;">🍲 {menu[0]}</p>
            <p style="font-size: 17px; color: #555; line-height: 2.0;">{' / '.join(menu[1:])}</p>
        </div>
    """, unsafe_allow_html=True)

with col_tab:
    # 인덱스 탭 프레임
    for label in ["조식", "간편식", "중식", "석식", "야식"]:
        b_color, _ = color_map[label]
        if st.button(label, key=f"btn_{label}"):
            st.session_state.selected_meal = label
            st.rerun()
        
        # 버튼별 선명한 컬러 주입
        st.markdown(f"""
            <style>
            div[data-testid="stVerticalBlock"] > div:nth-child({["조식", "간편식", "중식", "석식", "야식"].index(label)+1}) button {{
                background-color: {b_color} !important;
            }}
            </style>
        """, unsafe_allow_html=True)
