import datetime
from src.transaction import Transaction
from src.exceptions.empty_transaction_log_exception import EmptyTransactionLogException


class TransactionLog(list):

    def filter_by_contract_name(self, contract_name):
        filtered_transaction_log = filter(
            lambda transaction: transaction['transactionJson']['contractID'] == contract_name,
            self
        )

        return self.__class__(filtered_transaction_log)

    def filter_by_method_name(self, method_name):
        filtered_transaction_log = filter(
            lambda transaction: transaction['transactionJson']['methodID'] == method_name,
            self
        )

        return self.__class__(filtered_transaction_log)

    def get_last_transaction(self):
        if not len(self):
            raise EmptyTransactionLogException()

        def parse_timestamp(x):
            return datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f')

        sorted_transaction_log = sorted(self,
                                        key=lambda x: parse_timestamp(x['timestamp']),
                                        reverse=True)
        last_transaction = sorted_transaction_log[0]['transactionJson']

        return Transaction(last_transaction)
