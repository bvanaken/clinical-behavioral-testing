import random
import re
from enum import Enum

import utils
from test_shifts.base_shift import BaseShift


class Gender(Enum):
    FEMALE = "F"
    MALE = "M"
    TRANS = "T"


class GenderShift(BaseShift):
    age_sub_pattern = r'(\d{2}|\[\*\*Age over 90 \*\*\])'
    female_male_table = {
        'Ms. ': 'Mr. ',
        'Ms ': 'Mr ',
        'FEMALE': 'MALE',
        'Female': 'Male',
        ' female': ' male',
        'Woman ': 'Man ',
        ' woman ': ' man ',
        ' woman.': ' man.',
        'She ': 'He ',
        ' she ': ' he ',
        ' her ': ' his ',
        'Her ': 'His ',
        'lady': 'gentleman',
        'Lady': 'Gentleman',
        'yoF': 'yoM',
        'husband': 'wife',
        r'( \d{2})F ': r'( \d{2})M ',
        r'(\d{2}|\[\*\*Age over 90 \*\*\])[ ]?F[,]? ': r'(\d{2}|\[\*\*Age over 90 \*\*\])[ ]?M[,]? ',
        r'(\d{2}|\[\*\*Age over 90 \*\*\])[ ]?yF ': r'(\d{2}|\[\*\*Age over 90 \*\*\])[ ]?yM ',
        ' F ': ' M ',
        ' f ': ' m '
    }

    transgender_indicators = ["transgender"]

    def get_groups(self):
        return [Gender.FEMALE, Gender.MALE, Gender.TRANS]

    def get_group_names(self):
        return [group.value for group in self.get_groups()]

    def get_shift_method(self, sample: str, group: Gender):
        return self.text_to_gender(sample, group)

    def identify_group_in_text(self, text: str):
        for transgender_indicator in self.transgender_indicators:
            if transgender_indicator in text:
                return Gender.TRANS

        for key in self.female_male_table:
            value = self.female_male_table[key]
            if re.search(key, text) is not None:
                return Gender.FEMALE
            elif re.search(value, text) is not None:
                return Gender.MALE

        return None

    def text_to_gender(self, text: str, gender: Gender):
        shifted_text = text
        text_is_shifted = False

        mention_insertion_position = utils.find_patient_characteristic_position_in_text(shifted_text)
        if mention_insertion_position is not None:

            if gender is not Gender.TRANS:

                for transgender_indicator in self.transgender_indicators:
                    shifted_text = shifted_text.replace(transgender_indicator, "")

                for key in self.female_male_table:

                    if gender is Gender.FEMALE:
                        query = key
                        shift_query = self.female_male_table[key]
                    elif gender is Gender.MALE:
                        query = self.female_male_table[key]
                        shift_query = key

                    if re.search(query, shifted_text) is not None:
                        # text already has chosen gender
                        return shifted_text

                    shift_match = re.search(shift_query, shifted_text)
                    if shift_match is not None:

                        if shift_match.re.groups > 0:
                            shifted_text = re.sub(shift_query, r'\1{} '.format(gender.value), shifted_text)
                        else:
                            shifted_text = re.sub(shift_query, query, shifted_text)

                        text_is_shifted = True

            else:
                for transgender_indicator in self.transgender_indicators:
                    if transgender_indicator in shifted_text:
                        # text already has chosen gender
                        return shifted_text

                transgender_mention = random.choice(self.transgender_indicators)
                shifted_text = f"{shifted_text[:mention_insertion_position]}{transgender_mention} {shifted_text[mention_insertion_position:]}"
                text_is_shifted = True

        return shifted_text if text_is_shifted else None
