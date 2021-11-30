# Behavioral Testing of Clinical NLP Models

This repository contains code for testing the behavior of clinical prediction models based on patient letters. For a detailed description of the testing framework see our paper [What Do You See in this Patient? Behavioral Testing of Clinical NLP Models]().

![From an existing test set we create test groups by altering specific tokens in the clinical note. We then analyse the change in predictions which reveals the impact of the mention on the clinical NLP model.](/img/framework.png)

## Usage

Install requirements: `pip install -r requirements.txt`

Run main.py, e.g. for **diagnosis prediction** test on **gender**, **age** and **ethnicity**:
```
python main.py 
    --test_set_path ./path_to_test_set
    --model_path bvanaken/CORe-clinical-diagnosis-prediction
    --task diagnosis
    --shift_keys gender,age,ethnicity
    --save_dir ./results
    --gpu False
```

| Parameter  | Description |
| ------------- | ------------- |
| test_set_path  | Path to original test set file  |
| model_path  | Path to model or Huggingface model hub checkpoint |
| task  | Current options: *diagnosis*, *mortality* |
| shift_keys  | Which patient characteristics to test. Current options: *age*, *gender*, *ethnicity*, *weight*, *intersectional* (gender + ethnicity) |
| save_dir  | Directory to save results, default: *"./results"* |
| gpu  | Whether to use a gpu during inference or not, default: *False* |

### Using Non-Transformer models
The framework currently focuses on testing Transformer-based models. However, it is easy to extend it to any other prediction model. To do so, simply create a new class implementing the [Predictor](/prediction.py#L11) interface and add it to the [TASK_MAP in main.py](/main.py#L23).

## Cite
```
@inproceedings{vanAken2021,
  author    = {Betty van Aken and
               Sebastian Herrmann and
               Alexander Löser},
  title     = {What Do You See in this Patient? Behavioral Testing of Clinical NLP Models},
  booktitle = {Bridging the Gap: From Machine Learning Research to Clinical Practice, 
               Research2Clinics Workshop @ NeurIPS 2021},
  year      = {2021}
}
```
