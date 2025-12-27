# Beyond Text: Yapay Zekaya “Göz” Kazandırmak

Bu proje, **TurkStudentCo Workshop Webinarı** kapsamında geliştirilen, el hareketlerini algılayıp (Computer Vision) bunları anlamlandıran ve Yapay Zeka (LLM) ile yanıt veren bir uygulamadır.

## 🚀 Özellikler
- **MediaPipe:** El iskeleti çıkarma ve hareket algılama.
- **Gemini API:** Algılanan harekete göre yaratıcı cevaplar üretme.
- **Local LLM (Qwen):** API kotası dolsa bile çalışmaya devam eden "Yedek Mod".
- **Mock Mode:** İlk iki modelde hata olması durumunda back-up planı - mock llm.
- **Real-time:** Düşük gecikme ile anlık tepki.

## 🛠️ Kurulum

Projeyi kendi bilgisayarınızda çalıştırmak için adımları takip edin:

Repoyu Klonlayın:
   ```bash
   git clone <https://github.com/zgeblbl/beyond-text-workshop.git>
   cd beyond-text-workshop
   ```
Sanal Ortamı Kurun (Önerilen):

```bash
python -m venv venv
# Windows için:
venv\Scripts\activate
# Mac/Linux için:
source venv/bin/activate
```
Gerekli Kütüphaneleri Yükleyin:

```bash
pip install -r requirements.txt
```
## 🔑 API Anahtarı Ayarı (Önemli!)
Bu proje Google Gemini API kullanır. Güvenlik nedeniyle API anahtarı repoda paylaşılmamıştır.

- Google AI Studio adresinden ücretsiz bir API Key alın.
- Proje ana dizininde api_key.txt adında bir dosya oluşturun.
- Aldığınız anahtarı bu dosyanın içine yapıştırın ve kaydedin.

## ▶️ Çalıştırma
Her şey hazırsa uygulamayı başlatın:

```bash
python app.py
```
Kameranız açılacak ve terminalde yerel sunucu adresi (genellikle http://127.0.0.1:7860) görünecektir.

## 🤖 Nasıl Çalışır?
- Yumruk (Rock): Taş/Yumruk işareti.
- İşaret (Point): Bir parmak açık.
- Zafer (Peace): İki parmak havada.
- Selam (Hello): Beş parmak açık.

Not: Eğer API kotanız dolarsa, sistem otomatik olarak "Mock Mode"a geçer ve hazır cevaplar verir.

## Geliştirici: Özge Bülbül 

Workshop katılımcılarına teşekkürler! 🎓
