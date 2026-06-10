import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. 페이지 설정
st.set_page_config(
    page_title="원신 나선비경 픽률 도감",
    page_icon="⚔️",
    layout="wide"
)

st.title("⚔️ 원신 나선비경 캐릭터 픽률 & 도감")
st.markdown("캐릭터를 선택하면 나선비경 픽률과 캐릭터 도감 이미지를 함께 확인할 수 있습니다.")

# 2. 데이터 및 캐릭터 이미지 URL 준비
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

# 캐릭터별 도감 이미지 URL 딕셔너리 (원신 공식 위키 등의 이미지 주소 예시)
# 이미지가 정상적으로 나오게 하려면 실제 접근 가능한 이미지 URL 경로를 입력해야 합니다.
# 여기서는 예시 URL을 넣었으며, 원하시는 이미지 링크가 있다면 아래 주소를 수정하시면 됩니다.
CHARACTER_IMAGES = {
    "닐루": "https://images.unsplash.com/photo-1578632767115-351597cf2477?w=400", # 임시 대체 이미지 예시
    "푸리나": "https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?w=400",
    "나히다": "https://images.unsplash.com/photo-1560942485-b2a11cc13456?w=400",
    "종려": "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=400",
    "카즈하": "https://images.unsplash.com/photo-1541701494587-cb58502866ab?w=400",
}
# 이미지 딕셔너리에 없는 캐릭터는 기본 이미지 처리
DEFAULT_IMAGE = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=400"


# 3. 사이드바 설정 - 캐릭터 선택
st.sidebar.header("🎯 캐릭터 선택")
default_char_idx = character_list.index("닐루") if "닐루" in character_list else 0
selected_char = st.sidebar.selectbox("정보를 확인할 캐릭터를 선택하세요:", character_list, index=default_char_idx)


# 4. 선택된 캐릭터 정보 추출
char_row = df[df["Character"] == selected_char].iloc[0]
char_pick_rate = char_row["PickRate"]
char_rank = df[df["Character"] == selected_char].index[0] + 1


# 5. 화면 배치 (좌측: 도감 이미지 및 정보 / 우측: 전체 순위 비교 차트)
col1, col2 = st.columns([1.2, 2])

with col1:
    st.subheader(f"✨ {selected_char} 상세 정보")
    
    # 캐릭터 도감 이미지 표시 기능
    img_url = CHARACTER_IMAGES.get(selected_char, DEFAULT_IMAGE)
    st.image(img_url, caption=f"원신 도감 - {selected_char}", use_container_width=True)
    
    # 픽률 및 순위 카드
    st.metric(label="나선비경 픽률", value=f"{char_pick_rate:.1f}%")
    st.success(f"🏆 현재 나선비경 전체 **{char_rank}등**")

with col2:
    st.subheader("📈 캐릭터별 픽률 비교")
    
    # 초록색 그라데이션 적용 (선택된 캐릭터를 쉽게 알아볼 수 있도록 전체 그래프도 표시)
    total_count = len(df)
    colors = []
    for i in range(total_count):
        # 현재 선택된 캐릭터의 막대는 좀 더 강조된 진한 초록색, 나머지는 일반 초록색 그라데이션
        if df.loc[i, "Character"] == selected_char:
            colors.append("rgba(0, 100, 0, 1.0)") # 강조용 아주 진한 초록색 (DarkGreen)
        else:
            opacity = 1.0 - (i * (0.8 / (total_count - 1 if total_count > 1 else 1)))
            colors.append(f"rgba(46, 139, 87, {opacity})") # SeaGreen 계열
        
    # Plotly 시각화
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df["Character"],
        y=df["PickRate"],
        marker_color=colors,
        text=[f"{val:.1f}%" for val in df["PickRate"]],
        textposition='outside',
        hoverinfo='x+y'
    ))
    
    fig.update_layout(
        title=f"<b>전체 캐릭터 픽률 순위 (현재 강조: {selected_char})</b>",
        title_font_size=16,
        xaxis=dict(title="캐릭터", tickfont_size=12),
        yaxis=dict(title="픽률 (%)", range=[0, 100]),
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=50, b=20)
    )
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(200, 200, 200, 0.3)')
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 미니 테이블 리스트
    st.markdown("**🔝전체 캐릭터 순위표**")
    display_df = df.copy()
    display_df.index = display_df.index + 1
    display_df.columns = ["캐릭터 이름", "픽률 (%)"]
    st.dataframe(display_df, use_container_width=True)
