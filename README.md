# LayoutLMV3_Fine_Tuning


Please find the model video explanation in the youtube - https://www.youtube.com/watch?v=bBwDTY38X58&list=PLeNIpK8NwtHtxa2wC1OcPb8RmQ9vy-Uav

# Prerequisites:

1. Python 3.9.* (use the installer not the embedded/portable ver)

2. Onedrive to be connected to local pc. make sure it follows:

    ```C:\Users\(Employee_No)\OneDrive - Singapore Aero Engine Services Pte Ltd```

(Create a folder ```LayoutLMV3``` in the onedrive folder, followed by another 3 folders inside ```LayoutLMV3```: ```json conversion```, ```test_model_input```, ```test_model_output```)


3. Microsoft Flow installed with desktop flow (Check if the machine is registered with Microsoft Automate by running ```Power Automate machine runtime```)
# Steps:

Always use the main_menu.bat to check for avaliable options, if you can program you can check the different scripts

# Installations:

1. ```1. Install```

2. create a .env file at where main_menu.bat is located

3. fill up .env as according to .env.dist

# PreLabeling:

1. Input pdfs into files/pdfs

2. Run main_menu.bat and enter:```2. Convert_pdf_to_dataset``` (json file is found in ```files/ocr_tasks```)

3. Run main_menu.bat and enter: ```6. Launch label-studio```

4. Do labelling (refer to https://youtu.be/_7PlXrFX7VM?list=PLeNIpK8NwtHtxa2wC1OcPb8RmQ9vy-Uav&t=400)

5. Export as json-Min and put in `files/label-studio`

# Training from base model:

1. Run main_menu.bat and enter: ```3. Convert_label_to_layout```

2. Run main_menu.bat and enter: ```4. Training from base ```

(take note of the generated label before training, try to save it to somewhere)

3. The model will be saved at `src/models`

# Fine-tuning:

1. edit the .env in `src/` to use the model (etc, ```./models/model-8asdj34```)

2. Run main_menu.bat and enter: ```5. Fine-tuning```


# Microsoft Flow

There should be 3 main flows to make it work in Microsoft flow 

1. Create JSON file for new files to save in onedrive location, saving in the Intranet also (Auto Creation Automation)

2. Run model using desktop flow to generate the result (Run Inference)

3. populate column using json (From onedrive to sharepoint (add column))


Current this model and scripts is catered towards FFA, however to use for more general use,

1. collect a few pdfs and follow the above until Training

There are 2 parts for model usage

1. model inference (what the model outputs)

2. compile json (to compile model outputs to smaller version for sharepoint flow to use)




FFA_trained_v0.0.1
Labels:  {0: 'published date', 1: 'effective date', 2: 'turbofan engine', 3: 'document type', 4: 'others'}

B and I Ner tags for FFA_trained_v0.0.1
Labels: {0: 'B-DOCUMENT_TYPE', 1: 'B-EFFECTIVE_DATE', 2: 'B-PUBLISHED_DATE', 3: 'B-TURBOFAN_ENGINE', 4: 'I-DOCUMENT_TYPE', 5: 'I-EFFECTIVE_DATE', 6: 'I-PUBLISHED_DATE', 7: 'I-TURBOFAN_ENGINE', 8: 'O'}