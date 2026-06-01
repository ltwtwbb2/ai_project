import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

st.set_page_config(
    page_title="서울 기온 분석 및 미래 예측",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 서울 기온 분석 및 미래 예측")

# ----------------------------------
# 데이터 불러오기
# ----------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("seoul.csv", encoding="cp949")

    df.columns = df.columns.str.strip()

    df["날짜"] = pd.to_datetime(df["날짜"])

    df["연도"] = df["날짜"].dt.year
    df["월"] = df["날짜"].dt.month
    df["일"] = df["날짜"].dt.day

    return df

df = load_data()

# ----------------------------------
# 날짜 선택
# ----------------------------------
st.header("날짜 선택")

col1, col2 = st.columns(2)

with col1:
    month = st.selectbox(
        "월",
        range(1, 13)
    )

days_in_month = {
    1:31, 2:29, 3:31, 4:30,
    5:31, 6:30, 7:31, 8:31,
    9:30, 10:31, 11:30, 12:31
}

with col2:
    day = st.selectbox(
        "일",
        range(1, days_in_month[month] + 1)
    )

# ----------------------------------
# 해당 날짜 데이터
# ----------------------------------
selected = df[
    (df["월"] == month) &
    (df["일"] == day)
].copy()

selected = selected.sort_values("연도")

selected = selected.dropna(
    subset=["최고기온(℃)", "최저기온(℃)"]
)

# ----------------------------------
# 그래프
# ----------------------------------
st.header(f"{month}월 {day}일 연도별 기온")

if len(selected) == 0:
    st.error("데이터가 없습니다.")
    st.stop()

fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(
    selected["연도"],
    selected["최고기온(℃)"],
    color="hotpink",
    linewidth=2,
    label="최고기온"
)

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
ax.legend()
ax.grid(True, alpha=0.3)

st.pyplot(fig)

# ----------------------------------
# 미래 예측
# ----------------------------------
st.header("🔮 미래 기온 예측")

last_year = int(selected["연도"].max())

future_year = st.number_input(
    "예측할 미래 연도",
    min_value=last_year + 1,
    value=2030,
    step=1
)

# 학습 데이터
X = selected["연도"].values.reshape(-1, 1)

y_max = selected["최고기온(℃)"].values
y_min = selected["최저기온(℃)"].values

# 최고기온 모델
max_model = LinearRegression()
max_model.fit(X, y_max)

# 최저기온 모델
min_model = LinearRegression()
min_model.fit(X, y_min)

# 예측
future_X = np.array([[future_year]])

pred_max = max_model.predict(future_X)[0]
pred_min = min_model.predict(future_X)[0]

st.subheader(f"📅 {future_year}년 {month}월 {day}일 예측")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "예상 최고기온",
        f"{pred_max:.1f}℃"
    )

with col2:
    st.metric(
        "예상 최저기온",
        f"{pred_min:.1f}℃"
    )

# ----------------------------------
# 예측 그래프
# ----------------------------------
graph_data = selected.copy()

future_row = pd.DataFrame({
    "연도": [future_year],
    "최고기온(℃)": [pred_max],
    "최저기온(℃)": [pred_min]
})

graph_data = pd.concat(
    [graph_data, future_row],
    ignore_index=True
)

fig2, ax2 = plt.subplots(figsize=(12, 6))

ax2.plot(
    graph_data["연도"],
    graph_data["최고기온(℃)"],
    color="hotpink",
    linewidth=2,
    label="최고기온"
)

ax2.plot(
    graph_data["연도"],
    graph_data["최저기온(℃)"],
    color="lightskyblue",
    linewidth=2,
    label="최저기온"
)

# 예측점 강조
ax2.scatter(
    future_year,
    pred_max,
    s=120,
    color="red",
    zorder=5
)

ax2.scatter(
    future_year,
    pred_min,
    s=120,
    color="blue",
    zorder=5
)

ax2.set_title(
    f"{future_year}년 {month}월 {day}일 기온 예측"
)

ax2.set_xlabel("연도")
ax2.set_ylabel("기온(℃)")
ax2.legend()
ax2.grid(True, alpha=0.3)

st.pyplot(fig2)

# ----------------------------------
# 데이터 표시
# ----------------------------------
with st.expander("데이터 보기"):
    st.dataframe(
        selected[
            ["연도", "최고기온(℃)", "최저기온(℃)"]
        ],
        use_container_width=True
    )
