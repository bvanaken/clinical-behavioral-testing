import re

from test_shifts.base_shift import BaseShift


class AgeShift(BaseShift):
    age_sub_pattern = r'(\d{2}|\[\*\*Age over 90 \*\*\])'
    age_patterns = [
        rf'{age_sub_pattern}([ ]?M[,]? )',
        rf'{age_sub_pattern}([ ]?F[,]? )',
        rf'{age_sub_pattern}([ ]?y\/o)',
        rf'{age_sub_pattern}([ ]?yo)',
        rf'{age_sub_pattern}(-yo)',
        rf'{age_sub_pattern}(y )',
        rf'{age_sub_pattern}([ ]?y\.o[\.]?)',
        rf'{age_sub_pattern}([ ]?yF)',
        rf'{age_sub_pattern}([ ]?yM)',
        rf'{age_sub_pattern}( year old)',
        rf'{age_sub_pattern}(-year-old)',
        rf'{age_sub_pattern}(-year old)',
        rf'{age_sub_pattern}( year-old)',
    ]

    age_patterns_compiled = [re.compile(pattern, flags=re.IGNORECASE) for pattern in age_patterns]

    age_groups = [str(i) for i in range(18, 90)] + ["[**Age over 90 **]"]

    def __init__(self, age_values=None):
        if age_values is not None:
            self.age_groups = age_values

    def get_groups(self):
        return self.age_groups

    def get_group_names(self):
        return self.get_groups()

    def get_shift_method(self, sample, group):
        return self.text_to_age(sample, group)

    def identify_group_in_text(self, text: str):
        for pattern in self.age_patterns_compiled:

            age_match = re.search(pattern, text)
            if age_match is not None:
                span = age_match.regs[1]
                return text[span[0]:span[1]]

        return None

    def text_to_age(self, text, age: str):
        age_indicator_found = False
        shifted_text = text

        for pattern in self.age_patterns_compiled:

            age_match = re.search(pattern, text)
            if age_match is not None:
                age_indicator_found = True

                shifted_text = re.sub(pattern, r'{}\2'.format(age), shifted_text)

        return shifted_text if age_indicator_found else None
