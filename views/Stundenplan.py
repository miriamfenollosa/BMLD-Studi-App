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
# 2. SESSION STATE INITIALISIEREN
# ─────────────────────────────────────────────
if "user" not in st.session_state:
    st.session_state["user"] = None

# ─────────────────────────────────────────────
# 3. HILFSFUNKTIONEN
# ─────────────────────────────────────────────
def register(name, email, password):
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {"full_name": name}
            }
        })
        return response, None
    except Exception as e:
        return None, str(e)

def login(email, password):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        return response, None
    except Exception as e:
        return None, str(e)

def logout():
    supabase.auth.sign_out()
    st.session_state["user"] = None

def upload_image(user_id, img_bytes):
    file_path = f"{user_id}/stundenplan.png"
    try:
        supabase.storage.from_(BUCKET).upload(
            path=file_path,
            file=img_bytes,
            file_options={"content-type": "image/png", "upsert": "true"}
        )
        return True, None
    except Exception as e:
        return False, str(e)

def load_image(user_id):
    file_path = f"{user_id}/stundenplan.png"
    try:
        response = supabase.storage.from_(BUCKET).download(file_path)
        return response
    except Exception:
        return None

def delete_image(user_id):
    file_path = f"{user_id}/stundenplan.png"
    try:
        supabase.storage.from_(BUCKET).remove([file_path])
        return True
    except Exception:
        return False

# ─────────────────────────────────────────────
# 4. NICHT EINGELOGGT → LOGIN / REGISTRIERUNG
# ─────────────────────────────────────────────
if st.session_state["user"] is None:
    st.title("📅 Stundenplan App")

    tab_login, tab_register = st.tabs(["🔐 Login", "📝 Registrieren"])

    # ── LOGIN ──
    with tab_login:
        st.subheader("Einloggen")
        email = st.text_input("E-Mail", key="login_email")
        password = st.text_input("Passwort", type="password", key="login_password")

        if st.button("Einloggen", use_container_width=True):
            if email and password:
                response, error = login(email, password)
                if error:
                    st.error(f"❌ Fehler: {error}")
                else:
                    st.session_state["user"] = response.user
                    st.success("✅ Erfolgreich eingeloggt!")
                    st.rerun()
            else:
                st.warning("Bitte E-Mail und Passwort eingeben.")

    # ── REGISTRIERUNG ──
    with tab_register:
        st.subheader("Neues Konto erstellen")
        name = st.text_input("Vollständiger Name", key="reg_name")
        email_reg = st.text_input("E-Mail", key="reg_email")
        password_reg = st.text_input("Passwort", type="password", key="reg_password")
        password_reg2 = st.text_input("Passwort wiederholen", type="password", key="reg_password2")

        if st.button("Registrieren", use_container_width=True):
            if not name or not email_reg or not password_reg:
                st.warning("Bitte alle Felder ausfüllen.")
            elif password_reg != password_reg2:
                st.error("❌ Passwörter stimmen nicht überein.")
            elif len(password_reg) < 6:
                st.error("❌ Passwort muss mindestens 6 Zeichen lang sein.")
            else:
                response, error = register(name, email_reg, password_reg)
                if error:
                    st.error(f"❌ Fehler: {error}")
                else:
                    st.success("✅ Konto erstellt! Bitte E-Mail bestätigen, dann einloggen.")

# ─────────────────────────────────────────────
# 5. EINGELOGGT → HAUPTBEREICH
# ─────────────────────────────────────────────
else:
    user = st.session_state["user"]
    user_id = user.id
    name = user.user_metadata.get("full_name", user.email)

    # Sidebar
    with st.sidebar:
        st.write(f"👤 **{name}**")
        st.write(f"📧 {user.email}")
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            logout()
            st.rerun()

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

        if st.button("💾 Speichern", use_container_width=True):
            success, error = upload_image(user_id, img_bytes)
            if success:
                st.success("✅ Bild erfolgreich gespeichert!")
                st.rerun()
            else:
                st.error(f"❌ Fehler beim Speichern: {error}")

        st.image(image, caption="Vorschau", use_container_width=True)

    # ── GESPEICHERTES BILD ──
    st.markdown("---")
    st.markdown("### 💾 Dein gespeicherter Stundenplan")

    saved_image = load_image(user_id)

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
                if delete_image(user_id):
                    st.warning("Bild wurde gelöscht.")
                    st.rerun()
                else:
                    st.error("Fehler beim Löschen.")
    else:
        st.info("Du hast noch kein Bild gespeichert. Lade oben eines hoch!")


