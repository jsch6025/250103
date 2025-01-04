import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 제목 및 설명 추가
st.title('서울 자치구별 인구수 변화 대시보드')
st.write('최근 30년간 서울시 자치구의 인구 변화를 시각화합니다.')

# 데이터 불러오기
@st.cache_data
def load_data():
    data = pd.read_csv('seoul_population.csv')
    return data

# 데이터 로드
try:
    data = load_data()
except FileNotFoundError:
    st.error("데이터 파일을 찾을 수 없습니다. 올바른 파일 경로를 확인하세요.")
    st.stop()

# 데이터 확인
st.write("### 데이터 미리보기")
st.write(data.head())

# 사용자 입력: 자치구 선택
districts = sorted(data['자치구'].unique())
selected_district = st.selectbox('확인할 자치구를 선택하세요:', districts)

# 사용자 입력: 년도 선택
years = sorted(data['년도'].unique())
selected_years = st.slider('확인할 년도 범위를 선택하세요:', min_value=min(years), max_value=max(years), value=(min(years), max(years)))

# 데이터 필터링
filtered_data = data[(data['자치구'] == selected_district) & (data['년도'] >= selected_years[0]) & (data['년도'] <= selected_years[1])]

# 시각화
st.write(f"### {selected_district}의 인구수 변화 ({selected_years[0]}년 ~ {selected_years[1]}년)")
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(filtered_data['년도'], filtered_data['인구수'], marker='o')
ax.set_xlabel('년도')
ax.set_ylabel('인구수')
ax.set_title(f'{selected_district}의 인구수 변화')
ax.grid(True)
st.pyplot(fig)
