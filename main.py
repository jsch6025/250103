import streamlit as st
import pandas as pd
import plotly.express as px

# 제목 및 설명 추가
st.title('서울 자치구별 인구수 변화 대시보드')
st.write('최근 30년간 서울시 자치구의 인구 변화를 시각화합니다.')

# 파일 업로드 기능
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요.", type=['csv'])

if uploaded_file is not None:
    # 데이터 로드
    data = pd.read_csv(uploaded_file)

    # 데이터 확인
    st.write("### 데이터 미리보기")
    st.write(data.head())

    # 사용자 입력: 자치구 선택
    districts = sorted(data['자치구'].unique())
    selected_district = st.selectbox('확인할 자치구를 선택하세요:', districts)

    # 데이터 필터링
    filtered_data = data[data['자치구'] == selected_district]

    # 시각화
    st.write(f"### {selected_district}의 인구수 변화")
    fig = px.line(filtered_data, x='년도', y='인구수', markers=True, title=f'{selected_district}의 인구수 변화')
    st.plotly_chart(fig)
else:
    st.write("CSV 파일을 업로드하세요.")
