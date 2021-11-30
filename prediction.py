from typing import List
import torch

import numpy as np
import pandas as pd
from transformers import AutoModelForSequenceClassification, AutoTokenizer

import utils


class Predictor:
    result_df = None

    def predict_group(self, samples: List[str], group_name: str):
        raise NotImplementedError

    def save_results(self, save_path: str):
        raise NotImplementedError


class TransformerPredictor(Predictor):

    def __init__(self, checkpoint_path: str):
        self.model = AutoModelForSequenceClassification.from_pretrained(checkpoint_path)
        self.tokenizer = AutoTokenizer.from_pretrained(checkpoint_path)

    def inference_from_texts(self, input_texts: List[str]):
        tokenized_input = self.tokenizer(input_texts, return_tensors="pt", padding=True, truncation=True,
                                         max_length=512)
        output = self.model(**tokenized_input)
        return output.logits.detach()

    def predict_group(self, samples: List[str], group_name: str):
        raise NotImplementedError

    def save_results(self, save_path: str):
        raise NotImplementedError


class DiagnosisPredictor(TransformerPredictor):

    def __init__(self, checkpoint_path: str, test_set_path: str, gpu: bool = False, code_label: str = "short_codes",
                 **args):
        super().__init__(checkpoint_path)

        self.gpu = gpu

        self.code_filter = utils.codes_that_occur_n_times_in_dataset(n=100, dataset_path=test_set_path,
                                                                     code_label=code_label)
        self.label_list = list(self.model.config.label2id.keys())
        self.label_list_filter = [self.label_list.index(label) for label in self.code_filter]

        self.result_df = pd.DataFrame(columns=["group"] + self.code_filter)

    def reset_results(self):
        self.result_df = pd.DataFrame(columns=["group"] + self.code_filter)

    def predict_group(self, samples: List[str], group_name: str):
        logits_all_batches = self.inference_from_texts(samples)

        result_batch = torch.sigmoid(logits_all_batches)

        all_probs_per_label = []
        for result in result_batch:
            prob_per_label = [result[i] for i in self.label_list_filter]
            all_probs_per_label.append(prob_per_label)

        all_probs_per_label = np.array(all_probs_per_label)
        mean_prob_per_label = np.mean(all_probs_per_label, axis=0)

        df_row = dict(zip(self.code_filter, mean_prob_per_label))
        df_row["group"] = group_name
        self.result_df = self.result_df.append(df_row, ignore_index=True)

    def save_results(self, save_path):
        self.result_df.to_csv(save_path, index=False, float_format="%.4f")
        self.reset_results()


class MortalityPredictor(TransformerPredictor):

    def __init__(self, checkpoint_path: str, gpu: bool = False, **args):
        super().__init__(checkpoint_path)

        self.gpu = gpu
        self.result_df = pd.DataFrame(columns=["group"])

    def reset_results(self):
        self.result_df = pd.DataFrame(columns=["group"])

    def predict_group(self, samples: List[str], group_name: str):
        logits_all_batches = self.inference_from_texts(samples)
        result_batch = torch.softmax(logits_all_batches, dim=1)

        all_probs = []

        for result in result_batch:
            all_probs.append(result[1].item())

        all_probs = np.array(all_probs)
        mean_prob = np.mean(all_probs, axis=0)

        df_row = {"group": group_name, "mortality_risk": mean_prob}
        self.result_df = self.result_df.append(df_row, ignore_index=True)

    def save_results(self, save_path: str):
        self.result_df.to_csv(save_path, index=False, float_format="%.4f")
        self.reset_results()
