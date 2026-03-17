import streamlit as st
from datetime import datetime

# 1. [데이터] 3월 16일 ~ 3월 22일 주간 식단표 데이터
# 이미지에서 추출한 이번 주 실제 식단 정보입니다.
meal_data = {
    "2026-03-16": {
        "조식": {"menu": "두우스프 / 단호박에그마요샌드", "side": "바게트, 잡곡식빵&딸기잼, 버터, 맛살마요범벅, 오리엔탈샐러드, 씨리얼2종"},
        "간편식": {"menu": "미운영", "side": "월요일은 간편식을 운영하지 않습니다."},
        "중식": {"menu": "차돌해물짬뽕밥", "side": "김말이튀김, 갈리강정소스, 흑향미밥, 그린샐러드&딸기요거트, 깍두기, 매실주스"},
        "석식": {"menu": "어항가지돈육덮밥", "side": "흰쌀밥, 사골파국, 감자채햄볶음, 망고드레싱샐러드, 깍두기"},
        "야식": {"menu": "날치알볶음밥", "side": "후랑크소세지, 김칫국, 참깨드레싱샐러드, 연근조림, 요구르트"}
    },
    "2026-03-17": {
        "조식": {"menu": "제철미나리쭈꾸미연포탕", "side": "매운두부찜, 흰쌀밥, 모둠장아찌, 깍두기, 누룽지/원두커피"},
        "간편식": {"menu": "고구마무스샌드위치", "side": "삶은계란 & 플레인요거트"},
        "중식": {"menu": "버섯불고기", "side": "우엉채레몬튀김, 수수기장밥, 얼큰어묵탕, 참나물무중겉절이, 수정과"},
        "석식": {"menu": "양배추멘치카츠", "side": "양배추카츠+구운야채, 흰쌀밥, 가쓰오장국, 시저드레싱샐러드, 열무김치"},
        "야식": {"menu": "소고기미역죽", "side": "돈육장조림, 깍두기, 블루베리요플레"}
    },
    "2026-03-18": {
        "조식": {"menu": "감자수제비", "side": "흰쌀밥, 돈채가지볶음, 양념고추지, 깍두기, 누룽지/원두커피"},
        "간편식": {"menu": "닭가슴살샐러드 & 바나나", "side": ""},
        "중식": {"menu": "뼈없는닭볶음탕", "side": "혼합잡곡밥, 팽이장국, 유부겨자냉채, 흑깨드레싱샐러드, 열무김치, 복분자주스"},
        "석식": {"menu": "하이디라오마라탕", "side": "분모자+포두부+소세지 & 탕수육, 후르츠소스, 흰쌀밥, 짜사이무침, 열무김치"},
        "야식": {"menu": "돈사태떡찜", "side": "흰쌀밥, 유채된장국, 땅콩드레싱샐러드, 멸치볶음, 양파장아찌, 요구르트"}
    },
    "2026-03-19": {
        "조식": {"menu": "시래기장터국밥", "side": "모둠땡전, 케찹, 흰쌀밥, 치커리유자무침, 깍두기, 짜계치&라면3종"},
        "간편식": {"menu": "어니언치즈베이글샌드위치", "side": "얼리브망고쥬스"},
        "중식": {"menu": "통등심돈까스 & 데미소스", "side": "비빔막국수, 추가쌀밥, 미역국, 사우전드레싱샐러드, 깍두기, 레몬아이스티"},
        "석식": {"menu": "돼지목살필라프", "side": "우동장국, 삼색푸실리케찹볶음, 단무지무침, 포기김치, 망고주스"},
        "야식": {"menu": "함박스테이크", "side": "흰쌀밥, 콩가루배춧국, 실곤약초무침, 오복채, 열무김치, 망고주스"}
    },
    "2026-03-20": {
        "조식": {"menu": "김치해장죽 / 고구마파이", "side": "버터롤, 바게트&딸기잼, 버터, 오리엔탈샐러드, 씨리얼2종, 누룽지"},
        "간편식": {"menu": "미운영", "side": "금요일은 간편식을 운영하지 않습니다."},
        "중식": {"menu": "뿌리채소영양밥 & 양념장", "side": "언양식바싹구이, 파채, 아욱된장국, 도토리묵야채무침, 포기김치, 식혜"},
        "석식": {"menu": "셀프쭈불비빔밥", "side": "콩보리밥+쭈불볶음+김가루, 시금치된장국, 콩나물무침, 무생채, 열무김치"},
        "야식": {"menu": "치킨토마토샌드위치", "side": "피치우롱티"}
    }
}

# 2. 색상 테마 및 시간대 설정
color_theme = {"조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"}
current_date = datetime.now().strftime("%Y-%m-%d")
if current_date not in meal_data:
    current_date = "2026-03-17" # 데이터가 없는 날은 화요일로 예시

# 3. CSS: 모바일 폰트 크기 최적화 및 레이아웃 고정
st.markdown(f"""
<style>
    .main .block-container {{ max-width: 500px !important; padding: 10px 8px !important; }}
    
    .menu-card {{
        border: 3px solid var(--card-color);
        border-radius: 15px 15px 0 0;
        padding: 45px 15px;
        text-align: center;
        background-color: white;
        min-height: 280px;
    }}

    .index-tabs-wrap {{ display: flex; width: 100%; margin-bottom: 2px; }}
    .tab-unit {{
        flex: 1; text-align: center; padding: 12px 0;
        font-size: 12px !important; font-weight: bold; color: white;
    }}

    /* 라디오 버튼 컨트롤러 (텍스트 크기 확대 버전) */
    div[data-testid="stRadio"] > div {{
        display: flex !important; flex-direction: row !important;
        flex-wrap: nowrap !important; justify-content: space-between !important;
        background-color: #f1f3f5; padding: 12px 2px !important; border-radius: 0 0 15px 15px;
    }}
    div[data-testid="stRadio"] label {{ flex: 1 !important; justify-content: center !important; margin: 0 !important; }}
    div[data-testid="stRadio"] label p {{
        font-size: 14px !important; font-weight: 800 !important; color: #333 !important;
    }}
</style>
""", unsafe_allow_html=True)

# 4. 상단 날짜 및 식단 선택 세션 관리
st.subheader(f"📅 {current_date} 식단 가이드")
if 'selected_meal' not in st.session_state:
    st.session_state.selected_meal = "중식"

# 5. 데이터 표시 로직
current_meal = meal_data[current_date].get(st.session_state.selected_meal, {"menu": "정보 없음", "side": ""})
selected_color = color_theme[st.session_state.selected_meal]

st.markdown(f"""
    <div class="menu-card" style="--card-color: {selected_color};">
        <div style="color: {selected_color}; font-size: 16px; font-weight: bold; margin-bottom: 15px;">{st.session_state.selected_meal}</div>
        <div style="font-size: 26px; font-weight: 800; color: #222; margin-bottom: 20px; word-break: keep-all;">{current_meal['menu']}</div>
        <div style="height: 1px; background-color: #eee; width: 50%; margin: 0 auto 20px;"></div>
        <div style="color: #555; font-size: 15px; line-height: 1.6; word-break: keep-all;">{current_meal['side']}</div>
    </div>
""", unsafe_allow_html=True)

# 6. 하단 인덱스 탭 & 라디오 버튼
tabs_html = '<div class="index-tabs-wrap">'
for meal, color in color_theme.items():
    opacity = "1.0" if meal == st.session_state.selected_meal else "0.3"
    tabs_html += f'<div class="tab-unit" style="background-color: {color}; opacity: {opacity};">{meal}</div>'
tabs_html += '</div>'
st.markdown(tabs_html, unsafe_allow_html=True)

selected = st.radio("식단선택", options=list(color_theme.keys()), 
                    index=list(color_theme.keys()).index(st.session_state.selected_meal),
                    horizontal=True, label_visibility="collapsed")

if selected != st.session_state.selected_meal:
    st.session_state.selected_meal = selected
    st.rerun()
