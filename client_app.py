import streamlit as st
import requests

# Sayfa yapılandırması (Büyüteç ve yaprak simgesi ile)
st.set_page_config(
    page_title="AgroVision", 
    page_icon="🔍🍃", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Genel kart ve footer stilleri
st.markdown("""
    <style>
    .report-card {
        background-color: #f1f8e9;
        padding: 20px;
        border-radius: 15px;
        border-left: 6px solid #2e7d32;
        margin-top: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .footer {
        text-align: center;
        color: #888;
        font-size: 13px;
        margin-top: 40px;
        padding-bottom: 10px;
        border-top: 1px solid #eee;
        padding-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Başlık ve Alt Başlık (Büyüteç ve yaprak ikonlarıyla)
st.markdown("<h2 style='text-align: center; color: #2e7d32; margin-bottom: 0;'>🔍🍃 AgroVision</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666; font-size: 14px;'>Tomato Symptom Diagnosis System</p>", unsafe_allow_html=True)
st.write("---")

# Buluttaki Render FastAPI adresiniz
CLOUD_API_URL = "https://agrovision-api.onrender.com/api/analiz-et"

# Tek ve merkezi yükleme alanı (Mobilde hem kamera hem galeri seçeneği sunar)
_, center_col, _ = st.columns([1, 6, 1])

with center_col:
    uploaded_file = st.file_uploader(
        "📸 Upload / Take a photo", 
        type=["jpg", "jpeg", "png"]
    )

# Fotoğraf yüklendiyse önizleme ve analiz aşaması
if uploaded_file is not None:
    st.write("---")
    _, img_col, _ = st.columns([1, 6, 1])
    with img_col:
        st.image(uploaded_file, caption="Aktarılan Saha Görseli", use_container_width=True)
        st.write("") 
        
        if st.button("🚀 Analyse with AgroVision", type="primary", use_container_width=True):
            with st.spinner("Yapay zeka patolog bitkiyi inceliyor, lütfen bekleyin..."):
                try:
                    files = {"file": ("saha_gorseli.jpg", uploaded_file.getvalue(), "image/jpeg")}
                    response = requests.post(CLOUD_API_URL, files=files, timeout=30)
                    
                    if response.status_code == 200:
                        data = response.json()
                        raw_result = data.get("analiz_sonucu", "{}")
                        
                        st.success("Analiz Başarıyla Tamamlandı!")
                        
                        st.markdown(f"""
                        <div class="report-card">
                            <h3>🔬 Teşhis Raporu</h3>
                            <p>{raw_result}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                    else:
                        st.error(f"Sunucu Hatası: {response.status_code}. Lütfen birkaç saniye sonra tekrar deneyin.")
                        
                except requests.exceptions.Timeout:
                    st.error("Zaman aşımı! Yapay zeka sunucusu şu an yoğun, lütfen tekrar deneyin.")
                except Exception as e:
                    st.error(f"Bağlantı hatası: {e}")
else:
    _, info_col, _ = st.columns([1, 6, 1])
    with info_col:
        st.info("💡 Click above to upload or capture a photo.")

# Geliştirici Bilgisi (Footer)
st.markdown("""
    <div class="footer">
        Developer: <b>saydin001-droidn</b> | AgroVision AI Sistemleri
    </div>
""", unsafe_allow_html=True)
