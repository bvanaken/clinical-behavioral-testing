import re
from enum import Enum

import utils
from test_shifts.base_shift import BaseShift


class BodyWeight(Enum):
    MORBIDLY_OBESE = 1
    OBESE = 2
    OVERWEIGHT = 3
    NORMAL = 4
    UNDERWEIGHT = 5
    NO_MENTION = 6


class BodyWeightShift(BaseShift):
    weight_mentions = {BodyWeight.MORBIDLY_OBESE: ["morbidly obese", "morbid obesity", "morbid obese"],
                       BodyWeight.OBESE: ["obese", "obesity"],
                       BodyWeight.OVERWEIGHT: ["overweight"],
                       BodyWeight.NORMAL: ["normal weight"],
                       BodyWeight.UNDERWEIGHT: ["underweight"]}

    def get_groups(self):
        return list(BodyWeight)

    def get_group_names(self):
        return [group.name for group in self.get_groups()]

    def get_shift_method(self, sample: str, group: BodyWeight):
        return self.text_to_body_weight(sample, group)

    def identify_group_in_text(self, text: str):
        for body_weight_key in self.weight_mentions:
            indicators = self.weight_mentions[body_weight_key]

            for mention in indicators:
                indicator_match = re.search(mention, text, flags=re.IGNORECASE)
                if indicator_match is not None:
                    return body_weight_key

        return BodyWeight.NO_MENTION

    def text_to_body_weight(self, text: str, body_weight: BodyWeight):
        shifted_text = text

        for body_weight_key in self.weight_mentions:
            indicators = self.weight_mentions[body_weight_key]

            for mention in indicators:
                indicator_match = re.search(mention, shifted_text, flags=re.IGNORECASE)
                if indicator_match is not None:

                    if body_weight_key == body_weight:
                        # patient already has the requested body weight
                        return text

                    else:
                        shifted_text = re.sub(mention, '', shifted_text, flags=re.IGNORECASE)

        if body_weight is BodyWeight.NO_MENTION:
            return shifted_text

        mention_insertion_position = utils.find_patient_characteristic_position_in_text(shifted_text)
        if mention_insertion_position is not None:
            weight_mention = self.weight_mentions[body_weight][0]
            shifted_text = f"{shifted_text[:mention_insertion_position]}{weight_mention} {shifted_text[mention_insertion_position:]}"

            return shifted_text
