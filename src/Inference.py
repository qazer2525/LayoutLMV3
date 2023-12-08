import torch
import json
from PIL import Image, ImageDraw, ImageFont
from transformers import AutoModelForTokenClassification, AutoProcessor, LayoutLMv3FeatureExtractor, LayoutLMv3TokenizerFast, LayoutLMv3Processor, LayoutLMv3ForTokenClassification
import numpy as np
from transformers import LayoutLMv3FeatureExtractor, LayoutLMv3TokenizerFast, LayoutLMv3Processor, LayoutLMv3ForTokenClassification
import pytesseract
import os
import glob
from pdf2image import convert_from_path
import fitz
from dotenv import dotenv_values

# id2label = {0: 'B-DOCUMENT_TYPE', 
#                1: 'B-EFFECTIVE_DATE', 
#                2: 'B-PUBLISHED_DATE', 
#                3: 'B-SECTION', 
#                4: 'B-TURBOFAN_ENGINE', 
#                5: 'I-DOCUMENT_TYPE', 
#                6: 'I-EFFECTIVE_DATE', 
#                7: 'I-PUBLISHED_DATE', 
#                8: 'I-SECTION', 
#                9: 'I-TURBOFAN_ENGINE', 
#                10: 'O'}
# label2color = {'B-DOCUMENT_TYPE':"red",
#             'B-EFFECTIVE_DATE':"blue", 
#             'B-PUBLISHED_DATE':"yellow", 
#             'B-SECTION':"pink", 
#             'B-TURBOFAN_ENGINE':"purple",
#             'I-DOCUMENT_TYPE': "red", 
#             'I-EFFECTIVE_DATE':"blue", 
#             'I-PUBLISHED_DATE':"yellow", 
#             'I-SECTION':"pink", 
#             'I-TURBOFAN_ENGINE':"purple",
#             'O':"grey" }

document_type_to_short = {"Federal Aviation Administration": "FAA", "EASE":"EASE"}
trent_type = {

}
LEVELS = {
    'page_num': 1,
    'block_num': 2,
    'par_num': 3,
    'line_num': 4,
    'word_num': 5
}

def convert_for_processor(image, tesseract_output, per_level='word_num'):
    """
    :param image: PIL image object
    :param tesseract_output: the output from tesseract
    :param per_level: control the granularity of bboxes from tesseract
    :return: tasks.json ready to be imported into Label Studio with "Optical Character Recognition" template
    """
    image_width, image_height = image.size
    per_level_idx = LEVELS[per_level]
    bbox = []
    tokens = []
    for i, level_idx in enumerate(tesseract_output['level']):
        if level_idx == per_level_idx:
            box = [1000 * tesseract_output['left'][i] / image_width, 1000 * tesseract_output['top'][i] / image_height, 
                    1000 * (tesseract_output['width'][i] + tesseract_output['left'][i])  / image_width,
                    1000 * (tesseract_output['height'][i] + tesseract_output['top'][i]) / image_height]
            
            bbox.append(box)
            tokens.append(tesseract_output['text'][i])
    return bbox, tokens


def create_image_url(filepath):
    """
    Label Studio requires image URLs, so this defines the mapping from filesystem to URLs
    if you use ./serve_local_files.sh <my-images-dir>, the image URLs are localhost:8081/filename.png
    Otherwise you can build links like /data/upload/filename.png to refer to the files
    """
    filename = os.path.basename(filepath)
    return f'http://localhost:8081/{filename}'



def get_words(tesseract_output, per_level):
    per_level_idx = LEVELS[per_level]
    results = []
    for i, level_idx in enumerate(tesseract_output['level']):
        if level_idx == per_level_idx:
            results.append(tesseract_output['text'][i])
    
    return results


def unnormalize_box(bbox, width, height):
    return [
        width * (bbox[0] / 1000),
        height * (bbox[1] / 1000),
        width * (bbox[2] / 1000),
        height * (bbox[3] / 1000),
    ]


dpi = 300
zoom = dpi/72
magnify = fitz.Matrix(zoom, zoom)


def process_model_output(data: dict):
    pass

def get_onedrive_location(base_directory: str):
    user = "\\".join(base_directory.split("\\")[0:3])
    onedrive_location_local = user + "\\OneDrive - Singapore Aero Engine Services Pte Ltd\\LayoutLMV3"
    if os.path.exists(onedrive_location_local):
        return onedrive_location_local
    else:
        raise ValueError
base_directory = os.getcwd().strip("//src")
pdf_folder_path = get_onedrive_location(base_directory) + r'\test_model_input'
image_folder_path = base_directory + r'\src\images'
output_folder_path = get_onedrive_location(base_directory) + r'\test_model_output'
pytesseract.pytesseract.tesseract_cmd = base_directory + r'\Tesseract-OCR\tesseract.exe'
config = dotenv_values("..\\.env")
target_repo = config["DEST_REPO"]
source_repo = config["SOURCE_REPO"]
# tesseract output levels for the level of detail for the bounding boxes
pdf_files = glob.glob(f"{pdf_folder_path}\*.pdf")
for x in pdf_files:
    doc = fitz.open(x) # type: ignore
    count = 0
    pdf_name = x.split("\\")[-1]
    for page in doc:
        count+=1
        pix = page.get_pixmap(matrix=magnify)
        pix.save(f"{image_folder_path}\{pdf_name.replace('.pdf','', 1)}-page{count}.png")
model = AutoModelForTokenClassification.from_pretrained(target_repo, local_files_only = True) # type: ignore
# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# model.to(device)
processor = AutoProcessor.from_pretrained(source_repo, apply_ocr=True)
images = glob.glob(".\images\*.png")
pdf_name = ""
tasks = {}
target_file = ""
id2label = json.load(open(".\\id2labels.json"))
for x in images:
    
    image_name = x.split("\\")[-1].strip(".png")
    file_name = image_name.split("-page")[0]
    if target_file != file_name and target_file != "":
        with open(f"{output_folder_path}\{target_file}.json", mode='w') as f:
            print(tasks)
            process_model_output(tasks)
            json.dump(tasks, f, indent=2)
        tasks = {}
        target_file = file_name
    elif target_file == "":
        target_file = file_name
    
    image = Image.open(x).convert("RGB")
    width, height = image.size
    encoding = processor(image, truncation=True, return_offsets_mapping=True, return_tensors="pt")
    offset_mapping = encoding.pop('offset_mapping')
    outputs = model(**encoding)

    # get predictions
    predictions = outputs.logits.argmax(-1).squeeze().tolist()        
    token_boxes = encoding.bbox.squeeze().tolist()
    input_ids = encoding.input_ids.squeeze().tolist()

    
    # only keep non-subword predictions
    is_subword = np.array(offset_mapping.squeeze().tolist())[:,0] != 0
    true_tokens = [processor.tokenizer.decode(id) for idx, id in enumerate(input_ids)]
    true_predictions = [id2label[str(pred)] for idx, pred in enumerate(predictions)]
    true_boxes = [unnormalize_box(box, width, height) for idx, box in enumerate(token_boxes)]
    # draw predictions over the image
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    words = {}
    label = "O"
    text = ""
    for prediction, box, token in zip(true_predictions, true_boxes, true_tokens):
        predicted_label = prediction
        if predicted_label != "O":
            if predicted_label[0] == "B" and label == "O":
                text += token
                label = predicted_label[2:]
            
            elif predicted_label[0] == "I" and predicted_label[2:] == label:
                text += token
            
            elif predicted_label[0] == "B" and label != "O":
                if label in words:
                    words[label].append(text)
                else:
                    words[label] = [text]
                text = token
                label = predicted_label[2:]
            
        else:
            if label != "O":
                if label in words:
                    words[label].append(text)
                else:
                    words[label] = [text]
                text = ""
                label = "O"
        # draw.rectangle(box, outline=label2color[predicted_label])
        # draw.text((box[0]+10, box[1]-10), text=predicted_label, fill=label2color[predicted_label], font=font)
    tasks[image_name] = words

    # image.show()
with open(f"{output_folder_path}\{file_name}.json", mode='w') as f:
    print(tasks)
    process_model_output(tasks)
    json.dump(tasks, f, indent=2)
files = glob.glob(image_folder_path + r"\*")
for f in files:
    os.remove(f)
