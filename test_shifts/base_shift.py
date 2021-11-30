from enum import Enum
from typing import List, Union


class BaseShift:

    def make_shift(self, samples: List[str], return_stats=False):
        shift_groups = []
        stats = {"total_samples": len(samples)}

        skip_samples_indices = set()
        for group in self.get_groups():

            samples_in_group = []

            for i, sample in enumerate(samples):
                shifted_sample = self.get_shift_method(sample, group)

                if shifted_sample is None:
                    skip_samples_indices.add(i)
                samples_in_group.append(shifted_sample)

            filtered_samples = [samp for j, samp in enumerate(samples_in_group) if j not in skip_samples_indices]
            shift_groups.append(filtered_samples)

        stats["skipped_samples"] = skip_samples_indices
        stats["total_included_samples"] = len(samples) - len(skip_samples_indices)

        if return_stats:
            return shift_groups, stats
        else:
            return shift_groups

    def get_groups(self):
        raise NotImplementedError

    def get_group_names(self):
        raise NotImplementedError

    def get_shift_method(self, sample: str, group: Union[Enum, str]):
        raise NotImplementedError

    def identify_group_in_text(self, text):
        raise NotImplementedError
