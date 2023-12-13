# LayoutLMV3_Fine_Tuning


Please find the model video explanation in the youtube - https://www.youtube.com/watch?v=bBwDTY38X58&list=PLeNIpK8NwtHtxa2wC1OcPb8RmQ9vy-Uav

This is a modified fork of https://github.com/manikanthp/LayoutLMV3_Fine_Tuning, using Tesseract-OCR. I was having problems with the code so I heavily modified to fit my use.
`src/compile_json.py` is tailored to compile the model output, do create one yourself, or just use inference.py if you just want the model output
The OCR can be swapped out for other OCR, as long as you follow the input format of Label-Studio, but requires abit of programming skills.
inference.py is modified to handle BIO tagging scheme (refer to https://medium.com/analytics-vidhya/bio-tagged-text-to-original-text-99b05da6664)
eg: B-PUBLISHED_DATE (beginning), I-EFFECTIVE_DATE (inside), O (others)

# Prerequisites:

1. Python 3.9.* (use the installer not the embedded/portable ver)

2. Onedrive to be connected to local pc. make sure it follows:

    ```C:\Users\(Employee_No)\OneDrive - Singapore Aero Engine Services Pte Ltd```

(Create a folder ```LayoutLMV3``` in the onedrive folder, followed by another 3 folders inside ```LayoutLMV3```: ```json_conversion```, ```test_model_input```, ```test_model_output```)

3. Microsoft Flow installed with desktop flow (Check if the machine is registered with Microsoft Automate by running ```Power Automate machine runtime```)

# Steps:

Always use the main_menu.bat to check for avaliable options, if you can program you can check the different scripts, open up main_menu.bat to figure out what scripts is running under each choice

# Installations:

1. ```1. Install```

2. create a .env file at where main_menu.bat is located

3. fill up .env as according to .env.dist

(Before proceeding, make sure that you have 1 set of pdfs for training, 1 set of pdfs for evaluation)
# PreLabeling:

1. Input train pdfs into files/train/pdfs and eval pdfs into files/eval/pdfs

2. Run main_menu.bat and enter:```2. Convert_pdf_to_dataset``` (the dataset json files is found in ```files/ocr_tasks```)

3. Run main_menu.bat and enter: ```6. Launch label-studio```

4. Do labelling for both train and eval(refer to https://youtu.be/_7PlXrFX7VM?list=PLeNIpK8NwtHtxa2wC1OcPb8RmQ9vy-Uav&t=400)
(create one project for each dataset with same labels)
(Label unwanted words as `O` for better detections)

5. Export the two sections once you are done with both as json-Min and put in `files/label-studio`. rename the train json as `training.json` and eval json as `testing.json`


# Training from base model:

1. Run main_menu.bat and enter: ```3. Convert_label_to_layout```

2. Run main_menu.bat and enter: ```4. Training from base ```

3. The model will be saved at `src/models`

4. The id2label is saved as `src/id2label.json`. Open up to see what label belongs to what id

# Fine-tuning:

1. edit the `DEST_REPO` .env in `src/` to use the model (etc, ```./models/model-8asdj34```)

2. Run main_menu.bat and enter: ```5. Fine-tuning```


# Microsoft Flow

There should be 3 main flows to make it work in Microsoft flow
(change connection to onedrive/sharepoint/desktop flow if needed)

1. Create JSON file for new files to save in onedrive location, saving in the Intranet also (Auto Creation Automation)

2. Run model using desktop flow to generate the result (Run Inference)

3. populate column using json (From onedrive to sharepoint (add column))

There are 2 parts for model usage

1. model inference (what the model outputs)

2. compile json (to compile model outputs to smaller version for sharepoint flow to use)