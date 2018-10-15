import click
import sys
from petition_builder import zenroom_petition


class CreateRequestException(Exception):
    def __str__(self):
        return 'Failed to create petition: ' + self.message


def create_petition(key_pair):
    try:
        our_object = zenroom_petition(key_pair).initialize()
        petitionObjectID = our_object.object_id
        result = {'petitionObjectId': petitionObjectID}

        return result
    except Exception as e:
        raise CreateRequestException(str(e))


def main(keyfile):
    try:
        results = create_petition(keyfile)

        print "petition created successfully!"
        print results
    except Exception as err:
        print err
        sys.exit(-1)


@click.command()
@click.option('--keyfile', default='/keys/key.json', help='Seed for key generation')
def cli_main(keyfile):
    main(keyfile)


if __name__ == '__main__':
    cli_main()
