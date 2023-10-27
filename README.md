# LayoutLMV3_Fine_Tuning


Please find the model video explanation in the youtube - https://www.youtube.com/watch?v=bBwDTY38X58&list=PLeNIpK8NwtHtxa2wC1OcPb8RmQ9vy-Uav

# Prerequisites:

1. Python 3.9.* (use the installer not the embedded/portable ver)

2. Onedrive to be connected to local pc. make sure it follows:

    ```C:\Users\(Employee_No)\OneDrive - Singapore Aero Engine Services Pte Ltd```

3. A HuggingFace Account, with token access (https://huggingface.co/settings/tokens)

4. A HuggingFace Repo to upload to

# Steps:

Always use the main_menu.bat

# Installations:

1. ```1. Install```

2. create a .env file at where main_menu.bat is located

3. fill up .env as according to .env.dist

# PreLabeling:

1. Input pdfs into files/pdfs

2.  ```2. Convert_pdf_to_dataset``` (json file is found in files/ocr_tasks)

3. ```6. Launch label-studio```

4. Do labelling (refer to https://youtu.be/_7PlXrFX7VM?list=PLeNIpK8NwtHtxa2wC1OcPb8RmQ9vy-Uav&t=400)

5. Export as json-Min and put in files/label-studio

# Training from base model:

1. ```3. Convert_label_to_layout```

2. ```4. Training from base ```

# Fine-tuning:

1. ```5. Fine-tuning```



FFA_trained_v0.0.1
Labels:  {0: 'published date', 1: 'effective date', 2: 'turbofan engine', 3: 'document type', 4: 'others'}

B and I Ner tags
Labels: {0: 'B-DOCUMENT_TYPE', 1: 'B-EFFECTIVE_DATE', 2: 'B-PUBLISHED_DATE', 3: 'B-TURBOFAN_ENGINE', 4: 'I-DOCUMENT_TYPE', 5: 'I-EFFECTIVE_DATE', 6: 'I-PUBLISHED_DATE', 7: 'I-TURBOFAN_ENGINE', 8: 'O'}