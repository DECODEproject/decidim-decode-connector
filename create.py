from os import environ
import requests
import click
import json
import sys

DEFAULT_WALLET_PROXY_URL = "http://localhost:5010"


class CreateRequestException(Exception):
    def __str__(self):
        return 'Failed to create petition: ' + self.message


def get_wallet_proxy_url():
    if 'WALLET_PROXY_URL' in environ:
        return environ['WALLET_PROXY_URL']
    return DEFAULT_WALLET_PROXY_URL


def create_petition(url):
    try:
        response = requests.post(url + '/chainspace/petitions')
    except Exception as e:
        raise CreateRequestException(str(e))

    if response.status_code >= 400:
        raise CreateRequestException(response.text)
    return json.loads(response.content)


def main():
    wallet_proxy_url = get_wallet_proxy_url()

    try:
        results = create_petition(wallet_proxy_url)

        print "petition created successfully!"
        print results
    except Exception as err:
        print err
        sys.exit(-1)


@click.command()
def cli_main():
    main()


if __name__ == '__main__':
    cli_main()
