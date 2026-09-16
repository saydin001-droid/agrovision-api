import os
import tempfile
from fastapi import FastAPI, UploadFile, File, HTTPException
import google.generativeai as genai

# FastAPI uygulamasını başlatıyoruz
app = FastAPI(title="AgroVision API", version="1.0")

# Google Gemini API yapılandırması
# (Render veya Cloud Run ortam değişkenlerinden API anahtarını otomatik alır, yoksa tırnak içine yazabilirsiniz)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "BURAYA_GEMINI_API_ANAHTARINIZI_YAZIN")
genai.configure(api_key=GEMINI_API_KEY)

# Gemini model ayarları (Görüntü analizi için uygun model)
generation_config = {
    "temperature": 0.2,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 1024,
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config
)

@app.get("/")
def read_root():
    return {"status": "AgroVision API aktif ve çalışıyor 🌿"}

@app.post("/api/analiz-et")
async def analiz_et(file: UploadFile = File(...)):
    temp_file_path = None
    try:
        # 1. Gelen görseli geçici bir dosyaya kaydediyoruz
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            contents = await file.read()
            temp_file.write(contents)
            temp_file_path = temp_file.name

        # 2. Dosyayı Gemini için yüklüyoruz
        sample_file = genai.upload_file(temp_file_path, mime_type="image/jpeg")

        # 3. Zirai analiz için uzmana talimat veriyoruz
        prompt = (
            "Sen uzman bir ziraat mühendisi ve bitki patoloğusun. "
            "Bu domates bitkisine ait görseli incele. "
            "1. Görülen belirtileri ve olası hastalık/stres faktörünü (örneğin TSWV, ToBRFV, mantari hastalıklar, besin noksanlığı vb.) net bir şekilde belirt. "
            "2. Çiftçinin alması gereken acil kültürel veya kimyasal çözüm önerilerini madde madde kısa ve anlaşılır bir Türkçe ile açıkla."
        )

        # 4. Gemini modelinden yanıt alıyoruz
        response = model.generate_content([sample_file, prompt])
        
        # Analiz sonucunu dönüyoruz
        return {"analiz_sonucu": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        # 5. Sunucuda yer kaplamaması için geçici dosyayı siliyoruz
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except Exception:
                pass
