import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. 페이지 설정
st.set_page_config(
    page_title="원신 나선비경 픽률 통계",
    page_icon="⚔️",
    layout="wide"
)

st.title("⚔️ 원신 나선비경 캐릭터 픽률 통계")
st.markdown("캐릭터를 선택하면 해당 캐릭터의 나선비경 픽률과 순위를 정확하게 확인할 수 있습니다.")

# 2. 데이터 준비
@st.cache_data
def load_abyss_data():
    csv_filename = "genshin_abyss_mbti.csv"
    
    try:
        df = pd.read_csv(csv_filename)
    except FileNotFoundError:
        # 기본 캐릭터 데이터 (픽률 기준 내림차순)
        mock_data = {
            "Character": ["푸리나", "나히다", "종려", "카즈하", "느비예트", "야란", "베넷", "시노부", "닐루", "라이덴", "행추", "향릉", "알하이탐", "백출", "피슬", "설탕"],
            "PickRate": [84.5, 81.2, 78.9, 75.4, 72.1, 68.5, 55.4, 48.2, 42.5, 41.8, 38.2, 35.0, 31.2, 28.5, 20.1, 12.4]
        }
        df = pd.DataFrame(mock_data)
        df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
    
    df = df.sort_values(by="PickRate", ascending=False).reset_index(drop=True)
    return df

df = load_abyss_data()
character_list = df["Character"].tolist()

# 3. 사이드바 설정 - 캐릭터 선택
st.sidebar.header("🎯 캐릭터 선택")
default_char_idx = character_list.index("닐루") if "닐루" in character_list else 0
selected_char = st.sidebar.selectbox("정보를 확인할 캐릭터를 선택하세요:", character_list, index=default_char_idx)

# 4. 선택된 캐릭터 정보 추출
char_row = df[df["Character"] == selected_char].iloc[0]
char_pick_rate = char_row["PickRate"]
char_rank = df[df["Character"] == selected_char].index[0] + 1

# 5. 화면 배치 (좌측: 선택된 캐릭터 단독 지표 / 우측: 전체 비교 그래프)
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader(f"✨ {selected_char} 분석 결과")
    
    # 선택된 캐릭터의 픽률과 순위만 대형 카드로 직관적으로 표시
    st.metric(label="나선비경 픽률", value=f"{char_pick_rate:.1f}%")
    st.success(f"🏆 현재 나선비경 전체 **{char_rank}등** (총 {len(df)}명 중)")
    
    # 깔끔한 미니 순위표 제공
    st.markdown("---")
    st.markdown("**🔝 전체 캐릭터 순위 리스트**")
    display_df = df.copy()
    display_df.index = display_df.index + 1
    display_df.columns = ["캐릭터 이름", "픽률 (%)"]
    st.dataframe(display_df, use_container_width=True)

with col2:
    st.subheader("📈 캐릭터별 픽률 비교 차트")
    
    # 초록색 그라데이션 적용 (현재 선택된 캐릭터만 진하게 강조)
    total_count = len(df)
    colors = []
    for i in range(total_count):
        if df.loc[i, "Character"] == selected_char:
            colors.append("rgba(0, 100, 0, 1.0)")  # 선택된 캐릭터: 강조용 진한 초록색 (DarkGreen)
        else:
            opacity = 1.0 - (i * (0.8 / (total_count - 1 if total_count > 1 else 1)))
            colors.append(f"rgba(46, 139, 87, {opacity})")  # 나머지: SeaGreen 계열 그라데이션
        
    # Plotly 막대그래프 시각화
    fig = go.Figure()
    fig.add_trace(go.Bar(
