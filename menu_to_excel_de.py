import streamlit as st
import os
import pandas as pd
import base64
from PIL import Image
import fitz  # PyMuPDF
import re
import io

# Set page configuration
st.set_page_config(layout="wide")

MAIN_COLOR = "#163c68"
SECONDARY_COLOR = "#cddff4"

# Responsive styles and German translations
st.markdown(f"""
<style>
body {{
    background-color: #fff !important;
    font-family: "Helvetica", sans-serif;
    color: #000;
}}
.sidebar .sidebar-content {{
    background-color: #f9f9f9 !important;
    color: #000 !important;
}}
.block-container {{
    background-color: #fff !important;
    padding-top: 40px !important; /* Extra top padding */
}}
h1, h2, h3, h4, h5, h6 {{
    color: {MAIN_COLOR} !important;
}}
.st-download-button {{
    background-color: {MAIN_COLOR} !important;
    color: #fff !important;
    border-radius: 4px;
    border: none;
}}
.st-download-button:hover {{
    background-color: #122b4b !important;
    color: #fff !important;
}}
.st-button > button:first-child {{
    background-color: {MAIN_COLOR} !important;
    color: #fff;
    border-radius: 4px;
    border: none;
}}
.st-button > button:first-child:hover {{
    background-color: #122b4b !important;
    color: #fff;
}}
.uploadedFileInfo {{
    color: #555 !important;
}}
img {{
    max-width: 100%;
    height: auto;
}}
</style>
""", unsafe_allow_html=True)

def pdf_to_jpeg(pdf_file):
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    images = []
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)
    return images

# Main application
def main():
    # Display logo and title
    logo = "logo.png"  
    col1, col2 = st.columns([0.2, 1])
    with col1:
        if os.path.exists(logo):
            st.image(logo, use_container_width=True)
    with col2:
        st.title("AI-Menü-Konverter in Excel mit Übersetzungen")

    st.markdown("<hr style='border:none; height:1px; background-color:#ccc; margin:20px 0;' />", unsafe_allow_html=True)
    st.write("Laden Sie Ihr Menü (PDF oder Bild) hoch und konvertieren Sie es in eine strukturierte Excel-Datei mit Übersetzungen in mehrere Sprachen.")
    st.write("Dies kann zwischen **5 und 10 Minuten** dauern, abhängig von der Menügröße.")
    st.write("Bitte haben Sie Geduld, während der Prozess läuft.")

    # File uploader
    uploaded_files = st.file_uploader(
        "Laden Sie Ihre Datei(en) hoch (PDF oder Bild):", 
        type=["pdf", "jpg", "jpeg", "png"], accept_multiple_files=True
    )

    # Language selector
    menu_language = st.selectbox(
        "Wählen Sie die Sprache des Menüs:", 
        ["Englisch", "Deutsch", "Französisch", "Spanisch", "Portugiesisch"]
    )

    # Output file name input
    output_filename = st.text_input("Name der Excel-Ausgabedatei (ohne Erweiterung):")

    if st.button("In Excel konvertieren"):
        if not uploaded_files:
            st.error("Bitte laden Sie mindestens eine Datei hoch.")
            return
        if not output_filename:
            st.error("Bitte geben Sie den Namen der Ausgabedatei an.")
            return

        all_images = []
        for uploaded_file in uploaded_files:
            if uploaded_file.type == "application/pdf":
                images = pdf_to_jpeg(uploaded_file)
                all_images.extend(images)
            else:
                img = Image.open(uploaded_file)
                all_images.append(img)

        if all_images:
            st.spinner("Verarbeite Bilder... Dies kann einige Minuten dauern.")
            # Dummy DataFrame for output
            df = pd.DataFrame({
                "CategoryTitleDefault": ["Kategorie 1", "Kategorie 2"],
                "ItemNameDefault": ["Element 1", "Element 2"],
                "ItemPrice": ["10.99", "20.99"]
            })

            output_path = f"{output_filename}.xlsx"
            df.to_excel(output_path, index=False)
            st.success(f"Excel-Datei erfolgreich als {output_path} gespeichert.")

            with open(output_path, "rb") as f:
                st.download_button(
                    label="Excel-Datei herunterladen",
                    data=f.read(),
                    file_name=output_path,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

if __name__ == "__main__":
    main()
