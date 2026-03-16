import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime

st.set_page_config(page_title="성의교정 통합 식단 매니저", layout="wide")

# 1. 가독성 향상을 위한 커스텀 스타일
st.markdown("""
    <style>
    .reportview-container { background: #f0f2f6; }
    .menu-card {
        background-color: white;
        padding: 18px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border-top: 4px solid #2E7D32;
        margin-bottom: 10px;
    }
    .time-label { color: #2E7D32; font-weight: bold; font-size: 0.9rem; }
    .main-dish { font-size: 1.1rem; font-weight: bold; margin: 5px 0; }
    .side-dish { font-size: 0.85rem; color: #666; line-height: 1.4; }
    </style>
    """, unsafe_allow_html=True)

st.title("📅 주간 식단 통합 관리 시스템")
st.info("조식부터 야식까지 모든 시간대의 식단을 확인하고 엑셀로 저장할 수 있습니다.")

# 2. 전체 식단 데이터 구조화 (이미지 데이터 기반 샘플)
# 실제 운영 시에는 이 리스트에 전체 요일 데이터를 추가합니다.
full_data = [
    {"날짜": "3/13(금)", "시간대": "조식", "메인메뉴": "참치야채죽", "상세내용": "크로와상샌드위치, 잡곡식방, 오리엔탈샐러드, 우유/두유", "칼로리": "-"},
    {"날짜": "3/13(금)", "시간대": "간편식", "메인메뉴": "손이가요샌드위치", "상세내용": "사과주스 포함", "칼로리": "-"},
    {"날짜": "3/13(금)", "시간대": "중식", "메인메뉴": "소세지카레라이스", "상세내용": "완두콩밥, 유부장국, 실곤약초무침, 깍두기, 미숫가루", "칼로리": "773kcal"},
    {"날짜": "3/13(금)", "시간대": "석식", "메인메뉴": "춘천닭갈비", "상세내용": "유채된장국, 흰쌀밥, 청포묵무침, 와사비쌈무, 열무김치", "칼로리": "-"},
    {"날짜": "3/13(금)", "시간대": "야식", "메인메뉴": "우렁강된장덮밥", "상세내용": "미역국, 부추야채전, 동그랑땡구이, 깍두기, 포도주스", "칼로리": "-"},
    # 다른 요일 데이터도 동일한 형식으로 추가 가능
]

df = pd.DataFrame(full_data)

# 3. 요일 선택 및 필터링
days = ["월", "화", "수", "목", "금", "토", "일"]
selected_day = st.selectbox("조회할 요일을 선택하세요", days, index=4) # 기본 금요일

# 4. 화면 출력 (가독성 중심 카드 레이아웃)
st.subheader(f"🍴 {selected_day}요일 전체 식단")
day_df = df[df['날짜'].str.contains(selected_day)]

if not day_df.empty:
    cols = st.columns(len(day_df))
    for i, (idx, row) in enumerate(day_df.iterrows()):
        with cols[i]:
            st.markdown(f"""
                <div class="menu-card">
                    <div class="time-label">{row['시간대']}</div>
                    <div class="main-dish">{row['메인메뉴']}</div>
                    <div class="side-dish">{row['상세내용']}</div>
                    <div style="text-align:right; font-size:0.7rem; color:#999; mt-10">{row['칼로리']}</div>
                </div>
            """, unsafe_allow_html=True)
else:
    st.warning("해당 요일의 데이터가 입력되지 않았습니다.")

st.divider()

# 5. 전체 데이터 엑셀 다운로드 기능
st.subheader("📥 주간 식단표 엑셀 내보내기")
st.write("이미지 속의 모든 시간대(조식~야식) 데이터를 포함한 전체 엑셀 파일을 생성합니다.")

output = BytesIO()
with pd.ExcelWriter(output, engine='openpyxl') as writer:
    df.to_excel(writer, index=False, sheet_name='전체식단표')

st.download_button(
    label="🚀 주간 식단 전체 데이터 다운로드 (xlsx)",
    data=output.getvalue(),
    file_name=f"Catholic_Univ_Full_Menu_{datetime.now().strftime('%m%d')}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.table(df) # 전체 데이터 검토용 표
