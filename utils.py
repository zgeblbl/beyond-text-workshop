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
            ##############################
            messages = [
                {"role": "system", "content": "Sen yardımsever bir robotsun. Çok kısa Türkçe cevap ver."},
                {"role": "user", "content": f"Kullanıcı '{gesture_name}' hareketi yaptı. Ne dersin?"}
            ]
            
            prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            outputs = pipe(prompt, max_new_tokens=40, do_sample=True, temperature=0.7)
            
            response = outputs[0]["generated_text"].split("assistant")[-1].strip()
            return f"Local: {response}"
            
        except Exception as e:
            return f"Local Hata: {e}"

    elif model:
        try:
            ##############################
            prompt = f"Sen robotsun. Kullanıcı '{gesture_name}' yaptı. Komik tek cümle söyle."
            response = model.generate_content(prompt)
            return f"Gemini: {response.text.strip()}"
        except Exception as e:
            return get_mock_response(gesture_name)

    else:
        return get_mock_response(gesture_name)

def get_mock_response(gesture_name):
    ##############################
    mock_responses = {
        "Yumruk (Rock)": "Mock: Güç bende!",
        "Zafer (Peace)": "Mock: Barış olsun.",
        "Selam (Hello)": "Mock: Selamlar!",
        "Isaret (Point)": "Mock: Orayı görüyorum.",
        "Bilinmiyor": "Mock: ..."
    }
    return mock_responses.get(gesture_name, "Mock: ...")


def count_fingers(hand_landmarks):
    tip_ids = [8, 12, 16, 20]
    ##############################
    count = 0
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        count += 1
    for id in tip_ids:
        if hand_landmarks.landmark[id].y < hand_landmarks.landmark[id - 2].y:
            count += 1
    return count
