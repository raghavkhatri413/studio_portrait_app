# Studio-Quality Portrait Generator

A computer-vision based web application that converts raw human portraits into studio-quality images.

## Features
- Person-only motion blur removal
- Natural background blur (portrait/bokeh effect)
- Identity-preserving enhancement
- Side-by-side image comparison
- Download enhanced image

## Tech Stack
- Python
- OpenCV
- rembg (u2net)
- scikit-image
- Streamlit

## How to Run Locally

```bash
git clone https://github.com/raghavkhatri413/studio_portrait_app.git
cd studio_portrait_app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
