import json
import os
from dotenv import load_dotenv
from PIL import Image
import random
import re
import os
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

with open(f"{input_folder}\\training.json", encoding="utf8") as f:
    data = json.load(f)


train_output = []
test_output = []
test_pdfs = []
current_pdf = ""
test_pdf_count = 0
if os.path.exists(base_directory + r"\files\pdfs") and os.path.isdir(base_directory + r"\files\pdfs"):
	file_list = os.listdir(base_directory + r"\files\pdfs")
	file_count = len(file_list)
	if file_count < 5:
		test_pdf_count_limit = 3
	else:
		test_pdf_count_limit = int(file_count * 0.2)
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
			v = v.split('/')[-1]
			print(f'filename: {v}')
			data["image"] = f"{base_directory}\\files\\images\\{v}"
			pattern = r'-(\d+)\.png'
			target_pdf = re.sub(pattern, '.pdf', v)
			page_number = re.search(pattern, v)
			extracted_int = int(page_number.group(1))

			#start pdf test
			if current_pdf == ""  and test_pdf_count < test_pdf_count_limit and extracted_int == 1:
				if random.choice([True, False]) == True:
				#flip coin
					test_pdfs.append(target_pdf)
					current_pdf = target_pdf
					test_output.append(data)
					test_pdf_count += 1
				#else
				else:
					current_pdf = ""
					train_output.append(data)
					

			#continue page
			elif current_pdf == target_pdf:
				test_output.append(data)
			
			#try and see whether next document is in test
			elif test_pdf_count < test_pdf_count_limit and current_pdf != target_pdf and extracted_int == 1 and current_pdf != "":
				#flip coin
				if random.choice([True, False]) == True:
					test_pdfs.append(target_pdf)
					current_pdf = target_pdf
					test_output.append(data)
					test_pdf_count += 1
				#else
				else:
					current_pdf = ""
					train_output.append(data)
			
			#back to train output
			else:
				train_output.append(data)


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

		# data["annotations"] = ann_list


with open(f"{input_folder}\\training_train_layoutLMV3.json", "w") as f:
  json.dump(train_output, f, indent=4)

with open(f"{input_folder}\\training_test_layoutLMV3.json", "w") as f:
  json.dump(test_output, f, indent=4)

print(test_pdf_count)