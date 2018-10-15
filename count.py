import click
import sys
from petition_builder import zenroom_petition


class CountRequestException(Exception):
    def __str__(self):
        return 'Failed to count signatures: ' + self.message


def count_signatures():
    try:
        number_of_signatures = zenroom_petition().count_signatures()

        return {'numberOfSignatures': number_of_signatures}
    except Exception as e:
        raise CountRequestException(str(e))


def main():
    try:
        results = count_signatures()

        print "petition signatures counted successfully!"
        print results
    except Exception as err:
        print err
        sys.exit(-1)


@click.command()
def cli_main():
    main()


if __name__ == '__main__':
    cli_main()
