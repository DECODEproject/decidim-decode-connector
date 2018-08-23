from petition_builder import petition


def count_signatures():
    number_of_signatures = petition(('', '')).count_signatures()

    return {'numberOfSignatures': number_of_signatures}
