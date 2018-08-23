from petition_builder import petition


class CountRequestException(Exception):
    def __str__(self):
        return 'Failed to count signatures: ' + self.message


def count_signatures():
    try:
        number_of_signatures = petition(('', '')).count_signatures()

        return {'numberOfSignatures': number_of_signatures}
    except Exception as e:
        raise CountRequestException(str(e))
