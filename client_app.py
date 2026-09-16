import streamlit as st
import requests

# Sayfa yapılandırması
st.set_page_config(
    page_title="AgroVision Saha Asistanı", 
    page_icon="🌿", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Mobil dostu özel CSS stilleri
st.markdown("""
    <style>
    .stButton button {
        width: 100%;
        background-color: #2e7d32;
        color: white;
        font-size: 18px;
        font-weight: bold;
        padding: 0.75rem;
        border-radius: 12px;
        border: none;
    }
    .stButton button:hover {
        background-color: #1b5e20;
        color: white;
    }
    .report-card {
        background-color: #f1f8e9;
        padding: 20px;
        border-radius: 15px;
        border-left: 6px solid #2e7d32;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: #2e7d32;'>🌿 AgroVision Saha Asistanı</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>Domates Yaprak ve Meyve Teşhis Sistemi</p>", unsafe_allow_html=True)

# Buluttaki Render FastAPI adresiniz
CLOUD_API_URL = "https://agrovision-api.onrender.com/api/analiz-et"

# Kullanıcıya seçim hakkı: Kamera ile çek veya Dosya/Galeri yükle
secim = st.radio("Görüntü Kaynağı Seçin:", ["📷 Kameradan Çek", "📁 Galeriden / Dosyadan Yükle"], horizontal=True)

uploaded_file = None

if secim == "📷 Kameradan Çek":
    uploaded_file = st.camera_input("Bitkiyi kadraja yerleştirin ve çekin")
else:
    uploaded_file = st.file_uploader("Dosya seçin...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Seçilen veya çekilen görseli göster
    st.image(uploaded_file, caption="Aktarılan Saha Görseli", use_container_width=True)
    
    st.write("") 
    
    if st.button("🚀 AgroVision ile Analiz Et"):
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
    st.info("💡 Kamerayı açarak veya fotoğraf yükleyerek analizi başlatabilirsiniz.")
