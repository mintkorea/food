import streamlit as st
from datetime import datetime, timedelta, time

# 1. 한국 시간(KST) 강제 설정 (시차 10시간 오류 해결)
# 서버가 UTC 기준일 경우 9시간을 더해 한국 시간을 계산합니다.
now = datetime.utcnow() + timedelta(hours=9)
curr_t = now.time()
weekday = now.weekday()
day_names = ["월", "화", "수", "목", "금", "토", "일"]

# 2. 식단 데이터 및 설정
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

color_theme = {"조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"}
meal_times = {
    "조식": (time(7, 0), time(9, 0)),
    "중식": (time(11, 20), time(14, 0)),
    "석식": (time(17, 20), time(19, 20))
}

# 자동 식단 선택 로직
if curr_t < meal_times["중식"][0]: auto_meal = "조식"
elif curr_t < meal_times["석식"][0]: auto_meal = "중식"
else: auto_meal = "석식"

# 3. CSS: 여백 및 탭 위치 조정
day_color = "#E95444" if weekday == 6 else ("#4A90E2" if weekday == 5 else "#222")

st.markdown(f"""
<style>
    /* 상단 여백 극한으로 제거 */
    .main .block-container {{ max-width: 500px !important; padding: 0px 8px !important; margin-top: -50px !important; }}
    
    .date-title {{
        font-size: 20px !important; font-weight: 800; text-align: center;
        margin: 10px 0 !important; color: {day_color};
    }}

    /* 메뉴 카드 디자인 (탭이 아래로 가므로 상단 라운드 처리) */
    .menu-card {{
        border: 3px solid var(--card-color); border-radius: 20px 20px 0 0;
        padding: 30px 15px; text-align: center; background-color: white; min-height: 220px;
    }}

    .side-menu {{ color: #444; font-size: 17px !important; line-height: 1.6; font-weight: 500; margin-top: 15px; }}

    /* 인덱스 탭 디자인 (카드 아래 배치) */
    .index-tabs-wrap {{ display: flex; width: 100%; overflow: hidden; margin-top: -3px; }}
    .tab-unit {{
        flex: 1; text-align: center; padding: 10px 0;
        font-size: 13px !important; font-weight: bold; color: white;
    }}

    /* 라디오 버튼 (탭 바로 아래 배치) */
    div[data-testid="stRadio"] > div {{
        display: flex !important; flex-wrap: nowrap !important;
        background-color: #f1f3f5; padding: 10px 2px !important; border-radius: 0 0 20px 20px;
    }}
    div[data-testid="stRadio"] label {{ flex: 1 !important; justify-content: center !important; }}
    div[data-testid="stRadio"] label p {{ font-size: 13px !important; font-weight: 800 !important; white-space: nowrap !important; }}
    
    /* 하단 안내 박스 여백 확보 */
    .timer-box {{
        text-align: center; background-color: #f8f9fa; padding: 12px;
        border-radius: 12px; font-size: 14px; font-weight: bold; color: #555; margin: 15px 0 30px 0;
    }}
</style>
""", unsafe_allow_html=True)

# 4. UI 출력
st.markdown(f'<p class="date-title">📅 {now.strftime("%m월 %d일")} ({day_names[weekday]})</p>', unsafe_allow_html=True)

if 'selected_meal' not in st.session_state:
    st.session_state.selected_meal = auto_meal

# 메뉴 카드 (상단)
display_date = now.strftime("%Y-%m-%d")
current_meal = meal_data.get(display_date, meal_data["2026-03-18"]).get(st.session_state.selected_meal, {"menu": "정보 없음", "side": ""})
selected_color = color_theme[st.session_state.selected_meal]

st.markdown(f"""
    <div class="menu-card" style="--card-color: {selected_color};">
        <div style="color: {selected_color}; font-size: 14px; font-weight: bold; margin-bottom: 8px;">{st.session_state.selected_meal}</div>
        <div style="font-size: 26px; font-weight: 800; color: #111; margin-bottom: 12px;">{current_meal['menu']}</div>
        <div style="height: 1px; background-color: #eee; width: 35%; margin: 0 auto;"></div>
        <div class="side-menu">{current_meal['side']}</div>
    </div>
""", unsafe_allow_html=True)

# 인덱스 탭 (중간)
tabs_html = '<div class="index-tabs-wrap">'
for meal, color in color_theme.items():
    opacity = "1.0" if meal == st.session_state.selected_meal else "0.3"
    tabs_html += f'<div class="tab-unit" style="background-color: {color}; opacity: {opacity};">{meal}</div>'
tabs_html += '</div>'
st.markdown(tabs_html, unsafe_allow_html=True)

# 라디오 버튼 (하단)
selected = st.radio("식단선택", options=list(color_theme.keys()), 
                    index=list(color_theme.keys()).index(st.session_state.selected_meal),
                    horizontal=True, label_visibility="collapsed")

if selected != st.session_state.selected_meal:
    st.session_state.selected_meal = selected
    st.rerun()

# 5. 시간 계산 로직 (몇 시간 몇 분 형식)
if st.session_state.selected_meal in meal_times:
    s_t, e_t = meal_times[st.session_state.selected_meal]
    s_dt, e_dt = datetime.combine(now.date(), s_t), datetime.combine(now.date(), e_t)
    
    if now < s_dt:
        diff = s_dt - now
        h, m = diff.seconds // 3600, (diff.seconds % 3600) // 60
        msg = f"⌛ {st.session_state.selected_meal} 시작까지 {f'{h}시간 ' if h > 0 else ''}{m}분 남음"
    elif now <= e_dt:
        diff = e_dt - now
        h, m = diff.seconds // 3600, (diff.seconds % 3600) // 60
        msg = f"🍴 {st.session_state.selected_meal} 배식 중! 종료까지 {f'{h}시간 ' if h > 0 else ''}{m}분 남음"
    else:
        msg = f"🚩 오늘의 {st.session_state.selected_meal} 배식이 완료되었습니다."
else:
    msg = f"💡 {st.session_state.selected_meal} 메뉴를 확인 중입니다."

st.markdown(f'<div class="timer-box">{msg}</div>', unsafe_allow_html=True)
