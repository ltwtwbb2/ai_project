import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="서울 기온 분석",
    page_icon="🌡️",
    layout="wide"
)

st.title("서울 기온 데이터 분석")

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("seoul.csv", encoding="cp949")

    # 컬럼명 공백 제거
    df.columns = df.columns.str.strip()

    # 날짜 변환
    df["날짜"] = pd.to_datetime(df["날짜"])

    # 월, 일, 연도 추출
    df["연도"] = df["날짜"].dt.year
    df["월"] = df["날짜"].dt.month
    df["일"] = df["날짜"].dt.day

    return df

df = load_data()

# ----------------------------
# 날짜 선택
# ----------------------------
col1, col2 = st.columns(2)

with col1:
    month = st.selectbox(
        "월 선택",
        list(range(1, 13)),
        index=0
    )

with col2:
    days_in_month = {
        1:31, 2:29, 3:31, 4:30,
        5:31, 6:30, 7:31, 8:31,
        9:30, 10:31, 11:30, 12:31
    }

    day = st.selectbox(
        "일 선택",
        list(range(1, days_in_month[month] + 1)),
        index=0
    )

# ----------------------------
# 선택한 날짜 데이터 추출
# ----------------------------
selected = df[
    (df["월"] == month) &
    (df["일"] == day)
].copy()

selected = selected.sort_values("연도")

# 결측 제거
selected = selected.dropna(
    subset=["최고기온(℃)", "최저기온(℃)"]
)

st.subheader(f"{month}월 {day}일의 연도별 기온 변화")

if len(selected) == 0:
    st.warning("해당 날짜의 데이터가 없습니다.")
else:

    fig, ax = plt.subplots(figsize=(12, 6))

    # 최고기온
    ax.plot(
        selected["연도"],
        selected["최고기온(℃)"],
        color="hotpink",
        linewidth=2,
        label="최고기온"
    )

    # 최저기온
    ax.plot(
        selected["연도"],
        selected["최저기온(℃)"],
        color="lightskyblue",
        linewidth=2,
        label="최저기온"
    )

    ax.set_xlabel("연도")
    ax.set_ylabel("기온(℃)")
    ax.set_title(f"{month}월 {day}일의 연도별 최고·최저기온")
    ax.grid(True, alpha=0.3)

    # 범례
    ax.legend()

    st.pyplot(fig)

    st.markdown("---")

    st.write("선택된 데이터")
    st.dataframe(
        selected[
            ["연도", "최고기온(℃)", "최저기온(℃)"]
        ],
        use_container_width=True
    )
