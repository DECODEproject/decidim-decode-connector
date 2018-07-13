class EmptyTransactionLogException(Exception):
    def __str__(self):
        return 'Empty transaction log for this petition'
