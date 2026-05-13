import streamlit as st
st.title('나의 첫 웹 사이트 만들기!')
st.text_input('이름을 입력하세요')
st.selectbox('좋아하는 음식을 선택하세요',['치킨','스테이크','햄버거'])
st.button('인사말 생성')
