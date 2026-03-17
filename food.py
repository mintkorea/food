import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 데이터 로드 설정 ---
# 구글 시트에서 [파일] -> [공유] -> [웹에 게시] -> [쉼표로 구분된 값(.csv)]로 선택 후 
# 생성된 URL을 아래 SHEET_URL에 넣으시면 실시간 연동됩니다.
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/your_id/pub?output=csv"

def get_menu_data():
    try:
        # 실제 운영 시 아래 주석 해제하여 구글 시트와 연동
        # df = pd.read_csv(SHEET_URL)
        # return df
        
        # 테스트용 로컬 데이터 (이미지 분석 결과 반영)
        data = {
            "date": ["2026-03-17(화)", "2026-03-17(화)", "2026-03-17(화)", "2026-03-17(화)", "2026-03-17(화)"],
            "type": ["조식", "간편식", "중식", "석식", "야식"],
            "main": ["제철미나리쭈꾸미연포탕", "고로케양배추샌드위치", "버섯불고기", "양배추멘치카츠", "소고기미역죽"],
            "sub": ["매운두부찜, 흰쌀밥, 모둠장아찌", "삶은계란, 플레인요거트", "우엉채레몬튀김, 수수기장밥, 얼큰어묵탕", "가쓰오장국, 시저드레싱샐러드", "돈육장조림, 깍두기, 블루베리요플레"]
        }
        return pd.DataFrame(data)
    except:
        return pd.DataFrame()

# --- 2. 초기 세팅 및 시간 감지 ---
st.set_page_config(page_title="Index Menu", layout="centered")

now = datetime.now()
curr_hour = now.hour

# 현재 시간에 따른 자동 탭 선택 로직
if curr_hour < 9: default_type = "조식"
elif 9 <= curr_hour < 11: default_type = "간편식"
elif 11 <= curr_hour < 14: default_type = "중식"
elif 14 <= curr_hour < 19: default_type = "석식"
else: default_meal = "야식"

if 'selected_meal' not in st.session_state:
    st.session_state.selected_meal = "중식" # 기본값

# --- 3. 디자인 CSS (인덱스 탭 스타일) ---
st.markdown("""
    <style>
    /* 전체 배경 및 폰트 */
    [data-testid="stAppViewContainer"] { background-color: #F0F2F5; }
    
    /* 인덱스 버튼 공통 스타일 */
    .stButton > button {
        width: 100%;
        height: 70px;
        writing-mode: vertical-rl; /* 세로 글자 */
        text-orientation: upright;
        border-radius: 0px 10px 10px 0px; /* 오른쪽만 둥글게 */
        margin-bottom: 5px;
        border: none;
        color: white !important;
        font-weight: bold;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    
    /* 메인 카드 영역 */
    .menu-card {
        background: white;
        padding: 40px 20px;
        border-radius: 20px 0px 0px 20px; /* 왼쪽만 둥글게 */
        min-height: 400px;
        text-align: center;
        box-shadow: -5px 5px 15px rgba(0,0,0,0.08);
        border-right: 5px solid #E0E0E0;
    }
    
    /* 식사별 색상 코드 */
    .btn-breakfast { background-color: #FF9F43 !important; }
    .btn-snack { background-color: #FEB236 !important; }
    .btn-lunch { background-color: #28C76F !important; }
    .btn-dinner { background-color: #5C5EDC !important; }
    .btn-late { background-color: #A06EE1 !important; }
    </style>
""", unsafe_allow_html=True)

# --- 4. 메인 UI 레이아웃 ---
df = get_menu_data()
st.title("📂 주간 식단 가이드북")

# 날짜 선택기
selected_date = st.selectbox("날짜", df['date'].unique(), label_visibility="collapsed")

# 메인 레이아웃 (카드 8.5 : 인덱스 1.5)
col_card, col_index = st.columns([8.5, 1.5], gap="none")

with col_index:
    # 물리적인 인덱스 카드 탭 구현
    if st.button("조식", key="btn_bf"): st.session_state.selected_meal = "조식"
    if st.button("간편", key="btn_sn"): st.session_state.selected_meal = "간편식"
    if st.button("중식", key="btn_lu"): st.session_state.selected_meal = "중식"
    if st.button("석식", key="btn_di"): st.session_state.selected_meal = "석식"
    if st.button("야식", key="btn_la"): st.session_state.selected_meal = "야식"

with col_card:
    # 선택된 데이터 필터링
    row = df[(df['date'] == selected_date) & (df['type'] == st.session_state.selected_meal)]
    
    if not row.empty:
        main_dish = row['main'].values[0]
        sub_dishes = row['sub'].values[0]
        
        st.markdown(f"""
            <div class="menu-card">
                <p style="color: #888; font-size: 14px;">{selected_date}</p>
                <h2 style="margin-top: 0px;">{st.session_state.selected_meal}</h2>
                <div style="margin: 30px 0;">
                    <span style="font-size: 28px; font-weight: 800; color: #333;">🍲 {main_dish}</span>
                </div>
                <p style="color: #666; line-height: 1.8; font-size: 18px;">
                    {sub_dishes.replace(',', '<br>')}
                </p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="menu-card"><h3>정보 없음</h3></div>', unsafe_allow_html=True)
