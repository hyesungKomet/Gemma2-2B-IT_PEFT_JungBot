import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel, PeftConfig

class JungBot:
    def __init__(self, modelName="google/gemma-2-2b-it", lora_weights_path="skhoon4u/jung2"):
        self.modelName = modelName
        self.lora_weights_path = lora_weights_path
        self.template = """
            대화 기록: {chat_history}
            <start_of_turn>user
            {user}<end_of_turn>
            <start_of_turn>model
            {response}<end_of_turn>
            """
        self.tokenizer, self.model = self.load_model()

    def postprocess_output(self, output_text):
        # 반복 제거 및 줄바꿈 간소화
        lines = output_text.split('. ')
        unique_lines = []
        for line in lines:
            if line not in unique_lines and len(line.strip()) > 1:  # 줄바꿈과 중복 제거
                unique_lines.append(line.strip())
        cleaned_text = '. '.join(unique_lines)  # 줄바꿈 대신 문장 간 간격을 최소화
        return cleaned_text.strip()

    def load_model(self):
        model = AutoModelForCausalLM.from_pretrained(
            self.modelName,
            device_map="cpu",
        )

        tokenizer = AutoTokenizer.from_pretrained(self.modelName)

        if self.lora_weights_path:
            peft_config = PeftConfig.from_pretrained(self.lora_weights_path)
            model = PeftModel.from_pretrained(model, self.lora_weights_path)
            print('Lora Adaptor loaded!')

        print("Tokenizer vocab size:", tokenizer.vocab_size)
        return tokenizer, model
    
    def inference(self, input_text, chat_history):
        clean_input = input_text.strip().lower().rstrip('.')

        if clean_input in ['종료', '안녕', '바이']:
            print("Chat end trigger")
            return 0
        
        prompt = self.template.format(
            chat_history=chat_history, 
            user=clean_input,
            response="다음은 당신의 심리상담사가 된 심리학자 칼 융이 두 문장으로 간략하게 입력한 상황에 대해 제공하는 답변입니다:")
        inputs = self.tokenizer(
            prompt, 
            return_tensors="pt",
        )

        with torch.no_grad():
            output = self.model.generate(
                inputs.input_ids.to('cpu'), 
                attention_mask=inputs.attention_mask.to('cpu'),  
                max_length=512,
                num_return_sequences=1,
                do_sample=True,
                no_repeat_ngram_size=4,
                top_k=40,
                top_p=0.85,
                temperature=0.7
            )

        generated_text = self.tokenizer.decode(output[0], skip_special_tokens=True)
        generated_text = self.postprocess_output(generated_text)
        generated_text = self.clean_generated_text(generated_text)
        generated_text = self.filter_output(generated_text)
        return generated_text
    
    def clean_generated_text(self, text):
        # "대화 기록", "user", "model" 등의 태그와 불필요한 줄 제거
        text = text.replace('대화 기록:', '').strip()
        text = text.replace('<start_of_turn>user', '').strip()
        text = text.replace('<start_of_turn>model', '').strip()
        text = text.replace('<end_of_turn>', '').strip()

        # 빈 줄과 불필요한 공백을 제거
        lines = [line.strip() for line in text.split('\n') if line.strip()]  
        return ' '.join(lines) 
    
    def filter_output(self, output_text):
        # 'user'와 'model' 사이의 모든 텍스트 제거
        if "model" in output_text:
            output_text = output_text.split("model")[-1].strip()
 
        if "다음은 당신의 심리상담사가 된 심리학자 칼 융이 두 문장으로 간략하게 입력한 상황에 대해 제공하는 답변입니다:" in output_text:
            output_text = output_text.split("다음은 당신의 심리상담사가 된 심리학자 칼 융이 두 문장으로 간략하게 입력한 상황에 대해 제공하는 답변입니다:")[-1].strip()
        
        # 문장 끝에 적절한 줄바꿈 추가
        sentences = output_text.split(". ")  
        formatted_text = ".\n".join(sentences)  

        return formatted_text.strip()