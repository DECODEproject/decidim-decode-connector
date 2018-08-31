from src.exceptions.tally_closed_petition_exception import TallyClosedPetitionException
import json


class ZenroomPetition:

    def __init__(self, chainspace_repository, contract, keyfile):
        self.chainspace_repository = chainspace_repository
        self.contract = contract
        self.keyfile = keyfile

        self.reference_inputs = None
        self.parameters = None

    def initialize(self):
        petition_token = self.__initialize_contract()
        new_petition_object = self.__create_petition(petition_token)
        return new_petition_object

    def __initialize_contract(self):
        transaction = self.contract.init()
        self.chainspace_repository.process_transaction(transaction)
        return transaction['transaction']['outputs'][0]

    def __create_petition(self, petition_token):
        inputs = (petition_token,)

        votes = ['YES', 'NO']
        # gender = ['ANY', 'M', 'F', 'U']
        # age = ['ANY', '0-19', '20-29', '30-39', '40+']
        # options = ["%s-%s-%s" % (v, g, a) for v in votes for g in gender for a in age]
        options = votes

        transaction = self.contract.create_petition(
            inputs,
            self.reference_inputs,
            self.parameters,
            options,
            self.keyfile
        )
        self.chainspace_repository.process_transaction(transaction)
        return transaction['transaction']['outputs'][1]
