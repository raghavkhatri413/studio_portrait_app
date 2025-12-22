# processor.py

import cv2
import numpy as np
from PIL import Image
from rembg import remove, new_session
from skimage.restoration import wiener
import streamlit as st

# --------------------------------------------------
# Cache U2Net session (VERY IMPORTANT for Streamlit)
# --------------------------------------------------
@st.cache_resource
def get_u2net_session():
    return new_session("u2net")

# --------------------------------------------------
# Main processing function
# --------------------------------------------------
def studio_portrait(image_bytes):
    # Decode image
    file_bytes = np.asarray(bytearray(image_bytes), dtype=np.uint8)
    raw = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(raw, cv2.COLOR_BGR2RGB)

    # ---------- PERSON MATTING ----------
    sess = get_u2net_session()
    fg = remove(Image.fromarray(img), session=sess)

    alpha = np.array(fg.split()[-1]).astype(np.float32) / 255.0
    alpha = cv2.GaussianBlur(alpha, (31, 31), 0)
    person_mask = (alpha > 0.6).astype(np.float32)

    # ---------- PERSON-ONLY MOTION DEBLUR ----------
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    psf = np.ones((1, 9)) / 9

    deblur = wiener(gray, psf, balance=0.15)
    deblur = np.clip(deblur * 255, 0, 255).astype(np.uint8)

    # Detail-only injection (prevents whitening)
    detail = deblur.astype(np.float32) - gray.astype(np.float32)
    detail = np.clip(detail, -20, 20)

    result = img.astype(np.float32)
    for c in range(3):
        result[..., c] += detail * person_mask * 0.8

    result = np.clip(result, 0, 255).astype(np.uint8)

    # ---------- BACKGROUND BLUR (REDUCED INTENSITY) ----------
    bg_blur = cv2.GaussianBlur(img, (0, 0), sigmaX=22, sigmaY=22)

    final = (
        result * alpha[..., None] +
        bg_blur * (1 - alpha[..., None])
    ).astype(np.uint8)

    return img, final
