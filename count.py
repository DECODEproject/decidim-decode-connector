import click
import sys
from petition_builder import petition, zenroom_petition


class CountRequestException(Exception):
    def __str__(self):
        return 'Failed to count signatures: ' + self.message


def count_signatures(use_zenroom):
    try:
        if use_zenroom:
            number_of_signatures = zenroom_petition().count_signatures()
        else:
            number_of_signatures = petition().count_signatures()

        return {'numberOfSignatures': number_of_signatures}
    except Exception as e:
        raise CountRequestException(str(e))


def main(use_zenroom):
    try:
        results = count_signatures(use_zenroom)

        print "petition signatures counted successfully!"
        print results
    except Exception as err:
        print err
        sys.exit(-1)


@click.command()
@click.option('--zenroom/--no-zenroom', default=False)
def cli_main(zenroom):
    main(zenroom)


if __name__ == '__main__':
    cli_main()
