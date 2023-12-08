import fitz
import os
import glob
from pathlib import Path

base_directory = os.getcwd()

def convert_pdf_to_images(dataset_type: str):
    pdf_folder_path = base_directory + r"\files\pdfs\{}".format(dataset_type)
    image_folder_path = base_directory + r"\files\images\{}".format(dataset_type)
    dpi = 300
    zoom = dpi/72
    magnify = fitz.Matrix(zoom, zoom)
    pdf_files = glob.glob(f"{pdf_folder_path}\*.pdf")

    
    for x in pdf_files:
        doc = fitz.open(x)
        count = 0
        pdf_name = x.split("\\")[-1]
        output_folder = Path(image_folder_path) / pdf_name.strip('.pdf')  # Folder for each PDF
        output_folder.mkdir(parents=True, exist_ok=True)  # Create folder if it doesn't exist
        for page in doc:
            count+=1
            pix = page.get_pixmap(matrix=magnify)
            pix.save(f"{image_folder_path}\{pdf_name.strip('.pdf')}\{pdf_name.strip('.pdf')}-{count}.png")
convert_pdf_to_images("train")
convert_pdf_to_images("eval")