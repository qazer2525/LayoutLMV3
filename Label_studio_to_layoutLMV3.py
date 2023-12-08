import json
import os
from dotenv import load_dotenv
from PIL import Image
import random
import re
import os

from sympy import EX
base_directory = os.getcwd()
input_folder = base_directory + r"\files\label_studio"
def convert_bounding_box(x, y, width, height):
	"""Converts the given bounding box coordinates to the YOLO format.

	Args:
	x: The x-coordinate of the top-left corner of the bounding box.
	y: The y-coordinate of the top-left corner of the bounding box.
	width: The width of the bounding box.
	height: The height of the bounding box.

	Returns:
	A tuple of four coordinates (x1, y1, x2, y2) in the YOLO format.
	"""

	x1 = x * 10
	y1 = y * 10
	x2 = (x + width) * 10
	y2 = (y + height) * 10

	return [x1, y1, x2, y2]


# load_dotenv(".\.env")
# labels = os.getenv("labels").split(",")

####################################### Loading json data ###################################
def conversion_label_studio_to_layoutlmv3(json_type):
    output = []
    if json_type == "train":
        try:
            with open(f"{input_folder}\\training.json", encoding="utf8") as f:
                data = json.load(f)
        except Exception as e:
            return
    elif json_type == "eval":
        try:
            with open(f"{input_folder}\\testing.json", encoding="utf8") as f:
                data = json.load(f)  
        except Exception as e:
            return

    if os.path.exists(base_directory + r"\files\pdfs") and os.path.isdir(base_directory + r"\files\pdfs"):
        file_list = os.listdir(base_directory + r"\files\pdfs")
    else:
        print("The specified path is not a valid folder.")


    for annoatated_image in data:
        data = {}
        annotation = []
        ann_list = []

        if len(annoatated_image) < 8:
            continue

        for k, v in annoatated_image.items():
            if k == 'ocr':
                pdf = v.split('/')[-1]
                pdf_folder = v.split('/')[-2]
                print(pdf_folder)
                print(f'filename: {v}')
                data["image"] = f"{base_directory}\\files\\images\\{json_type}\\{pdf_folder}\\{pdf}"
                print(data["image"])
                output.append(data)
                
            if k == 'bbox':
                width = v[0]['original_width']
                height = v[0]['original_height']

                data["height"] = height
                data["width"] = width



        boxes = []
        ner_tags = []
        texts = []
        for bb, text, label in zip(annoatated_image['bbox'], annoatated_image['transcription'],   annoatated_image['label']):

            boxes.append(convert_bounding_box(bb['x'], bb['y'], bb['width'], bb['height']))
            ner_tags.append(label['labels'][-1])
            texts.append(text)

            data["tokens"] = texts
            data["bboxes"] = boxes
            data["ner_tags"] = ner_tags

    if json_type == "train":
        with open(f"{input_folder}\\training_train_layoutLMV3.json", "w") as f:
            json.dump(output, f, indent=4)

    elif json_type == "eval":
        with open(f"{input_folder}\\training_test_layoutLMV3.json", "w") as f:
            json.dump(output, f, indent=4)


conversion_label_studio_to_layoutlmv3("train")
conversion_label_studio_to_layoutlmv3("eval")
print("Done!")