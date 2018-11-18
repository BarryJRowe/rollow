import tornado.web
import json
import random
import datetime
from html_keyword_service import KeyWordHTMLService
from hashtree_service import HashTreeService
from blockchain_service import BlockChainService
from local_storage_service import LocalStorageService
from expertise_summary_service import ExpertiseSummaryService
from third_party_service import ThirdPartyService
from second_party_service import SecondPartyService
from first_party_service import FirstPartyService
from main_service import MainService

account_id = "a3d55f0f-b139-4d80-aba6-016b07285f97"

class BlockChainHandler(tornado.web.RequestHandler):
    pass

class HTMLHandler(BlockChainHandler):
    def post(self):
        data = json.loads(self.request.body)
        html = data['html']
        url = data['url']
        #account_id = data['account_id']
        timestamp = str(datetime.datetime.now())

        keyword_positions, keyword_totals = KeyWordHTMLService.get_keyword_positions(html)
        #print keyword_positions       
        
        created_hashdata = HashTreeService.form_hash_data(keyword_positions,
                                                          url, timestamp)
        created_hashtree = HashTreeService.get_hashtree(created_hashdata)

        #create proof_of_purchase
        block_id = BlockChainService.add_entry_to_chain(account_id, 
                                                        created_hashtree)
        LocalStorageService.add_local_entry(created_hashdata, 
                                            created_hashtree,
                                            block_id)
        self.write(json.dumps({"status": "ok"}))


class ExpertiseHandler(BlockChainHandler):
    def post(self):
        body = json.loads(self.request.body)
        keywords = body['keywords']
        #account_id = "..."
       
        evidences = LocalStorageService.find_evidence(keywords)
        #individual evidence: [url, blockid, timestamp, proof_of_purchase]??
        self.write(json.dumps(evidences))


class ExpertiseSummaryHandler(BlockChainHandler):
    def post(self):
        body = json.loads(self.request.body)
        keywords = body['keywords']
        #account_id = body['account']

        evidences = LocalStorageService.find_evidence(keywords)
        summary = ExpertiseSummaryService.find_summary(evidences)

class SecondPartyHandler(BlockChainHandler):
    def get(self):
        html = SecondPartyService.get_second_party_attestations(account_id)
        self.write(html)

class ThirdPartyHandler(BlockChainHandler):
    def get(self):
        html = ThirdPartyService.get_third_party_attestations(account_id)
        self.write(html)
 
    def post(self):
        body = json.loads(self.request.body)
        request_type = body.get("type", "email_verification")
        third_party = body.get("3rd_party", "email_mock")
        account_id = body.get("account_id")
        request_data = body.get("request_data")
        ThirdPartyService.call_third_party(request_type, third_party,
                                           account_id, request_data)
        self.write({"status": "ok"})
      

class AccountCreateHandler(BlockChainHandler):
    def post(self):
        body = json.loads(self.request.body)
        admin_email = body.get("admin_email", body['email'])
        contact = {
          "phone": body['phone'],
          "email": body['email'],
          "first-name": body['first_name'],
          "last-name": body['last_name'],
          "address": {
            "city": body['city'],
            "country": body['country'],
            "postal-code": body['postal_code'],
            "province-region": body['province_region'],
            "street-address-1": body['address1'],
            "street-address-2": body['address2']
          }
        }

        BlockChainService.create_account(admin_email, contact)

class AttestationsHandler(BlockChainHandler):
    def get(self):
        pass

    def post(self):
        pass

class GetAttestationsHandler(BlockChainHandler):
    def get(self):
        pass

class MainHandler(BlockChainHandler):
    def get(self):
        #acacount_id = "aaaa"
        html = MainService.render_landing(account_id)
        
        self.write(html)

class FirstPartyHandler(BlockChainHandler):
    def get(self):
        keywords = self.get_argument("keywords").split()
        evidences = LocalStorageService.find_evidence(keywords)
        
        html = FirstPartyService.render_html(evidences, keywords)
        self.write(html)

    def post(self):
        print 'bbbbbbbbbbbbbbbbbbbb'
        pass 

def main():
    app = tornado.web.Application([
        (r"/", MainHandler),
        #1st-party
        (r"/html", HTMLHandler),
        (r"/expertise", ExpertiseHandler),
        (r"/expertise_summary", ExpertiseSummaryHandler),
        (r"/1st_party", FirstPartyHandler),
        #2nd-party
        (r"/attestations", AttestationsHandler),
        (r"/get_attestations", GetAttestationsHandler),
        #3rd-party
        (r"/2nd_party", SecondPartyHandler),
        (r"/3rd_party", ThirdPartyHandler),
        #settings/administration
        (r"/create_account", AccountCreateHandler),
    ])
    app.listen(1331)
    tornado.ioloop.IOLoop.current().start()

if __name__=='__main__':
    main()


