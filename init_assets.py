import sys
import random
import logging
import os.path

import bigchaindb
import bigchaindb.config_utils

import apps_config
from server.lib.models.accounts import Account
from server.lib.models.assets import create_asset

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    CONFIG_FILE = os.environ['BIGCHAINDB_CONFIG']
except KeyError:
    CONFIG_FILE = os.path.join(os.path.dirname(__file__), '.bigchaindb_examples')

APPS = apps_config.APPS


def get_bigchain(conf=CONFIG_FILE):
    if os.path.isfile(conf):
        bigchaindb.config_utils.autoconfigure(filename=conf, force=True)

    return bigchaindb.Bigchain()

bigchain = get_bigchain()
logging.info('INIT: bigchain initialized with database: {}'.format(bigchaindb.config['database']['name']))


def main(ledger_number=''):

    for app in APPS:
        accounts = []
        app_name = '{}'.format(app['name'])
        for i in range(app['num_accounts']):
            account = Account(bigchain=bigchain,
                              name='account_{}'.format(i),
                              ledgers=[bigchaindb.config['database']['name']],
                              db=app_name)
            accounts.append(account)

        logging.info('INIT: {} accounts initialized for app: {}'.format(len(accounts), app_name))

        assets = []
        for i in range(app['num_assets']):
            asset = create_asset(bigchain=bigchain,
                                 to=accounts[random.randint(0, app['num_accounts'] - 1)].vk,
                                 payload=app['payload_func'](i))
            assets.append(asset)
        logging.info('INIT: {} assets initialized for app: {}'.format(len(assets), app_name))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
