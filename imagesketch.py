import streamlit as st
import cv2
import numpy as np
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Sketrix", layout="wide")
st.title("Sketrix")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    blur_intensity = st.slider("Tone", 1, 101, 21, step=2)
    clarity = st.slider("Clarity", 50, 300, 256)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inv = 255 - gray
    blur = cv2.GaussianBlur(inv, (blur_intensity, blur_intensity), 0)
    sketch = cv2.divide(gray, 255 - blur, scale=clarity)

    pil_sketch = Image.fromarray(sketch)
    buf = BytesIO()
    pil_sketch.save(buf, format="PNG")
    byte_im = buf.getvalue()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Original Image")
        st.image(img_rgb, use_container_width=True)
    with col2:
        st.subheader("Sketcher")
        st.image(sketch, use_container_width=True, clamp=True)

    st.download_button("Download Sketch", data=byte_im, file_name="sketch.png", mime="image/png")
else:
    st.info("Please upload an image to start.")


