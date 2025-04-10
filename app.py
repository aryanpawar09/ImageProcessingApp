import streamlit as st
import cv2
import numpy as np
from PIL import Image


st.set_page_config(page_title="Image Wizard", layout="centered", page_icon="🖼️")
st.title("🖼️ Image Wizard - Quick Image Processing")

st.markdown("<h4 style='text-align: center'><b>Name: Aryan Anil Pawar &nbsp;&nbsp; Reg No: 229301788</b></h4>", unsafe_allow_html=True)


st.markdown("""
<style>
body {
    background-color: #f4f4f4;
}
[data-testid="stSidebar"] {
    background-color: #333;
    color: white;
}
h1 {
    text-align: center;
}
</style>
""", unsafe_allow_html=True)


st.sidebar.header("Upload Image")
uploaded_file = st.sidebar.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    st.image(image, caption="Original Image", use_column_width=True)

   
    st.sidebar.markdown("---")
    st.sidebar.header("Choose Operation")
    operation = st.sidebar.selectbox("Select Processing Type", [
        "Convert to Grayscale",
        "Convert to Negative",
        "Edge Detection",
        "Apply Blur"
    ])

    st.markdown("### 🔧 Processed Output")

    if operation == "Convert to Grayscale":
        gray_img = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        st.image(gray_img, caption="Grayscale Image", use_column_width=True, clamp=True, channels="GRAY")

    elif operation == "Convert to Negative":
        neg_img = 255 - img_array
        st.image(neg_img, caption="Negative Image", use_column_width=True)

    elif operation == "Edge Detection":
        method = st.selectbox("Select Edge Method", ["Canny", "Laplacian"])
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

        if method == "Canny":
            t1 = st.slider("Lower Threshold", 0, 255, 100)
            t2 = st.slider("Upper Threshold", 0, 255, 200)
            edge = cv2.Canny(gray, t1, t2)
        else:
            edge = cv2.Laplacian(gray, cv2.CV_64F)
            edge = np.uint8(np.absolute(edge))
        
        st.image(edge, caption="Edge Detected Image", use_column_width=True, clamp=True, channels="GRAY")

    elif operation == "Apply Blur":
        blur_type = st.radio("Choose Blur Type", ["Gaussian", "Median", "Sharpen"])
        
        if blur_type == "Gaussian":
            k = st.slider("Kernel Size", 3, 25, 7, step=2)
            blur_img = cv2.GaussianBlur(img_array, (k, k), 0)
        elif blur_type == "Median":
            k = st.slider("Kernel Size", 3, 25, 5, step=2)
            blur_img = cv2.medianBlur(img_array, k)
        else:
            kernel = np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])
            blur_img = cv2.filter2D(img_array, -1, kernel)

        st.image(blur_img, caption=f"{blur_type} Filter Applied", use_column_width=True)

else:
    st.info("👈 Upload an image from the sidebar to get started.")
