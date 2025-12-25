import google.generativeai as genai

# API Key'ini buraya yapıştır
GOOGLE_API_KEY = "AIzaSyBBAC2pQ6WWsyT_0R39QeLwwEfmgo8xByw"

genai.configure(api_key=GOOGLE_API_KEY)

print("🔍 Erişim iznin olan modeller taranıyor...\n")

try:
    available_models = []
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ BULUNDU: {m.name}")
            available_models.append(m.name)
            
    if not available_models:
        print("❌ HİÇBİR MODEL BULUNAMADI! API Servisi kapalı olabilir.")
    else:
        print(f"\n💡 İpucu: utils.py dosyasında model ismini '{available_models[0]}' olarak değiştirmelisin.")

except Exception as e:
    print(f"❌ BAĞLANTI HATASI: {e}")