from fastapi import FastAPI, File, UploadFile, HTTPException
from google import genai
from google.genai import types
import os

app = FastAPI(title="AgroVision AI Backend", version="1.0")

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# Tarayıcıdan ana adrese girildiğinde 404 yerine şık bir karşılama versin:
@app.get("/")
async def root():
    return {
        "durum": "aktif", 
        "asistan": "AgroVision AI Backend", 
        "dokuman_ve_test_icin": "/docs"
    }

AGROVISION_SYSTEM_PROMPT = """
Sen uluslararası alanda tanınan uzman bir domates patoloğu, virolog ve bitki koruma uzmanısın. 
Görevin, sana gözlük kamerasından aktarılan domates bitkisi görsellerini analiz ederek özellikle şu kritik etkenleri ve stresleri yüksek doğrulukla teşhis etmektir:
- TSWV (Tomato Spotted Wilt Virus)
- TYLCV (Tomato Yellow Leaf Curl Virus)
- ToBRFV (Tomato Brown Rugose Fruit Virus)
- Fusarium (Vasküler Solgunluk)
- Clavibacter (Bakteriyel Solgunluk ve Kanser)
- ToMV (Tomato Mosaic Virus)
- Veya diğer yaygın fungal/bakteriyel hastalıklar ile besin element noksanlıkları.

Yanıtını kesinlikle şu JSON formatında ver, başka bir açıklama ekleme:
{
  "teshis": "Hastalık veya noksanlık adı",
  "guven_orani": "%95",
  "etken_kategorisi": "Viral / Fungal / Bakteriyel / Noksanlık",
  "acil_aksiyon_onerisi": "Saha için kısa ve net pratik çözüm önerisi"
}
"""

@app.post("/api/analiz-et")
async def gorsel_analizet(file: UploadFile = File(...)):
    temp_file_path = f"temp_{file.filename}"
    try:
        with open(temp_file_path, "wb") as buffer:
            buffer.write(await file.read())
            
        uploaded_file = client.files.upload(file=temp_file_path)
        
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=[uploaded_file, "Bu domates bitkisini analiz et ve istenen JSON formatında yanıt ver."],
            config=types.GenerateContentConfig(
                system_instruction=AGROVISION_SYSTEM_PROMPT,
            ),
        )
        
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        
        return {"durum": "basarili", "analiz_sonucu": response.text}
        
    except Exception as e:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
