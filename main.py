import streamlit as st
import pandas as pd
import plotly.express as px

# 제목 및 설명 추가
st.title('서울 자치구별 나이대별 인구수 변화')
st.write('최근 30년간 서울시 자치구의 나이대별 인구 변화를 시각화합니다.')

# 데이터 불러오기
@st.cache_data
def load_data():
    data = pd.read_csv('seoul_population_age.csv')
    return data

# 데이터 로드
try:
    data = load_data()
except FileNotFoundError:
    st.error("데이터 파일을 찾을 수 없습니다. 파일 경로를 확인하세요.")
    st.stop()

# 데이터 확인
st.write("### 데이터 미리보기")
st.write(data.head())

# 사용자 입력: 자치구 선택
districts = sorted(data['자치구'].unique())
selected_districts = st.multiselect('자치구 선택:', districts, default=[districts[0]])

# 사용자 입력: 년도 선택
years = sorted(data['년도'].unique())
selected_years = st.slider('년도 범위 선택:', min_value=min(years), max_value=max(years), value=(min(years), max(years)))

# 사용자 입력: 나이대 선택
ages = sorted(data['나이대'].unique())
selected_ages = st.multiselect('나이대 선택:', ages, default=[ages[0]])

# 데이터 필터링
filtered_data = data[(data['자치구'].isin(selected_districts)) & 
                      (data['년도'] >= selected_years[0]) & 
                      (data['년도'] <= selected_years[1]) &
                      (data['나이대'].isin(selected_ages))]

# 시각화
st.write(f"### 선택한 자치구의 나이대별 인구수 변화 ({selected_years[0]}년 ~ {selected_years[1]}년)")
fig = px.line(filtered_data, x='년도', y='인구수', color='나이대', markers=True, title='나이대별 인구수 변화')
st.plotly_chart(fig)
