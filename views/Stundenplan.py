import streamlit as st
from PIL import Image
import io
from utils.data_manager import DataManager

st.title("Stundenplan")

data_manager = DataManager()

username = st.session_state.get("username")
name = st.session_state.get("name")

def fix_image_orientation(image):
    """Fix image orientation based on EXIF data."""
    try:
        from PIL import ExifTags
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        
        exif = image._getexif()
        if exif is not None:
            exif_dict = dict(exif.items())
            if orientation in exif_dict:
                orientation_value = exif_dict[orientation]
                if orientation_value == 3:
                    image = image.rotate(180, expand=True)
                elif orientation_value == 6:
                    image = image.rotate(270, expand=True)
                elif orientation_value == 8:
                    image = image.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        pass
    
    return image

st.markdown("### Bild hochladen")
uploaded_file = st.file_uploader(
    "Lade hier Bilder deiner Stunden-/Übungspläne hoch",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    image = fix_image_orientation(image)
    img_bytes = io.BytesIO()
    image.save(img_bytes, format="PNG")
    img_bytes_data = img_bytes.getvalue()
    st.image(image, caption="Vorschau", use_container_width=True)

    if st.button("Speichern", use_container_width=True):
        try:
            data_manager.save_user_data(img_bytes_data, 'stundenplan.png')
            st.success("✅ Bild erfolgreich gespeichert!")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Fehler beim Speichern: {e}")

st.markdown("---")
st.markdown("### Dein gespeicherter Stundenplan")

try:
    saved_image_bytes = data_manager.load_user_data(
        'stundenplan.png',
        initial_value=None
    )
    
    if saved_image_bytes is not None:
        st.image(saved_image_bytes, caption="Dein gespeicherter Stundenplan", use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="Herunterladen",
                data=saved_image_bytes,
                file_name="stundenplan.png",
                mime="image/png",
                use_container_width=True
            )
        with col2:
            if st.button("Bild löschen", use_container_width=True):
                try:
                    data_manager.delete_user_data('stundenplan.png')
                    st.warning("Bild wurde gelöscht.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Fehler beim Löschen: {e}")
    else:
        st.info("Du hast noch kein Bild gespeichert. Lade oben eines hoch!")
        
except Exception as e:
    st.info("Du hast noch kein Bild gespeichert. Lade oben eines hoch!")