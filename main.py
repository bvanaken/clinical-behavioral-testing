import os
from typing import List

import fire as fire

import utils
from behavioral_testing import BehavioralTesting
from prediction import DiagnosisPredictor, MortalityPredictor
from test_shifts.age_shift import AgeShift
from test_shifts.ethnicity_gender_shift import GenderEthnicityShift
from test_shifts.ethnicity_shift import EthnicityShift
from test_shifts.gender_shift import GenderShift
from test_shifts.weight_shift import BodyWeightShift

SHIFT_MAP = {
    "age": AgeShift(),
    "gender": GenderShift(),
    "ethnicity": EthnicityShift(),
    "weight": BodyWeightShift(),
    "intersectional": GenderEthnicityShift()
}

TASK_MAP = {
    "diagnosis": DiagnosisPredictor,
    "mortality": MortalityPredictor
}


def run(test_set_path: str, model_path: str, shift_keys: List[str], task: str, save_dir: str = "./results",
        gpu: bool = False):
    predictor = TASK_MAP[task](checkpoint_path=model_path,
                               test_set_path=test_set_path,
                               gpu=gpu)

    bt = BehavioralTesting(test_dataset_path=test_set_path)

    utils.create_dir_if_not_exists(save_dir)

    for shift_key in shift_keys:
        shift = SHIFT_MAP[shift_key]
        stats = bt.run_test(shift, predictor, os.path.join(save_dir, f"{shift_key}_shift_{task}.csv"))
        utils.save_to_file(stats, os.path.join(save_dir, f"{shift_key}_shift_{task}_stats.txt"))


if __name__ == '__main__':
    fire.Fire(run)
