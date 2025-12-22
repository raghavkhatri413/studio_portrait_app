import streamlit as st
from processor import studio_portrait
from PIL import Image
import io

st.set_page_config(page_title="Studio Portrait AI", layout="wide")
st.title("📸 Studio-Quality Portrait Generator")
st.info("⬆️ Upload an image to generate a studio-quality portrait")

uploaded = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png"]
)

if uploaded:
    with st.spinner("Processing image..."):
        original, enhanced = studio_portrait(uploaded.read())

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original Image")
        st.image(original, use_container_width=True)

    with col2:
        st.subheader("Studio-Quality Output")
        st.image(enhanced, use_container_width=True)

    buffer = io.BytesIO()
    Image.fromarray(enhanced).save(buffer, format="PNG")
    buffer.seek(0)

    st.download_button(
        label="⬇️ Download Studio Image",
        data=buffer,
        file_name="studio_output.png",
        mime="image/png"
    )
