import streamlit as st
from datetime import datetime

# [데이터] 주간 식단표 데이터 (생략된 날짜는 이전과 동일하게 유지)
meal_data = {
    "2026-03-17": {
        "조식": {"menu": "제철미나리쭈꾸미연포탕", "side": "매운두부찜, 흰쌀밥, 모둠장아찌, 깍두기, 누룽지/원두커피"},
        "간편식": {"menu": "고구마무스샌드위치", "side": "삶은계란 & 플레인요거트"},
        "중식": {"menu": "버섯불고기", "side": "우엉채레몬튀김, 수수기장밥, 얼큰어묵탕, 참나물무중겉절이, 수정과"},
        "석식": {"menu": "양배추멘치카츠", "side": "양배추카츠+구운야채, 흰쌀밥, 가쓰오장국, 시저드레싱샐러드, 열무김치"},
        "야식": {"menu": "소고기미역죽", "side": "돈육장조림, 깍두기, 블루베리요플레"}
    }
}

color_theme = {"조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"}
current_date = "2026-03-17"

# CSS: 여백 제거 및 폰트 크기 정밀 조정
st.markdown(f"""
<style>
    /* 1. 상단 여백 제거 */
    .main .block-container {{ 
        max-width: 500px !important; 
        padding: 5px 8px !important; /* 상단 패딩 최소화 */
    }}
    
    /* 2. 제목(날짜) 폰트 크기 축소 및 간격 조절 */
    .date-title {{
        font-size: 20px !important; 
        font-weight: 700;
        margin-bottom: 5px !important;
        color: #333;
    }}

    /* 3. 메뉴 카드 높이 조절 및 내부 여백 */
    .menu-card {{
        border: 3px solid var(--card-color);
        border-radius: 15px 15px 0 0;
        padding: 30px 10px; /* 위아래 패딩 축소 */
        text-align: center;
        background-color: white;
        min-height: 220px; /* 전체 높이 감소 */
    }}

    /* 4. 식단 텍스트(반찬 등) 폰트 크기 상향 */
    .side-menu {{
        color: #444; 
        font-size: 17px !important; /* 기존보다 2pt 상향 */
        line-height: 1.5; 
        word-break: keep-all;
        margin-top: 15px;
        font-weight: 500;
    }}

    .index-tabs-wrap {{ display: flex; width: 100%; margin-bottom: 2px; }}
    .tab-unit {{
        flex: 1; text-align: center; padding: 10px 0;
        font-size: 12px !important; font-weight: bold; color: white;
    }}

    /* 5. 라디오 버튼: '간편식' 개행 방지 및 폰트 최적화 */
    div[data-testid="stRadio"] > div {{
        display: flex !important; flex-direction: row !important;
        flex-wrap: nowrap !important; justify-content: space-between !important;
        background-color: #f1f3f5; padding: 12px 1px !important; border-radius: 0 0 15px 15px;
    }}
    div[data-testid="stRadio"] label {{ 
        flex: 1 !important; 
        min-width: 65px !important; /* 최소 너비 확보로 개행 방지 */
        justify-content: center !important; 
        margin: 0 !important; 
    }}
    div[data-testid="stRadio"] label p {{
        font-size: 13.5px !important; /* 버튼 텍스트 살짝 조절 */
        font-weight: 800 !important; 
        letter-spacing: -0.5px; /* 자간 축소로 개행 방지 */
    }}
</style>
""", unsafe_allow_html=True)

# 4. 상단 날짜 (폰트 크기 조절된 커스텀 태그)
st.markdown(f'<p class="date-title">📅 {current_date} 식단 가이드</p>', unsafe_allow_html=True)

if 'selected_meal' not in st.session_state:
    st.session_state.selected_meal = "중식"

# 5. 데이터 표시
current_meal = meal_data[current_date].get(st.session_state.selected_meal, {"menu": "정보 없음", "side": ""})
selected_color = color_theme[st.session_state.selected_meal]

st.markdown(f"""
    <div class="menu-card" style="--card-color: {selected_color};">
        <div style="color: {selected_color}; font-size: 15px; font-weight: bold; margin-bottom: 10px;">{st.session_state.selected_meal}</div>
        <div style="font-size: 26px; font-weight: 800; color: #111; margin-bottom: 12px; word-break: keep-all;">{current_meal['menu']}</div>
        <div style="height: 1px; background-color: #eee; width: 40%; margin: 0 auto;"></div>
        <div class="side-menu">{current_meal['side']}</div>
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
