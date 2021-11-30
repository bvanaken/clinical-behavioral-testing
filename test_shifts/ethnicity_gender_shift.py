from enum import Enum

from test_shifts.base_shift import BaseShift
from test_shifts.ethnicity_shift import Ethnicity, EthnicityShift
from test_shifts.gender_shift import GenderShift, Gender


class IntersectionalTestCase(Enum):
    AFRICAN_AMERICAN_FEMALE = (Gender.FEMALE, Ethnicity.AFRICAN_AMERICAN)
    WHITE_MALE = (Gender.MALE, Ethnicity.WHITE)


class GenderEthnicityShift(BaseShift):

    def __init__(self):
        self.gender_shift = GenderShift()
        self.ethnicity_shift = EthnicityShift()

    def get_groups(self):
        return list(IntersectionalTestCase)

    def get_group_names(self):
        return [group.name for group in self.get_groups()]

    def get_shift_method(self, sample: str, group: IntersectionalTestCase):
        return self.text_to_ethnicity_and_gender(sample, group)

    def identify_group_in_text(self, text: str):

        identified_gender = self.gender_shift.identify_group_in_text(text)
        identified_ethnicity = self.ethnicity_shift.identify_group_in_text(text)

        for group in self.get_groups():
            gender, ethnicity = group.value
            if identified_gender is gender and identified_ethnicity is ethnicity:
                return group

        return None

    def text_to_ethnicity_and_gender(self, text: str, ethnicity_and_gender: IntersectionalTestCase):
        gender, ethnicity = ethnicity_and_gender.value

        shifted_text = self.gender_shift.text_to_gender(text, gender)
        if shifted_text is None:
            return None
        else:
            return self.ethnicity_shift.text_to_ethnicity(shifted_text, ethnicity)
