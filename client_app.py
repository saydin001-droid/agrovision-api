import streamlit as st
import requests

# Sayfa yapılandırması (Mobil tarayıcılarda tam ekran ve şık durması için)
st.set_page_config(
    page_title="AgroVision Mobil", 
    page_icon="🌿", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Mobil dostu özel CSS stilleri (Butonları büyütme ve kart tasarımı)
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

# Buluttaki Render FastAPI adresiniz (Buraya kendi Render linkinizi yazın)
CLOUD_API_URL = "https://agrovision-api.onrender.com/api/analiz-et"

# Fotoğraf yükleme alanı (Telefondan direkt kamera ile çekme seçeneği sunar)
uploaded_file = st.file_uploader(
    "Yaprak veya meyve fotoğraflayın...", 
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed"
)

if uploaded_file is not None:
    # Fotoğrafı ekranda şık ve ortalanmış göster
    st.image(uploaded_file, caption="Saha Görüntüsü", use_container_width=True)
    
    st.write("") # Boşluk
    
    if st.button("🚀 Yapay Zekayı Çalıştır"):
        with st.spinner("Bitki patoloğu inceliyor, lütfen bekleyin..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                response = requests.post(CLOUD_API_URL, files=files, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    raw_result = data.get("analiz_sonucu", "{}")
                    
                    # Başarılı analiz kartı
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
    st.info("💡 Başlamak için yukarıdaki alandan bir fotoğraf yükleyin veya telefon kameranızla çekim yapın.")