import streamlit as st

# 1. 상태 관리 및 테마
color_theme = {
    "조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"
}

# 쿼리 파라미터를 통해 선택된 메뉴 파악 (새로고침 대응)
params = st.query_params
current = params.get("meal", "중식")

# 2. CSS: 모바일에서 절대 벌어지지 않는 고정 탭 디자인
st.markdown(f"""
<style>
    .main .block-container {{ max-width: 500px !important; padding: 10px !important; }}
    
    /* 탭 컨테이너: 가로로 꽉 차게 고정 */
    .tab-container {{
        display: flex;
        width: 100%;
        gap: 2px;
        margin-top: 10px;
    }}
    
    /* 개별 탭 버튼 스타일 */
    .tab-item {{
        flex: 1;
        text-align: center;
        padding: 12px 0;
        font-size: 14px;
        font-weight: bold;
        color: white;
        text-decoration: none;
        border-radius: 8px;
        transition: 0.2s;
    }}
    
    .meal-card {{
        border: 2px solid {color_theme.get(current, "#8BC34A")};
        border-radius: 15px; padding: 30px 10px; text-align: center;
        background-color: white; margin-bottom: 10px;
    }}
</style>
""", unsafe_allow_html=True)

# 3. 메인 표시 카드
st.markdown(f"""
    <div class="meal-card">
        <h1 style="color: {color_theme.get(current, "#8BC34A")}; margin: 0;">{current}</h1>
    </div>
""", unsafe_allow_html=True)

# 4. 탭 메뉴 생성 (HTML 앵커 태그 사용)
# 클릭 시 URL 파라미터를 변경하여 즉시 화면을 갱신합니다.
tabs_html = '<div class="tab-container">'
for meal, color in color_theme.items():
    # 선택된 메뉴는 선명하게, 나머지는 흐리게
    opacity = "1.0" if meal == current else "0.3"
    tabs_html += f'''
        <a href="/?meal={meal}" target="_self" class="tab-item" 
           style="background-color: {color}; opacity: {opacity};">
            {meal}
        </a>
    '''
tabs_html += '</div>'

st.markdown(tabs_html, unsafe_allow_html=True)

# 5. 선택된 메뉴에 따른 실제 데이터 출력 (예시)
st.write(f"### 🍱 {current} 식단표")
st.info(f"현재 {current} 메뉴 데이터를 불러오는 중입니다...")
