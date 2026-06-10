import streamlit as st
import pandas as pd
import plotly.graph_objects as go  # <-- 오타 수정 완료!

# 1. 페이지 설정
st.set_page_config(
    page_title="원신 나선비경 픽률 대시보드",
    page_icon="⚔️",
    layout="wide"
)

st.title("⚔️ 원신 나선비경 캐릭터 픽률 통계")
st.markdown("나선비경에서 자주 사용되는 캐릭터들의 픽률을 확인하고 비교할 수 있습니다.")

# 2. 데이터 준비 (CSV 파일이 없을 경우 기본 데이터를 자동 생성)
@st.cache_data
def load_abyss_data():
    csv_filename = "genshin_abyss_mbti.csv" # 데이터 보관용 파일명
    
    try:
        df = pd.read_csv(csv_filename)
    except FileNotFoundError:
        # 공월의 노래 여섯 번째 달(5.6 버전) 시점의 최신 주요 캐릭터 및 가상 픽률 데이터 확장
        mock_data = {
            "Character": [
                "푸리나", "나히다", "종려", "카즈하", "느비예트", "야란", "백출", "알하이탐", 
                "실버린", "마비카", "실로닌", "키니치", "말라니", "차스카", "올로룬", "시틀라리",
                "라이덴", "아를레키노", "베넷", "시노부", "닐루", "행추", "향릉", "피슬", 
                "타르탈리아", "리니", "나비아", "클로린드", "에밀리에", "설탕"
            ],
            "PickRate": [
                86.4, 83.1, 79.5, 76.2, 74.8, 69.1, 65.3, 62.0,
                60.5, 58.7, 56.4, 52.1, 49.8, 46.2, 43.5, 41.2,
                40.8, 39.5, 38.2, 36.4, 34.1, 31.5, 28.3, 22.4,
                19.8, 17.5, 15.2, 13.6, 11.4, 8.5
            ]
        }
        df = pd.DataFrame(mock_data)
        df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
    
    # 픽률 기준 내림차순 정렬 재확인
    df = df.sort_values(by="PickRate", ascending=False).reset_index(drop=True)
    return df

df = load_abyss_data()
character_list = df["Character"].tolist()

# 3. 사이드바 설정
st.sidebar.header("🎯 캐릭터 선택")
# 기본 선택을 '닐루'로 시도하고, 없으면 첫 번째 캐릭터 선택
default_char_idx = character_list.index("닐루") if "닐루" in character_list else 0
selected_char = st.sidebar.selectbox("픽률을 확인할 캐릭터를 선택하세요:", character_list, index=default_char_idx)

# 4. 선택된 캐릭터 정보 추출 및 순위 계산
char_row = df[df["Character"] == selected_char].iloc[0]
char_pick_rate = char_row["PickRate"]
char_rank = df[df["Character"] == selected_char].index[0] + 1

# 5. 화면 레이아웃 배치
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📊 선택된 캐릭터 정보")
    # 대형 카드 형태로 픽률 표기
    st.metric(label=f"✨ {selected_char} 나선비경 픽률", value=f"{char_pick_rate:.1f}%")
    st.info(f"🏆 전체 캐릭터 중 **{char_rank}등**입니다.")
    
    # 미니 순위표
    st.markdown("**🔝 나선비경 픽률 전체 순위**")
    display_df = df.copy()
    display_df.index = display_df.index + 1
    display_df.columns = ["캐릭터 이름", "픽률 (%)"]
    st.dataframe(display_df, use_container_width=True)

with col2:
    st.subheader("📈 캐릭터별 픽률 비교 차트")
    
    # 초록색 그라데이션 적용 (1등이 가장 진하고 아래로 갈수록 흐려짐)
    total_count = len(df)
    colors = []
    for i in range(total_count):
        # 1등(index 0)은 선명한 초록색, 마지막 등수는 연한 초록색
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
    
    # 그래프 내부 디자인 조정
    fig.update_layout(
        title=f"<b>전체 캐릭터 픽률 순위 (현재 선택: {selected_char})</b>",
        title_font_size=16,
        xaxis=dict(title="캐릭터", tickfont_size=12),
        yaxis=dict(title="픽률 (%)", range=[0, 100]), # 픽률 최댓값 100% 고정
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=50, b=20)
    )
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(200, 200, 200, 0.3)')
    
    st.plotly_chart(fig, use_container_width=True)
