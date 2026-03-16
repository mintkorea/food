import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime

st.set_page_config(page_title="성의교정 전체 식단 변환기", layout="wide")

# 1. 일주일 전체 식단 데이터 (이미지 내용을 바탕으로 구성)
# 실제 운영 시에는 이 부분을 추출된 데이터 리스트로 대체하게 됩니다.
full_menu_data = [
    {"날짜": "3/9(월)", "구분": "중식", "메인": "제철봄동비빔밥", "상세": "보리밥,계란후라이,데리야끼떡갈비,미역국,열무김치"},
    {"날짜": "3/9(월)", "구분": "석식", "메인": "부대찌개", "상세": "라면사리,견과류연근조림,코울슬로,깍두기"},
    {"날짜": "3/10(화)", "구분": "중식", "메인": "뚝배기대파육개장", "상세": "생선까스,와사비마요,참나물유자겉절이,깍두기"},
    {"날짜": "3/10(화)", "구분": "석식", "메인": "제주고기국수", "상세": "추가쌀밥,다대기,손만두,배추겉절이"},
    {"날짜": "3/11(수)", "구분": "중식", "메인": "불고기호박오일파스타", "상세": "쓰리라차닭살구이,오리엔탈샐러드,매실주스"},
    {"날짜": "3/11(수)", "구분": "석식", "메인": "시래기감자탕", "상세": "두부양념조림,쌈채소무침,깍두기"},
    {"날짜": "3/12(목)", "구분": "중식", "메인": "고추장두루치기", "상세": "청상추쌈,얼갈이된장국,마카로니콘마요,수정과"},
    {"날짜": "3/12(목)", "구분": "석식", "메인": "뚝배기불고기나베", "상세": "당면사리,소떡소떡강정,마늘종무침,깍두기"},
    {"날짜": "3/13(금)", "구분": "중식", "메인": "소세지카레라이스", "상세": "완두콩밥,유부장국,실곤약초무침,미숫가루"},
    {"날짜": "3/13(금)", "구분": "석식", "메인": "춘천닭갈비", "상세": "유채된장국,청포묵무침,와사비쌈무,열무김치"},
]

df_full = pd.DataFrame(full_menu_data)

# 2. UI 구성
st.title("📊 성의교정 주간 식단 전체 엑셀 변환")
st.info("업로드된 이미지의 전체 데이터를 표 형식으로 정리했습니다. 아래 버튼을 눌러 엑셀로 저장하세요.")

# 3. 데이터 미리보기 (가독성 확보)
st.subheader("🗓️ 이번 주 식단 미리보기")
st.dataframe(df_full, use_container_width=True)

st.divider()

# 4. 전체 데이터 엑셀 변환 및 다운로드
def to_excel(df):
    output = BytesIO()
    # openpyxl 엔진을 사용하여 호환성 극대화
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='주간식단표')
    return output.getvalue()

excel_data = to_excel(df_full)

st.download_button(
    label="📥 주간 식단표 전체 엑셀 다운로드 (.xlsx)",
    data=excel_data,
    file_name=f"Catholic_Univ_Menu_Full_{datetime.now().strftime('%m%d')}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# 5. 가독성 카드 뷰 (오늘 날짜 기준)
st.subheader("💡 오늘의 핵심 메뉴")
today_menu = df_full[df_full['날짜'].str.contains("3/13")] # 금요일 예시

cols = st.columns(len(today_menu))
for i, (idx, row) in enumerate(today_menu.iterrows()):
    with cols[i]:
        st.success(f"**{row['구분']}**")
        st.markdown(f"**{row['메인']}**")
        st.caption(row['상세'])
