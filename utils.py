import os
import time
import warnings

warnings.filterwarnings("ignore")

# --- AYARLAR ---
USE_LOCAL_LLM = True
def load_api_key():
    try:
        if os.path.exists("api_key.txt"):
            with open("api_key.txt", "r", encoding="utf-8") as f:
                return f.read().strip()
    except Exception as e:
        print(f"Key Okuma Hatası: {e}")
    return None

API_KEY = load_api_key()

pipe = None
model = None

# --- 3 model senaryosu local-api key-mock llm ---
if USE_LOCAL_LLM:
    try:
        from transformers import pipeline
        print("Local Model (Qwen-0.5B) RAM'e yükleniyor...")
        
        pipe = pipeline(
            "text-generation",
            model="Qwen/Qwen1.5-0.5B-Chat",
            model_kwargs={"low_cpu_mem_usage": True},
            device_map="auto"
        )
        print("Local Model Hazır!")
    except Exception as e:
        print(f"Local Model Yüklenemedi: {e}")
        print("Otomatik olarak diğer modlara geçilecek.")

else:
    try:
        if API_KEY and API_KEY != "":
            import google.generativeai as genai
            genai.configure(api_key=API_KEY)
            model = genai.GenerativeModel('models/gemini-flash-latest')
            print("Google Gemini API Bağlandı!")
        else:
            print("ℹAPI Key yok, Mock modunda çalışacak.")
    except Exception as e:
        print(f"Gemini Hatası: {e}")


def get_llm_response(gesture_name):
    
    if USE_LOCAL_LLM and pipe:
        try:
            # ----- Messages to LLM -----
            messages = []

            
            prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            outputs = pipe(prompt, max_new_tokens=40, do_sample=True, temperature=0.7)
            
            response = outputs[0]["generated_text"].split("assistant")[-1].strip()
            print(f"Local: {response}")
            return f"Local: {response}"
            
        except Exception as e:
            return f"Local Hata: {e}"

    elif model:
        try:
            # ----- Messages to LLM -----


        except Exception as e:
            print(f"hata: {e}")
            return get_mock_response(gesture_name)

    else:
        return get_mock_response(gesture_name)

def get_mock_response(gesture_name):
    # ----- MOCK LLM LOGIC -----
    mock_responses = {}

    return mock_responses.get(gesture_name, "Mock: ...")


def count_fingers(hand_landmarks):
    tip_ids = [8, 12, 16, 20]
    # ----- COUNT FINGERS LOGIC -----


    
    return " "
