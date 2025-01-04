import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 제목 및 설명 추가
st.title('시대별 서울 자치구 별 인구수 대시보드')
st.write('서울시 자치구의 시대별 인구수를 탐색하고 시각화합니다.')

# 파일 업로드 기능
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요.", type=['csv'])

if uploaded_file is not None:
    # 데이터 로드
    data = pd.read_csv(uploaded_file)

    # 데이터 확인
    st.write("### 데이터 미리보기:")
    st.write(data.head())

    # 사용자 입력: 년도 선택
    years = sorted(data['년도'].unique())
    selected_year = st.selectbox('확인할 연도를 선택하세요:', years)

    # 사용자 입력: 자치구 선택
    districts = sorted(data['자치구'].unique())
    selected_district = st.selectbox('확인할 자치구를 선택하세요:', districts)

    # 선택한 데이터 필터링
    filtered_data = data[(data['년도'] == selected_year) & (data['자치구'] == selected_district)]

    # 결과 표시
    st.write(f"### {selected_year}년 {selected_district}의 인구수")
    st.write(filtered_data)

    # 시각화
    st.write("### 자치구 별 인구수 변화 시각화")
    fig, ax = plt.subplots(figsize=(10, 6))
    for district in districts:
        district_data = data[data['자치구'] == district]
        ax.plot(district_data['년도'], district_data['인구수'], label=district)

    ax.set_xlabel('년도')
    ax.set_ylabel('인구수')
    ax.set_title('시대별 서울 자치구 별 인구수 변화')
    ax.legend(loc='upper right', fontsize='small')
    st.pyplot(fig)

else:
    st.write("파일을 업로드하면 데이터가 표시됩니다.")
