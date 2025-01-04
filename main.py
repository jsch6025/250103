import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 제목 및 설명 추가
st.title('Streamlit 데이터 분석 대시보드')
st.write('업로드한 CSV 파일의 데이터를 탐색하고 시각화합니다.')

# 파일 업로드 기능
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요.", type=['csv'])

if uploaded_file is not None:
    # 데이터 로드
    data = pd.read_csv(uploaded_file)
    st.write("### 데이터 미리보기:")
    st.write(data.head())

    # 데이터 정보 출력
    st.write("### 데이터 요약 정보:")
    st.write(data.describe())

    # 컬럼 선택
    st.write("### 컬럼 선택:")
    column = st.selectbox('분석할 컬럼을 선택하세요:', data.columns)

    # 히스토그램 시각화
    st.write(f"### {column} 컬럼의 히스토그램")
    fig, ax = plt.subplots()
    sns.histplot(data[column], kde=True, ax=ax)
    st.pyplot(fig)

    # 상관 행렬 출력
    st.write("### 상관 행렬:")
    corr = data.corr()
    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', ax=ax)
    st.pyplot(fig)

    # 사용자 입력: 데이터 필터링 예제
    st.write("### 필터링 예제:")
    filter_value = st.slider(f'{column} 값 필터링:', float(data[column].min()), float(data[column].max()))
    filtered_data = data[data[column] > filter_value]
    st.write(filtered_data)

else:
    st.write("파일을 업로드하면 데이터가 표시됩니다.")
