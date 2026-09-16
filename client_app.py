import streamlit as st
import requests

# Sayfa yapılandırması
st.set_page_config(
    page_title="AgroVision", 
    page_icon="🌿", 
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

# Başlık ve Alt Başlık
st.markdown("<h2 style='text-align: center; color: #2e7d32; margin-bottom: 0;'>🌿 AgroVision</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666; font-size: 14px;'>Domates Yaprak ve Meyve Teşhis Sistemi</p>", unsafe_allow_html=True)
st.write("---")

# Buluttaki Render FastAPI adresiniz
CLOUD_API_URL = "https://agrovision-api.onrender.com/api/analiz-et"

# Session State ile seçimi takip edelim
if "secim" not in st.session_state:
    st.session_state.secim = None

# Butonları sayfada mükemmel ortalamak için orta sütun yapısı kullanalım
_, center_col, _ = st.columns([1, 6, 1])

with center_col:
    if st.button("📷 Take a photo", use_container_width=True):
        st.session_state.secim = "kamera"
    
    if st.button("📁 Select from gallery", use_container_width=True):
        st.session_state.secim = "galeri"

uploaded_file = None

# Seçime göre ilgili aracı aktif edelim
if st.session_state.secim == "kamera":
    st.write("")
    uploaded_file = st.camera_input("Bitkiyi kadraja yerleştirin")
elif st.session_state.secim == "galeri":
    st.write("")
    uploaded_file = st.file_uploader("Galeriden fotoğraf seçin", type=["jpg", "jpeg", "png"])

# Fotoğraf yüklendiyse analiz aşaması
if uploaded_file is not None:
    st.write("---")
    st.image(uploaded_file, caption="Aktarılan Saha Görseli", use_container_width=True)
    
    st.write("") 
    
    # Analiz butonunu da ortalayalım
    _, btn_col, _ = st.columns([1, 6, 1])
    with btn_col:
        if st.button("🚀 AgroVision ile Analiz Et", type="primary", use_container_width=True):
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
    if not st.session_state.secim:
        st.info("💡 Başlamak için yukarıdaki butonlardan birine tıklayın.")

# Geliştirici Bilgisi (Footer)
st.markdown("""
    <div class="footer">
        Geliştirici: <b>Serkan Aydın</b> | AgroVision AI Sistemleri
    </div>
""", unsafe_allow_html=True)
