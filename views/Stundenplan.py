import streamlit as st
from supabase import create_client, Client
from PIL import Image
import io

# ─────────────────────────────────────────────
# 1. SUPABASE VERBINDUNG
# ─────────────────────────────────────────────
@st.cache_resource
def init_supabase() -> Client:
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )

supabase = init_supabase()
BUCKET = "stundenplaene"

# ─────────────────────────────────────────────
# 2. EINGELOGGTEN BENUTZER HOLEN
#    (Login läuft bereits über app.py / LoginManager)
# ─────────────────────────────────────────────
username = st.session_state.get("username")  # z.B. "max_mustermann"
name = st.session_state.get("name")          # z.B. "Max Mustermann"

# ─────────────────────────────────────────────
# 3. HILFSFUNKTIONEN
# ─────────────────────────────────────────────
def upload_image(username, img_bytes):
    file_path = f"{username}/stundenplan.png"
    try:
        supabase.storage.from_(BUCKET).upload(
            path=file_path,
            file=img_bytes,
            file_options={"content-type": "image/png", "upsert": "true"}
        )
        return True, None
    except Exception as e:
        return False, str(e)

def load_image(username):
    file_path = f"{username}/stundenplan.png"
    try:
        response = supabase.storage.from_(BUCKET).download(file_path)
        return response
    except Exception:
        return None

def delete_image(username):
    file_path = f"{username}/stundenplan.png"
    try:
        supabase.storage.from_(BUCKET).remove([file_path])
        return True
    except Exception:
        return False

# ─────────────────────────────────────────────
# 4. HAUPTBEREICH
# ─────────────────────────────────────────────
st.title("📅 Stundenplan")
st.write(f"Willkommen, **{name}**!")

# ── BILD HOCHLADEN ──
st.markdown("### 📤 Bild hochladen")
uploaded_file = st.file_uploader(
    "Lade hier Bilder deiner Stunden-/Übungspläne hoch",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    img_bytes = io.BytesIO()
    image.save(img_bytes, format="PNG")
    img_bytes = img_bytes.getvalue()

    st.image(image, caption="Vorschau", use_container_width=True)

    if st.button("💾 Speichern", use_container_width=True):
        success, error = upload_image(username, img_bytes)
        if success:
            st.success("✅ Bild erfolgreich gespeichert!")
            st.rerun()
        else:
            st.error(f"❌ Fehler beim Speichern: {error}")

# ── GESPEICHERTES BILD ──
st.markdown("---")
st.markdown("### 💾 Dein gespeicherter Stundenplan")

saved_image = load_image(username)

if saved_image is not None:
    st.image(saved_image, caption="Dein gespeicherter Stundenplan", use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="📥 Herunterladen",
            data=saved_image,
            file_name="stundenplan.png",
            mime="image/png",
            use_container_width=True
        )
    with col2:
        if st.button("🗑️ Bild löschen", use_container_width=True):
            if delete_image(username):
                st.warning("Bild wurde gelöscht.")
                st.rerun()
            else:
                st.error("Fehler beim Löschen.")
else:
    st.info("Du hast noch kein Bild gespeichert. Lade oben eines hoch!")