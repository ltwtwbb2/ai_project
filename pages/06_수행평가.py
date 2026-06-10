import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(
    page_title="원신 나선비경 캐릭터 조회",
    page_icon="⚔️",
    layout="centered"  # 캐릭터 단독 정보 조회를 위해 정렬을 중앙 집중형으로 변경
)

st.title("⚔️ 원신 나선비경 캐릭터 픽률 조회")
st.markdown("원하는 캐릭터를 선택하면 해당 캐릭터의 나선비경 픽률과 순위만 깔끔하게 확인할 수 있습니다.")

# 2. 데이터 준비 (공월의 노래 여섯 번째 달 기준 데이터)
@st.cache_data
def load_abyss_data():
    csv_filename = "genshin_abyss_mbti.csv" # 데이터 보관용 파일명
    
    try:
        df = pd.read_csv(csv_filename)
    except FileNotFoundError:
        # 5.6 버전 시점의 주요 캐릭터 및 가상 픽률 데이터셋 (픽률 기준 내림차순)
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
character_list = sorted(df["Character"].tolist())  # 사용자가 찾기 쉽도록 선택 상자는 가나다순 정렬

# 3. 본문 상단 - 캐릭터 선택 인터페이스
selected_char = st.selectbox("조회할 캐릭터를 선택하세요:", character_list, index=character_list.index("닐루") if "닐루" in character_list else 0)

# 4. 선택된 캐릭터 정보 추출 및 순위 계산
char_row = df[df["Character"] == selected_char].iloc[0]
char_pick_rate = char_row["PickRate"]
char_rank = df[df["Character"] == selected_char].index[0] + 1
total_characters = len(df)

# 5. 선택한 캐릭터에 대해서만 화면에 표시
st.markdown("---")
st.subheader("🎯 선택된 캐릭터 상세 분석")

# 깔끔한 레이아웃을 위해 좌우로 수치 지표 배치
metrics_col1, metrics_col2 = st.columns(2)

with metrics_col1:
    st.metric(label=f"✨ {selected_char} 나선비경 픽률", value=f"{char_pick_rate:.1f}%")

with metrics_col2:
    st.metric(label="🏆 나선비경 픽률 순위", value=f"{char_rank} 위", delta=f"전체 {total_characters}명 중")

# 진행 바(Progress Bar)를 활용해 픽률 시각적 표현
st.markdown("**📊 픽률 게이지**")
st.progress(char_pick_rate / 100.0)

# 안내 메시지 박스
if char_rank <= 5:
    st.success(f"🔥 **{selected_char}**은(는) 현재 최상위권 티어의 핵심 캐릭터입니다!")
elif char_rank <= 15:
    st.info(f"✅ **{selected_char}**은(는) 많은 유저들이 안정적으로 채용하는 고성능 캐릭터입니다.")
else:
    st.warning(f"💡 **{selected_char}**은(는) 특정 파티 조합이나 상황에서 활약하는 전략적 캐릭터입니다.")
