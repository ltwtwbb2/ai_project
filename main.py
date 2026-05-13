import streamlit as st
st.title('나의 첫 웹 사이트 만들기!')
a=st.text_input('이름을 입력하세요')
b=st.selectbox('좋아하는 음식을 선택하세요',['치킨','스테이크','햄버거'])
if st.button('인사말 생성'):
  st.write(a+'님! 안녕하세요')
st.info('반갑습니다')
st.warning(b+'좋아하시는군요!')
st.error('잘 지내봐요!!')
st.balloons()
