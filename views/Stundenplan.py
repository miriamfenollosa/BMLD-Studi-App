import streamlit as st
from PIL import Image
import io

st.title("Stundenplan")

# File Uploader
uploaded_file = st.file_uploader(
    "Lade ein Bild deines aktuellen Stundenplanes hoch 📤",
    type=["png", "jpg", "jpeg"]
)

# Verarbeitung
if uploaded_file is not None:
    # Bild öffnen
    image = Image.open(uploaded_file)

    # Anzeige
    st.image(image, caption="📷 Dein hochgeladenes Bild", use_container_width=True)

    # Infos
    st.write("📄 Dateiname:", uploaded_file.name)
    st.write("📏 Format:", image.format)
    st.write("📐 Größe:", image.size)

    # ---------------------------
    # Optional: als Bytes speichern
    # ---------------------------
    img_bytes = io.BytesIO()
    image.save(img_bytes, format=image.format)
    img_bytes = img_bytes.getvalue()

    # Session State speichern
    st.session_state["uploaded_image"] = img_bytes

    st.success("Bild erfolgreich hochgeladen ✅")

# Optional: Anzeige aus Session State
if "uploaded_image" in st.session_state:
    st.markdown("---")
    st.subheader("Gespeichertes Bild 💾")
    st.image(st.session_state["uploaded_image"])
