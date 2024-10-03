# Gemma2-2B-IT_PEFT_JungBot
Google Machine Learning Bootcamp Gemma Sprint

## Description
This project aims to provide psychological counseling as if receiving advice from renowned psychologist, Carl Jung by finetuning the Gemma model(gemma2-2b-it) on mental health 
counseling conversations and the works of these psychology experts.

## Instruction
You can easily run the code with `streamlit run chat_gemma.py`. 
You need to enter the Hugging Face token in terminal on the first run.

## Dataset
# 1. Wellness Conversation Scripts
We utilized user-chatbot conversation scripts from the counseling dataset available on AiHub.  
Dataset source: [AiHub - Wellness Conversation Scripts](https://aihub.or.kr/aihubdata/data/view.do?currMenu=120&topMenu=100&aihubDataSe=extrldata&dataSetSn=267)

# 2. GPT-Generated Dataset
We modified the chatbot responses in the Wellness Conversation Scripts using GPT. The responses were revised based on Carl Jung's analytical psychology, incorporating his research and beliefs.

# 3. Chatbot_data (Planned)
We plan to fine-tune the model using the artificially created chatbot dataset from the [Chatbot_data repository](https://github.com/songys/Chatbot_data), aiming to make Korean language conversations more natural.
