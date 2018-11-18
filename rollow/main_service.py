from tornado.template import Template
from blockchain_service import BlockChainService

landing_template = Template(open("./templates/landing.html").read())

class MainService(object):
    @classmethod
    def render_landing(cls, account_id):
        #account_data = BlockChainService.get_account(account_id)['data']['attributes']
        account_data = {"first-name": "Barry",
                        "last-name": "Rowe",
                        "contact": {"email": "barry@whoknows.com"}
                       }
        first_name = account_data['first-name']
        last_name = account_data['last-name']
        email = account_data['contact']['email']
        return landing_template.generate(account_id=account_id,
                                         first_name=first_name,
                                         last_name=last_name,
                                         email=email
                                        )

    @classmethod
    def pas(cls):
        pass
