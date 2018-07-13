class Signature:

    votes_table = {
        'yes': 0,
        'no': 1
    }
    genders_table = {
        'any': 0,
        'male': 1,
        'female': 2,
        'undisclosed': 3
    }
    ages_table = {
        'any': 0,
        '0-19': 1,
        '20-29': 2,
        '30-39': 3,
        '40+': 4
    }

    def __init__(self, vote, gender, age):
        self.vote = vote
        self.gender = gender
        self.age = age

    def get_contract_signature_representation(self):
        total_signature_combinations = len(self.votes_table)\
            * len(self.genders_table)\
            * len(self.ages_table)

        signature_combination_index = self.__get_signature_combination_index()
        contract_signature_representation = [0] * total_signature_combinations
        contract_signature_representation[signature_combination_index] = 1

        return contract_signature_representation

    def __get_signature_combination_index(self):
        # Signature combination: vote-gender-age
        vote_index_offset = len(self.genders_table) * len(self.ages_table)
        genders_index_offset = len(self.ages_table)

        vote_index = self.__get_vote_index()
        gender_index = self.__get_gender_index()
        age_index = self.__get_age_index()

        signature_combination_index = (vote_index_offset * vote_index)\
            + (genders_index_offset * gender_index)\
            + age_index
        return signature_combination_index

    def __get_vote_index(self):
        vote = self.vote.lower()

        if vote not in self.votes_table:
            raise Exception("this vote option does not exist please vote 'yes' or 'no'")

        return self.votes_table[vote]

    def __get_gender_index(self):
        gender = self.gender.lower()

        if gender not in self.genders_table:
            raise Exception("this gender option does not exist please choose 'female' or 'male' or 'any' or 'undisclosed'")

        return self.genders_table[gender]

    def __get_age_index(self):
        age = self.age.lower()

        if age not in self.ages_table:
            raise Exception("this age option does not exist please choose '0-19' or '20-29' or '30-39' or '40+' or 'any'")

        return self.ages_table[age]
