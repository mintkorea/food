import streamlit as st
from datetime import datetime

# 1. 페이지 설정 및 데이터 (데이터는 이전과 동일)
st.set_page_config(page_title="스마트 식단 가이드", layout="centered")

menu_data = {
    "2026-03-17(화)": {
        "조식": ["제철미나리쭈꾸미연포탕", "매운두부찜", "모둠장아찌", "누룽지"],
        "간편식": ["고로케양배추샌드위치", "삶은계란", "플레인요거트"],
        "중식": ["버섯불고기", "우엉채레몬튀김", "수수기장밥", "얼큰어묵탕", "수정과"],
        "석식": ["양배추멘치카츠", "가쓰오장국", "시저드레싱샐러드", "열무김치"],
        "야식": ["소고기미역죽", "돈육장조림", "블루베리요플레"]
    }
}

# 2. 사이드바를 인덱스 프레임으로 활용
with st.sidebar:
    st.header("🗂️ 식사 선택")
    meal_labels = ["조식", "간편식", "중식", "석식", "야식"]
    
    # 시간대별 컬러 정의 (사이드바 버튼용)
    selected_meal = st.radio(
        "확인할 식사 시간을 선택하세요",
        meal_labels,
        index=2 # 기본값 중식
    )
    st.info("💡 사이드바에서 메뉴를 선택하면 메인 화면이 바뀝니다.")

# 3. 메인 화면 프레임 디자인 (부드러운 컬러 반영)
color_map = {
    "조식": ("#E95444", "#FFF5F4"),
    "간편식": ("#F1A33B", "#FFF9F0"),
    "중식": ("#8BC34A", "#F9FBF2"),
    "석식": ("#4A90E2", "#F0F7FF"),
    "야식": ("#673AB7", "#F7F2FF")
}

bold_c, soft_c = color_map[selected_meal]

st.markdown(f"""
    <style>
    /* 메인 카드 프레임 최적화 */
    .main-card {{
        background-color: {soft_c};
        height: 80vh; /* 화면 높이의 80% 사용 */
        border-radius: 20px;
        border: 3px solid {bold_c};
        padding: 30px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }}
    </style>
""", unsafe_allow_html=True)

# 4. 콘텐츠 출력
st.title("📂 주간 식단 가이드")
selected_date = st.selectbox("날짜", list(menu_data.keys()), label_visibility="collapsed")

menu = menu_data[selected_date].get(selected_meal, ["정보 없음"])

st.markdown(f"""
    <div class="main-card">
        <h1 style="color: {bold_c}; margin-bottom: 0;">{selected_meal}</h1>
        <hr style="border: 1px solid {bold_c}; opacity: 0.2; margin: 25px 0;">
        <p style="font-size: 26px; font-weight: bold; color: #333;">🍲 {menu[0]}</p>
        <p style="font-size: 18px; color: #666; line-height: 2.0;">{' / '.join(menu[1:])}</p>
    </div>
""", unsafe_allow_html=True)
