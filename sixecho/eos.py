#  from pyeos_client.EOSChainApi import ChainAPI
#  from pyeos_client.EOSWalletApi import WalletAPI
#  from pyeos_client.NodeosConnect import RequestHandlerAPI
import datetime as dt
import json
import os

import eospy.cleos
import pytz


def test_eos():
    ce = eospy.cleos.Cleos(url='http://localhost:8888')

    # cleos push action hello hi '["bob"]' -p bob@active
    arguments = {"user": 'bob'}
    payload = {
        "account": "hello",
        "name": "hi",
        "authorization": [{
            "actor": "bob",
            "permission": "active",
        }],
    }

    data = ce.abi_json_to_bin(payload['account'], payload['name'], arguments)

    print(data)

    payload['data'] = data['binargs']
    print(payload)
    trx = {"actions": [payload]}
    import datetime as dt
    trx['expiration'] = str(
        (dt.datetime.utcnow() +
         dt.timedelta(seconds=60)).replace(tzinfo=pytz.UTC))

    key = eospy.keys.EOSKey(
        '5KDA5SewCxdFBSfiLKBnmNZR7PBZ3jZbtLpPhqhwi1LZ2dAHkAu')
    print(trx)
    resp = ce.push_transaction(trx, key, broadcast=True)

    print('------------------------------------------------')
    print(resp)
    print('------------------------------------------------')


class EOS(object):
    """
    EOS class
    """
    def __init__(self, private_key=None, host_url=None):
        """
        """
        self.private_key = private_key
        self.host_url = host_url

    def push_transaction(self, owner, authorization, digital_content):
        """
        upload digital content to server
        """
        ce = eospy.cleos.Cleos(url=self.host_url)
        payload = {
            "account": "assets",
            "name": "create",
            "authorization": authorization,
        }
        idata = json.dumps({
            "digest": digital_content.digest,
            "sha256": digital_content.sha256,
            "size_file": digital_content.file_size,
            "type": digital_content.type
        })
        mdata = json.dumps(digital_content.meta_media)

        arguments = {
            "author": owner,
            "category": digital_content.meta_media["category_id"],
            "owner": owner,
            "idata": idata,
            "mdata": mdata,
            "requireclaim": 0
        }
        data = ce.abi_json_to_bin(payload["account"], payload["name"],
                                  arguments)
        payload['data'] = data['binargs']
        trx = {"actions": [payload]}
        trx['expiration'] = str(
            (dt.datetime.utcnow() +
             dt.timedelta(seconds=60)).replace(tzinfo=pytz.UTC))
        key = eospy.keys.EOSKey(self.private_key)
        resp = ce.push_transaction(trx, key, broadcast=True)
        return resp

    def get_transaction(self):
        """
        """
        print("coming soon")
