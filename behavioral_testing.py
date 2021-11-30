import pandas as pd

from test_shifts.base_shift import BaseShift
from prediction import Predictor


class BehavioralTesting:
    def __init__(self,
                 test_dataset_path: str,
                 text_label="text"):
        self.test_dataset_path = test_dataset_path
        self.test_df = pd.read_csv(test_dataset_path)
        self.text_label = text_label

    def run_test(self, shift: BaseShift, predictor: Predictor, save_path: str):
        shift_groups = shift.get_group_names()

        shifted_samples, stats = shift.make_shift(samples=self.test_df[self.text_label].values, return_stats=True)

        groups = dict(zip(shift_groups, shifted_samples))

        for group_name in groups:
            predictor.predict_group(groups[group_name], group_name)

        predictor.save_results(save_path)
        return stats
