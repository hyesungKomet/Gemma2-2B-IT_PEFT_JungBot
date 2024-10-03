# Gemma2-2B-IT_PEFT_JungBot
Google Machine Learning Bootcamp Gemma Sprint

## Description
This project aims to provide psychological counseling as if receiving advice from renowned psychologist, Carl Jung by finetuning the Gemma model(gemma2-2b-it) on mental health 
counseling conversations and the works of these psychology experts.
- **Base Model:** gemma2-2b-it  
- **Supported Language:** Korean

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/hyesungKomet/Gemma2-2B-IT_PEFT_JungBot.git
   ```
2. Move to the project directory:
   ```bash
   cd Gemma2-2B-IT_PEFT_JungBot
   ```
3. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Streamlit app:
   ```bash
   streamlit run chat_gemma.py
   ```
5. Enter the Huggingface token in the Streamlit web interface and start counseling with the chatbot.

## Dataset
### 1. Wellness Conversation Scripts
We utilized user-chatbot conversation scripts from the counseling dataset available on AiHub.  
Dataset source: [AiHub - Wellness Conversation Scripts](https://aihub.or.kr/aihubdata/data/view.do?currMenu=120&topMenu=100&aihubDataSe=extrldata&dataSetSn=267)

### 2. GPT-Generated Dataset
We modified the chatbot responses in the Wellness Conversation Scripts using GPT. The responses were revised based on Carl Jung's analytical psychology, incorporating his research and beliefs.

### 3. Chatbot_data (Planned)
We plan to fine-tune the model using the artificially created chatbot dataset from the [Chatbot_data repository](https://github.com/songys/Chatbot_data), aiming to make Korean language conversations more natural.
