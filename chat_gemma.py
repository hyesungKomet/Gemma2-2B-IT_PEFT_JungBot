import streamlit as st
from dotenv import load_dotenv
import os
import torch
from huggingface_hub import login
from gemma_bot import JungBot

# 환경 변수 파일 로드
load_dotenv()

# 세션 초기화 버튼 추가 (디버깅용)
if st.button("세션 초기화"):
    st.session_state.clear()
    st.write("세션 초기화됨")

# 세션 상태에 토큰이 없으면 입력 필드 표시
if "hf_token" not in st.session_state:
    hf_token = st.text_input("Hugging Face Token", type="password")
    if hf_token:
        st.session_state.hf_token = hf_token
        login(token=hf_token)
        st.success("Logged in successfully!")
else:
    # 세션 상태에 토큰이 있으면 사용
    hf_token = st.session_state.hf_token
    login(token=hf_token)

def save_chat(user_input, model_output):
    st.session_state.chat_history.append({'user': user_input, 'model': model_output})

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    st.write('chat_history loaded!')

if "model" not in st.session_state:
    st.session_state.model = JungBot(modelName='google/gemma-2-2b-it')
    st.write('Gemma Model loaded into session state!')

print('gemma model loaded!')

st.title("💬 Jung Bot - Talk to AI mentalist!")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Feel free to talk to me!"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

prompt = st.chat_input("여기에 입력해주세요!")

if prompt:
    print('prompt: ', prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 사용자 입력 전처리
    clean_prompt = prompt.strip().lower().rstrip('.')

    response = st.session_state.model.inference(clean_prompt, st.session_state.chat_history)
    print('response: ', response)
    if response == 0:
        save_chat(prompt, response)
        st.success('Chat report saved successfully.')
        st.stop()
    else:
        msg = response if response else 'No response from the model'

    # 응답 후처리 및 줄바꿈 처리
    msg = msg.replace('\n', '\n\n').strip()  # 두 줄 띄우기 추가
    st.session_state.messages.append({"role": "assistant", "content": msg})

    st.chat_message("assistant").write(msg)