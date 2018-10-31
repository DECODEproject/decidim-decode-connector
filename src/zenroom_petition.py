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

    def count_signatures(self):
        contract_name = self.contract.contract.contract_name

        transaction_log = self.chainspace_repository.get_full_transaction_log()
        contract_transactions = transaction_log.filter_by_contract_name(contract_name)
        add_signature_transactions = contract_transactions.filter_by_method_name('add_signature')

        return len(add_signature_transactions)

    def get_results(self):
        inputs = [self.__get_chainspace_objects_of_last_transaction()[-1]]

        try:
            transaction = self.contract.tally(
                inputs,
                self.reference_inputs,
                self.parameters,
                self.keyfile
            )
        except Exception as err:
            if str(err) == "'scores'":
                raise TallyClosedPetitionException()
            raise

        self.chainspace_repository.process_transaction(transaction)

        outcome = json.loads(transaction['transaction']['outputs'][0])['outcome']

        result_yes = reduce((lambda x, y: x + y), outcome[:len(outcome) / 2])
        result_no = reduce((lambda x, y: x + y), outcome[len(outcome) / 2:])

        return [result_yes, result_no]

    def __initialize_contract(self):
        transaction = self.contract.init()
        self.chainspace_repository.process_transaction(transaction)
        return transaction['transaction']['outputs'][0]

    def __create_petition(self, petition_token):
        inputs = (petition_token,)

        votes = ['YES', 'NO']
        gender = ['ANY', 'M', 'F', 'O']
        age = ['ANY', '0-19', '20-29', '30-39', '40+']
        district = ['ANY', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        options = ["%s-%s-%s-%s" % (v, g, a, d) for v in votes for g in gender for a in age for d in district]

        transaction = self.contract.create_petition(
            inputs,
            self.reference_inputs,
            self.parameters,
            options,
            self.keyfile
        )
        self.chainspace_repository.process_transaction(transaction)
        return transaction['transaction']['outputs'][1]

    def __get_chainspace_objects_of_last_transaction(self):
        contract_name = self.contract.contract.contract_name

        transaction_log = self.chainspace_repository.get_full_transaction_log()
        contract_transactions = transaction_log.filter_by_contract_name(contract_name)
        last_transaction = contract_transactions.get_last_transaction()
        return last_transaction.extract_chainspace_objects()
