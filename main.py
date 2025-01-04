import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM

# 제목 및 설명 추가
st.title('서울 자치구별 개발 정도 시각화 및 예측')
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
grouped_data = data.groupby(['년도', '자치구']).agg({'개발점수': 'sum'}).reset_index()

# 데이터 필터링
filtered_data = grouped_data[(grouped_data['자치구'].isin(selected_districts)) & 
                              (grouped_data['년도'] >= selected_years[0]) & 
                              (grouped_data['년도'] <= selected_years[1])]

# 시각화: 개발 점수만 표시
st.write(f"### 선택한 자치구의 개발 점수 변화 ({selected_years[0]}년 ~ {selected_years[1]}년)")
fig = go.Figure()

for district in selected_districts:
    district_data = filtered_data[filtered_data['자치구'] == district]
    fig.add_trace(go.Scatter(x=district_data['년도'], y=district_data['개발점수'], mode='lines+markers', name=f'{district} 개발점수'))

fig.update_layout(title='개발 점수 변화', xaxis_title='년도', yaxis_title='개발점수', legend_title='자치구')
st.plotly_chart(fig)

# 딥러닝 기반 예측 모델 추가 (LSTM)
st.write("### 향후 10년 개발 점수 예측 (딥러닝 기반)")
forecast_fig = go.Figure()

for district in selected_districts:
    district_data = filtered_data[filtered_data['자치구'] == district]['개발점수'].values

    # 데이터 전처리
    data_scaled = (district_data - np.min(district_data)) / (np.max(district_data) - np.min(district_data))
    X = []
    y = []
    for i in range(len(data_scaled) - 1):
        X.append(data_scaled[i])
        y.append(data_scaled[i + 1])
    X = np.array(X).reshape(-1, 1, 1)
    y = np.array(y)

    # LSTM 모델 정의
    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=(1, 1)))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')

    # 모델 학습
    model.fit(X, y, epochs=50, batch_size=1, verbose=0)

    # 예측
    predictions = []
    current_input = X[-1]
    for _ in range(10):
        pred = model.predict(current_input.reshape(1, 1, 1))
        predictions.append(pred[0][0])
        current_input = pred

    # 스케일 복원
    predictions = np.array(predictions) * (np.max(district_data) - np.min(district_data)) + np.min(district_data)
    future_years = list(range(selected_years[1] + 1, selected_years[1] + 11))
    forecast_fig.add_trace(go.Scatter(x=future_years, y=predictions, mode='lines+markers', name=f'{district} 개발점수 예측'))

forecast_fig.update_layout(title='향후 10년 개발 점수 예측', xaxis_title='년도', yaxis_title='개발점수', legend_title='자치구')
st.plotly_chart(forecast_fig)
