import fitz
import os
import glob
base_directory = os.getcwd()
pdf_folder_path = base_directory + r"\files\pdfs"
image_folder_path = base_directory + r"\files\images"
dpi = 300
zoom = dpi/72
magnify = fitz.Matrix(zoom, zoom)


pdf_files = glob.glob(f"{pdf_folder_path}\*.pdf")
for x in pdf_files:
    doc = fitz.open(x)
    count = 0
    pdf_name = x.split("\\")[-1]
    for page in doc:
        count+=1
        pix = page.get_pixmap(matrix=magnify)
        pix.save(f"{image_folder_path}\{pdf_name.strip('.pdf')}-{count}.png")