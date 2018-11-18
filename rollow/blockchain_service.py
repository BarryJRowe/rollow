from todaq_driver import TODAQDriver
from hashtree_service import HashTreeService
import random

class BlockChainService(object):
    @classmethod
    def create_account(cls, email, contact, **kwargs):
        res = TODAQDriver.create_account_individual(email, contact, 
                                                    **kwargs)
        return res['data'][0]['id']#created account id

    @classmethod
    def get_accounts(cls):
        accounts = TODAQDriver.get_accounts_list(1, 1000)
        return accounts['data']

    @classmethod
    def get_account(cls, account_id):
        account = TODAQDriver.get_account_by_id(account_id)
        return account

    @classmethod
    def add_entry_to_chain(cls, account_id, created_hashtree):
        payload = {"attestation": "1st-party",
                   "type": "browsing_data",
                   "created_hashtree_root": created_hashtree[-1]}
        block_id = TODAQDriver.create_file(account_id, payload)
        block_id = {"cmr": HashTreeService.hash_func(str(random.random())),
                    "status": "success"
                   }
        return block_id
 
    @classmethod
    def get_account_total_files(cls, account_id):
        res = TODAQDriver.get_account_files(account_id)
        return len(res)

    @classmethod
    def get_account_files(cls, account_id):
        res = TODAQDriver.get_account_files(account_id)
        return res

    @classmethod
    def add_general_file(cls, account_id, file_data):
        output = TODAQDriver.create_file(account_id, file_data)
        file_id = output['data'][0]['id']
        return file_id

    @classmethod
    def send_file_to_account_id(cls, sender, reciever, the_file):
        TODAQDriver.initiate_transaction(cls, sender, recipient, [the_file])

        


