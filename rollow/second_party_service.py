from blockchain_service import BlockChainService
import datetime
from tornado.template import Template

second_party_template = Template(open("./templates/second_party.html").read())

class SecondPartyService(object):
    @classmethod
    def call_second_party(cls, request_type, third_party, account_id,
                         request_data):
        if request_type == "email_verification":
            EmailVerification.call_email_verification(third_party,
                                                      request_data)
    @classmethod
    def get_second_party_attestations(cls, account_id):
        return second_party_template.generate()
        for file_obj in BlockChainService.get_account_total_files(cls,
                                                           account_id):
            pass          

class EmailVerificaion(object):
    email_mock_account_id = ""

    @classmethod
    def call_email_verification(cls, third_party, account_id, request_data):
        if third_party == "email_mock":
            #just do it ourselves
            email_to_verify = request_data['email_to_verify']
            #assume it's verified now...
            #add verified email to blockchain
            # create file
            verifier_id = cls.email_mock_account_id

            file_data = {"attestation": "3rd-party",
                         "type": "email_verification",
                         "3rd-party_verifier": "email_mock",
                         "verifier_id": verifier_id,
                         "requester": account_id,
                         "timestamp": str(datedate.datetime.now())}
            file_id = BlockChainService.add_general_file(verifier_id,
                                                         file_data)
            #send to user 
            BlockChainService.send_file_to_account(verifier_id, 
                                                   account_id,
                                                   the_file)
        else:
            #no other verifiers for now...
            pass
