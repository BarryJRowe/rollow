import httplib
import json

TODAQ_API_KEY = None#{{x-api-key}}
TODAQ_API_URL = "api.todaqfinance.net"

class TODAQDriver(object):
    @classmethod
    def general_request(cls, method, uri, body=None, headers_override=None):
        headers = {"Content-Type": "application/json",
                   "x-api-key": TODAQ_API_KEY}
        if headers_override:
            headers = headers_override
        conn = httplib.HTTPSConnection(TODAQ_API_URL)    
        body=json.dumps(body)
        print body
        conn.request(method, uri, body, headers)
        response = conn.getresponse()
        data = response.read()
        print data
        return json.loads(data)
        
    ########ACCOUNTS#############
    @classmethod
    def create_account_individual(cls, email, contact, **kwargs):
        body = {
         "type": "account",
         "data": {
          "attributes": {
           "account-type": "individual",
           "admin-email": email,
           #"contact": contact
          }
         }
        }

        for key in kwargs:
            body['data']['attributes'][key] = kwargs[key]
    
        response = cls.general_request("POST", "/accounts", body)
        return response

    @classmethod
    def create_account_business(cls, admin_email, business_number, 
                                business_contact, **kwargs):
        body = {
         "type": "account",
         "data": {
          "attributes": {
           "account-type": "individual",
           "admin-email": admin_email,
           "business-type": business_type,
           "business-number": business_number,
           "business-contact": business_contact
          }
         }
        }
        for key in kwargs:
            body['data']['attributes'][key] = kwargs[key]

        response = cls.general_request("POST", "/accounts", body)
        return response

    @classmethod
    def get_accounts_list(cls, page, limit):
        response = cls.general_request("GET", "/accounts?page="+str(page)+"&limit="+str(limit))
        return response

    @classmethod
    def get_account_by_id(cls, account_id):
        response = cls.general_request("GET", "/accounts/"+account_id)
        return response

    @classmethod
    def get_account_transactions(cls, account_id, page, limit):
        response = cls.general_request("GET", "/accounts/"+account_id+"/transactions?page="+str(page)+"&limit="+str(limit))
        return response

    @classmethod
    def update_account_info(cls, account_id, patch_dict):
        body = {
          "data": {
            "attributes": patch_dict    
          }
        }
        response = cls.general_request("PATCH", "/accounts/"+account_id, body)
        return response

    @classmethod
    def set_account_active(cls, account_id, is_active):
        body = {
          "data": {
            "attributes": {
              "is-active": is_active
            }
          }
        }
        response = cls.general_request("PATCH", "/accounts/"+account_id, body)
        return response

    @classmethod
    def get_account_files(cls, page, limit):
        response = cls.general_request("GET", "/accounts/"+account_id+"/files?page="+str(page)+"&limit="+str(limit))
        return response

    ###########TRANSACTIONS#############

    @classmethod
    def initiate_transaction(cls, sender, recipient, files):
        body = {
          "data": {
            "relationships": {
              "sender": sender,
              "recipient": recipient,
              "files": files
            }
          }
        }
        response = cls.generate_request("POST", "/transactions", body)
        return response

    @classmethod
    def list_transactions_api(cls, page, limit):
        response = cls.general_request("GET", "/transactions?page="+str(page)+"&limit="+str(limit))
        return response

    @classmethod
    def get_transaction_by_id(cls, transaction_id):
        response = cls.general_request("GET", "/transactions/"+transaction_id)
        return response

    @classmethod
    def get_transaction_files(cls, transaction_id):
        response = cls.general_request("GET", "/transactions/"+transaction_id+"/files?page="+str(page)+"&limit="+str(limit))
        return response
 
    @classmethod
    def get_transaction_sender(cls, transaction_id):
        response = cls.general_request("GET", "/transactions/"+transaction_id)
        return response

    @classmethod
    def get_transaction_recipient(cls, transaction_id):
        response = cls.general_request("GET", "/transactions/"+transaction_id)
        return response


    ###########FILES##################

    @classmethod
    def create_file(cls, account_id, payload):
        account_dict = {"type": "account", "id": account_id}
        body = {
                "data":{
                 "type": "file",
                 "attributes": {
                  "payload": payload,
                 },
                 "relationships": {
                  "initial-account": {
                   "data": account_dict
                  }
                 }
                }
               }
        
        output = cls.general_request("POST", "/files", body)
        return output  
 
    @classmethod
    def get_file_list(cls, page, limit):
        response = cls.general_request("GET", "/files?page="+str(page)+"&limit="+str(limit))
        return response

    @classmethod
    def get_file_by_id(cls, file_id):
        response = cls.general_request("GET", "/files/"+file_id)
        return response

    @classmethod
    def get_file_transactions(cls, file_id, page, limit):
        response = cls.general_request("GET", "/files/"+file_id+"/transactions?page="+str(page)+"&limit="+str(limit))
        return response

    @classmethod
    def get_file_proofs(cls, file_id):
        response = cls.general_request("GET", "/files/"+file_id+"/proofs?page="+str(page)+"&limit="+str(limit))
        return response
  

