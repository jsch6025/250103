import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 제목 및 설명 추가
st.title('서울 자치구별 개발 정도 시각화')
st.write('서울시 자치구의 개발 정도를 다양한 지표로 수치화하고 시각화합니다.')

# 데이터 불러오기
@st.cache_data
def load_data():
    data = pd.read_csv('seoul_population_age_schools.csv')
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

# 사용자 입력: 시각화 항목 선택
options = st.multiselect('시각화 항목 선택:', ['개발점수', '학교수', '인구밀도'], default=['개발점수', '학교수', '인구밀도'])

# 자치구별 면적 데이터 (단위: km²)
area_data = {
    '종로구': 23.91, '중구': 9.96, '용산구': 21.87, '성동구': 16.85, '광진구': 17.06,
    '동대문구': 14.22, '중랑구': 18.50, '성북구': 24.57, '강북구': 23.60, '도봉구': 20.70,
    '노원구': 35.44, '은평구': 29.70, '서대문구': 17.61, '마포구': 23.85, '양천구': 17.41,
    '강서구': 41.42, '구로구': 20.11, '금천구': 13.00, '영등포구': 24.56, '동작구': 16.35,
    '관악구': 29.57, '서초구': 47.00, '강남구': 39.55, '송파구': 33.89, '강동구': 24.59
}

# 인구 밀도 및 개발 점수 계산
# 면적 및 인구 밀도 계산
data['면적'] = data['자치구'].map(area_data)
data['인구밀도'] = data['인구수'] / data['면적']

# 가중치 조정
data['가중치'] = 1/50
is_60s = data['나이대'] == '60대 이상'
data.loc[is_60s, '가중치'] = 1/100

# 20~40대 가중치 증가
is_20s_40s = data['나이대'].isin(['20대', '30대', '40대'])
data.loc[is_20s_40s, '가중치'] = 1/25

# 개발 점수 계산
data['개발점수'] = (data['인구밀도'] * data['가중치']) + (data['학교수'] * 0.8)

# 데이터 그룹화 (년도와 자치구 기준으로 합산)
grouped_data = data.groupby(['년도', '자치구']).agg({'개발점수': 'sum', '학교수': 'sum', '인구밀도': 'mean'}).reset_index()

# 데이터 필터링
filtered_data = grouped_data[(grouped_data['자치구'].isin(selected_districts)) & 
                              (grouped_data['년도'] >= selected_years[0]) & 
                              (grouped_data['년도'] <= selected_years[1])]

# 시각화: 선택한 항목만 표시
st.write(f"### 선택한 자치구의 선택 항목 변화 ({selected_years[0]}년 ~ {selected_years[1]}년)")
fig = go.Figure()

for district in selected_districts:
    district_data = filtered_data[filtered_data['자치구'] == district]
    if '개발점수' in options:
        fig.add_trace(go.Scatter(x=district_data['년도'], y=district_data['개발점수'], mode='lines+markers', name=f'{district} 개발점수'))
    if '학교수' in options:
        fig.add_trace(go.Scatter(x=district_data['년도'], y=district_data['학교수'], mode='lines+markers', name=f'{district} 학교수'))
    if '인구밀도' in options:
        fig.add_trace(go.Scatter(x=district_data['년도'], y=district_data['인구밀도'], mode='lines+markers', name=f'{district} 인구밀도'))

fig.update_layout(title='선택 항목 변화', xaxis_title='년도', yaxis_title='값', legend_title='항목')
st.plotly_chart(fig)
