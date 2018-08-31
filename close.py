from os import environ
import requests
import click
import sys
from read_keys import load_keys
from petition_builder import petition, zenroom_petition

DEFAULT_DECIDIM_MOCK_URL = "http://localhost:3040"


class TallyRequestException(Exception):
    def __str__(self):
        return 'Failed to request tally: ' + self.message


class CloseRequestException(Exception):
    def __str__(self):
        return 'Failed to close Decidim petition: ' + self.message


def get_decidim_mock_url():
    if 'DECIDIM_MOCK_URL' in environ:
        return environ['DECIDIM_MOCK_URL']
    return DEFAULT_DECIDIM_MOCK_URL


def request_tally(key_pair, use_zenroom):
    try:
        if use_zenroom:
            outcome = zenroom_petition(key_pair).get_results()
        else:
            outcome = petition(key_pair).get_results()

        return {
            'yes': outcome[0],
            'no': outcome[1]
        }
    except Exception as e:
        raise TallyRequestException(str(e))


def decidim_close(url, results):
    try:
        response = requests.post(url + '/close', json=results)
    except Exception as e:
        raise CloseRequestException(str(e))

    if response.status_code >= 400:
        raise CloseRequestException(response.text)


def main(keyfile, use_zenroom):
    try:
        decidim_mock_url = get_decidim_mock_url()

        if use_zenroom:
            results = request_tally(keyfile, use_zenroom)
        else:
            key_pair = load_keys(keyfile)
            results = request_tally(key_pair, use_zenroom)

        decidim_close(decidim_mock_url, results)

        print "petition closed successfully!"
        print results
    except Exception as err:
        print err
        sys.exit(-1)


@click.command()
@click.option('--keyfile', default='/keys/key.json', help='Seed for key generation')
@click.option('--zenroom/--no-zenroom', default=False)
def cli_main(keyfile, zenroom):
    main(keyfile, zenroom)


if __name__ == '__main__':
    cli_main()
