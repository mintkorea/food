import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 데이터 세팅 ---
def get_menu_data():
    data = {
        "date": ["2026-03-17(화)"] * 5,
        "type": ["조식", "간편식", "중식", "석식", "야식"],
        "main": ["제철미나리쭈꾸미연포탕", "고로케양배추샌드위치", "버섯불고기", "양배추멘치카츠", "소고기미역죽"],
        "sub": ["매운두부찜, 흰쌀밥, 모둠장아찌", "삶은계란, 플레인요거트", "우엉채레몬튀김, 수수기장밥", "가쓰오장국, 시저드레싱샐러드", "돈육장조림, 깍두기"]
    }
    return pd.DataFrame(data)

# --- 2. 초기 세팅 ---
st.set_page_config(page_title="Index Menu", layout="centered")

if 'selected_meal' not in st.session_state:
    st.session_state.selected_meal = "중식"

# --- 3. 디자인 CSS (타이틀 크기 조절 및 인덱스 최적화) ---
st.markdown("""
    <style>
    /* 타이틀 크기 강제 축소 */
    .app-title {
        font-size: 24px !important;
        font-weight: 800;
        margin-bottom: 10px;
        color: #333;
    }
    
    /* 인덱스 버튼 세로 배치 및 크기 조절 */
    .stButton > button {
        width: 100%;
        height: 65px;
        writing-mode: vertical-rl;
        text-orientation: upright;
        border-radius: 0px 8px 8px 0px;
        margin-bottom: 4px;
        border: none;
        color: white !important;
        font-size: 14px;
        font-weight: bold;
        padding: 0px;
    }
    
    /* 식사별 색상 */
    div.row-widget.stButton:nth-of-type(1) > button { background-color: #FF9F43; } 
    div.row-widget.stButton:nth-of-type(2) > button { background-color: #FEB236; color: black !important; } 
    div.row-widget.stButton:nth-of-type(3) > button { background-color: #28C76F; } 
    div.row-widget.stButton:nth-of-type(4) > button { background-color: #5C5EDC; } 
    div.row-widget.stButton:nth-of-type(5) > button { background-color: #A06EE1; }

    .menu-card {
        background: white;
        padding: 25px 15px;
        border-radius: 15px 0px 0px 15px;
        min-height: 350px;
        text-align: center;
        box-shadow: -3px 3px 10px rgba(0,0,0,0.05);
        border-right: 3px solid #eee;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. 메인 UI ---
# 기존 st.title 대신 마크다운으로 작게 표시
st.markdown('<p class="app-title">📂 주간 식단 가이드</p>', unsafe_allow_html=True)

df = get_menu_data()
selected_date = st.selectbox("날짜", df['date'].unique(), label_visibility="collapsed")

# 에러 수정 포인트: gap="none"을 제거하거나 "small"로 변경
col_card, col_index = st.columns([8.2, 1.8], gap="small")

with col_index:
    if st.button("조식"): st.session_state.selected_meal = "조식"
    if st.button("간편"): st.session_state.selected_meal = "간편식"
    if st.button("중식"): st.session_state.selected_meal = "중식"
    if st.button("석식"): st.session_state.selected_meal = "석식"
    if st.button("야식"): st.session_state.selected_meal = "야식"

with col_card:
    row = df[(df['date'] == selected_date) & (df['type'] == st.session_state.selected_meal)]
    if not row.empty:
        st.markdown(f"""
            <div class="menu-card">
                <p style="color: #999; font-size: 12px; margin-bottom:5px;">{selected_date}</p>
                <h3 style="margin: 0; color: #444;">{st.session_state.selected_meal}</h3>
                <hr style="margin: 15px 0; border: 0.5px solid #eee;">
                <div style="margin: 20px 0;">
                    <span style="font-size: 22px; font-weight: bold; color: #d32f2f;">🍲 {row['main'].values[0]}</span>
                </div>
                <p style="color: #666; font-size: 16px; line-height: 1.6;">
                    {row['sub'].values[0].replace(',', '<br>')}
                </p>
            </div>
        """, unsafe_allow_html=True)
