import re
from enum import Enum
import random

import utils
from test_shifts.base_shift import BaseShift


class Ethnicity(Enum):
    AFRICAN_AMERICAN = 1
    WHITE = 2
    ASIAN = 3
    HISPANIC = 4
    NO_MENTION = 5


class EthnicityShift(BaseShift):
    ethnicity_indicators = [" african american",
                            " african-american",
                            " african - american",
                            "black (male)",
                            "black (man)",
                            "black (gentleman)",
                            "black (female)",
                            "black (woman)",
                            "black (lady)",
                            "caucasian",
                            "white (male)",
                            "white (man)",
                            "white (gentleman)",
                            "white (female)",
                            "white (woman)",
                            "white (lady)",
                            " hispanic",
                            " asian"]

    ethnicity_addons = {Ethnicity.WHITE: ["white", "White", "Caucasian", "caucasian"],
                        Ethnicity.AFRICAN_AMERICAN: ["african american", "African American", "African-American"],
                        Ethnicity.HISPANIC: ["hispanic", "Hispanic"],
                        Ethnicity.ASIAN: ["Asian", "asian"]}

    def get_groups(self):
        return list(Ethnicity)

    def get_group_names(self):
        return [group.name for group in self.get_groups()]

    def get_shift_method(self, sample: str, group: Ethnicity):
        return self.text_to_ethnicity(sample, group)

    def identify_group_in_text(self, text: str):
        for ethnicity_key in self.ethnicity_addons:
            indicators = self.ethnicity_addons[ethnicity_key]

            for mention in indicators:
                indicator_match = re.search(mention, text, flags=re.IGNORECASE)
                if indicator_match is not None:
                    return ethnicity_key

        return Ethnicity.NO_MENTION

    def text_to_ethnicity(self, text: str, ethnicity: Ethnicity):
        shifted_text = text

        for indicator in self.ethnicity_indicators:
            indicator_match = re.search(indicator, shifted_text, flags=re.IGNORECASE)
            if indicator_match is not None:
                if indicator_match.re.groups > 0:
                    shifted_text = re.sub(indicator, r'\1', shifted_text, flags=re.IGNORECASE)
                else:
                    shifted_text = re.sub(indicator, "", shifted_text, flags=re.IGNORECASE)

        if ethnicity is Ethnicity.NO_MENTION:
            return shifted_text

        mention_insertion_position = utils.find_patient_characteristic_position_in_text(shifted_text)
        if mention_insertion_position is not None:
            ethnicity_mention = random.choice(self.ethnicity_addons[ethnicity])
            shifted_text = f"{shifted_text[:mention_insertion_position]}{ethnicity_mention} {shifted_text[mention_insertion_position:]}"

            return shifted_text
