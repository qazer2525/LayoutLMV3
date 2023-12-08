import json
from datasets import load_dataset
from transformers import LayoutLMv3FeatureExtractor, LayoutLMv3TokenizerFast, AutoProcessor, LayoutLMv3Processor, LayoutLMv3ForTokenClassification
from torch.optim import AdamW
import numpy as np
import torch
import os
from datasets.features import ClassLabel
from datasets import Features, Sequence, ClassLabel, Value, Array2D, Array3D
from PIL import Image
from datasets import load_metric
import numpy as np
from transformers import TrainingArguments, Trainer
from transformers.data.data_collator import default_data_collator
import evaluate
from datasets import concatenate_datasets

def training_model(starting_repo :str, dest_repo: str, source_repo: str):
    metric = evaluate.load("seqeval")
    base_directory = os.getcwd().strip("//src")
    pdf_folder_path = base_directory + r"\files\pdfs"
    image_folder_path = base_directory + r"\files\images"
    dataset_folder_path = base_directory + r"\files\label_studio"
    model_path = base_directory + r"\files\models"
    output_path = base_directory + r"\files\training_bin"
    processor = AutoProcessor.from_pretrained(starting_repo, apply_ocr=False)
    training_args = TrainingArguments(
                                    output_dir=f"models/{dest_repo}",
                                    max_steps=2500,
                                    per_device_train_batch_size=10,
                                    per_device_eval_batch_size=10,
                                    push_to_hub=True,  # after training, we'd like to push our model to the hub
                                    learning_rate=1e-5,
                                    evaluation_strategy="steps",
                                    eval_steps=250,
                                    load_best_model_at_end=True,
                                    metric_for_best_model="accuracy")

    def compute_metrics(p):
        return_entity_level_metrics = False
        predictions, labels = p
        predictions = np.argmax(predictions, axis=2)

        # Remove ignored index (special tokens)
        true_predictions = [
            [label_list[p] for (p, l) in zip(prediction, label) if l != -100]
            for prediction, label in zip(predictions, labels)
        ]
        true_labels = [
            [label_list[l] for (p, l) in zip(prediction, label) if l != -100]
            for prediction, label in zip(predictions, labels)
        ]

        results = metric.compute(predictions=true_predictions, references=true_labels)
        if return_entity_level_metrics:
            # Unpack nested dictionaries
            final_results = {}
            for key, value in results.items():
                if isinstance(value, dict):
                    for n, v in value.items():
                        final_results[f"{key}_{n}"] = v
                else:
                    final_results[key] = value
            return final_results
        else:
            return {
                "precision": results["overall_precision"],
                "recall": results["overall_recall"],
                "f1": results["overall_f1"],
                "accuracy": results["overall_accuracy"],
            }

    def get_label_list(labels):
        unique_labels = set()
        for label in labels:
            unique_labels = unique_labels | set(label)
        label_list = list(unique_labels)
        label_list.sort()
        return label_list



    def prepare_examples(examples):
        file_name = examples[image_column_name]
        images = []
        for x in file_name:
            images.append(Image.open(x))
        words = examples[text_column_name]
        boxes = examples[boxes_column_name]
        word_labels = examples[label_column_name]
        num_labels = list()
        for x in word_labels:
            temp_array = list()
            for y in x:
                temp_array.append(label2id[y])
            num_labels.append(temp_array)
        encoding = processor(images, words, boxes=boxes, word_labels=num_labels,
                            truncation=True, padding="max_length")
        return encoding

    dataset_train = load_dataset("json", data_files=f"{dataset_folder_path}\\training_train_layoutLMV3.json")
    dataset_test = load_dataset("json", data_files=f"{dataset_folder_path}\\training_test_layoutLMV3.json")
    features = dataset_train["train"].features
    column_names = dataset_train["train"].column_names
    image_column_name = "image"
    text_column_name = "tokens"
    boxes_column_name = "bboxes"
    label_column_name = "ner_tags"
    if isinstance(features[label_column_name].feature, ClassLabel):
        label_list = features[label_column_name].feature.names
        # No need to convert the labels since they are already ints.
        id2label = {k: v for k,v in enumerate(label_list)}
        label2id = {v: k for k,v in enumerate(label_list)}
    else:
        print("no labels, doing it now...")
        label_list = get_label_list(dataset_train["train"][label_column_name])
        id2label = {k: v for k,v in enumerate(label_list)}
        label2id = {v: k for k,v in enumerate(label_list)}
    # id2label= {0: 'effective date', 1: 'turbofan engine', 2: 'published date', 3: 'document type', 4: 'others'}
    # label2id = {'effective date': 0, 'turbofan engine': 1, 'published date': 2, 'document type': 3, 'others': 4}
    # we need to define custom features for `set_format` (used later on) to work properly
    features = Features({
        'pixel_values': Array3D(dtype="float32", shape=(3, 224, 224)),
        'input_ids': Sequence(feature=Value(dtype='int64')),
        'attention_mask': Sequence(Value(dtype='int64')),
        'bbox': Array2D(dtype="int64", shape=(512, 4)),
        'labels': Sequence(feature=Value(dtype='int64')),
    })

    train_dataset = dataset_train["train"].map(
        prepare_examples,
        batched=True,
        remove_columns=column_names,
        features=features,
    )
    eval_dataset = dataset_test["train"].map(
    prepare_examples,
    batched=True,
    remove_columns=column_names,
    features=features,
    )

    train_dataset.set_format("torch")
    model = LayoutLMv3ForTokenClassification.from_pretrained(source_repo,
                                                        id2label=id2label,
                                                        label2id=label2id)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print("Device: ", device)
    model.to(device)
    # Initialize our Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        tokenizer=processor,
        data_collator=default_data_collator,
        compute_metrics=compute_metrics,
    )
    print("Labels: ", id2label)
    print("Source Repo: ", source_repo)
    print("Starting Repo: ", starting_repo)
    print("Destination Repo: ", dest_repo)
    print("Training_dataset: ", len(train_dataset))
    print("Test_dataset: ", len(eval_dataset))
    input("Press any key to start training")
    with open(f"./id2labels.json", mode='w') as f:
        json.dump(id2label, f, indent=2)
    trainer.train()
    trainer.push_to_hub(dest_repo)
    trainer.evaluate()