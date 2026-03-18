import streamlit as st

# 1. 고정 그리드 레이아웃 설정 (비상연락망 방식 적용)
st.markdown("""
<style>
    /* 전체 컨테이너 폭 고정 */
    .block-container { padding-top: 2rem; max-width: 500px !important; }

    /* [핵심] 비상연락망 스타일의 가로 그리드 레이어 */
    .grid-layer {
        display: grid;
        grid-template-columns: repeat(5, 1fr); /* 무조건 가로 5칸 고정 */
        gap: 4px;
        background-color: #f0f2f6;
        padding: 5px;
        border-radius: 10px;
        margin-top: -10px; /* 상단 식단 카드와 밀착 */
    }

    /* 그리드 내 버튼 스타일 (넘버셸 제거된 비상연락망 느낌) */
    .grid-layer button {
        width: 100%;
        height: 45px !important;
        border: none !important;
        font-size: 13px !important;
        font-weight: 800 !important;
        background-color: white !important;
        color: #333 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* 선택된 버튼 강조 레이어 */
    .selected-btn button {
        background-color: #8BC34A !important; /* 중식 등 테마색 */
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# 2. 식단 카드 (상단 레이어)
st.markdown("""
    <div style="border: 1px solid #ddd; border-top: 10px solid #8BC34A; border-radius: 10px 10px 0 0; padding: 20px; text-align: center; background: white;">
        <div style="font-size: 14px; color: #8BC34A; font-weight: bold;">중식</div>
        <div style="font-size: 22px; font-weight: 800; margin: 10px 0;">뼈있는닭볶음탕</div>
        <div style="font-size: 15px; color: #666;">혼합잡곡밥, 팽이장국, 유부겨자냉채...</div>
    </div>
""", unsafe_allow_html=True)

# 3. 버튼 그리드 레이어 (하단)
# Streamlit에서 class를 직접 부여하기 위해 container와 columns 조합
grid_container = st.container()
with grid_container:
    cols = st.columns(5)
    meals = ["조식", "간편식", "중식", "석식", "야식"]
    
    for i, m in enumerate(meals):
        with cols[i]:
            # 현재 선택된 메뉴인 경우 스타일을 다르게 적용
            is_selected = (m == "중식") 
            if st.button(m, key=f"btn_{i}"):
                st.session_state.selected_meal = m
                st.rerun()

# [비상연락망 노하우] CSS 선택자로 특정 순서 버튼 색상 강제 지정
st.markdown(f"""
<style>
    div[data-testid="column"]:nth-of-type({meals.index("중식")+1}) button {{
        background-color: #8BC34A !important;
        color: white !important;
    }}
</style>
""", unsafe_allow_html=True)
