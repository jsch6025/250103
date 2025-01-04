import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 폰트 설정
plt.rc('font', family='Malgun Gothic')  # 한글 폰트 설정
plt.rc('axes', unicode_minus=False)  # 마이너스 기호 깨짐 방지

# 제목 및 설명 추가
st.title('Population Trends by District in Seoul')
st.write('Visualize the population trends of districts in Seoul over the past 30 years.')

# 데이터 불러오기
@st.cache_data
def load_data():
    data = pd.read_csv('seoul_population.csv')
    return data

# 데이터 로드
try:
    data = load_data()
except FileNotFoundError:
    st.error("Data file not found. Please check the file path.")
    st.stop()

# 데이터 확인
st.write("### Preview of Data")
st.write(data.head())

# 사용자 입력: 자치구 선택
districts = sorted(data['자치구'].unique())
selected_districts = st.multiselect('Select District(s):', districts, default=[districts[0]])

# 사용자 입력: 년도 선택
years = sorted(data['년도'].unique())
selected_years = st.slider('Select Year Range:', min_value=min(years), max_value=max(years), value=(min(years), max(years)))

# 데이터 필터링
filtered_data = data[(data['자치구'].isin(selected_districts)) & (data['년도'] >= selected_years[0]) & (data['년도'] <= selected_years[1])]

# 시각화
st.write(f"### Population Trends of Selected Districts ({selected_years[0]} - {selected_years[1]})")
fig, ax = plt.subplots(figsize=(10, 6))
for district in selected_districts:
    district_data = filtered_data[filtered_data['자치구'] == district]
    ax.plot(district_data['년도'], district_data['인구수'], marker='o', label=district)
ax.set_xlabel('Year')
ax.set_ylabel('Population')
ax.set_title('Population Trends by District')
ax.legend()
ax.grid(True)
st.pyplot(fig)
