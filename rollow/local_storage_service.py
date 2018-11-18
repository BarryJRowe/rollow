import json
from hashtree_service import HashTreeService

class LocalStorageService(object):
    filename = "localstorage.json"
    @classmethod
    def wipe_storage(cls):
        s = open(cls.filename, "w")
        s.close()

    @classmethod
    def add_local_entry(cls, created_hashdata, created_hashtree, block_id):
        s = open(cls.filename, "a")
        data = {"created_hashdata": created_hashdata,
                "created_hashtree": created_hashtree,
                "block_id": block_id}
        s.write(json.dumps(data)+"\n")

    @classmethod
    def find_evidence(cls, keywords):
        try:
            s = open(cls.filename)
        except IOError:
            return []
        evidences = list() 
        for line in s:
            data = json.loads(line)
            created_hashdata = data['created_hashdata']
            created_hashtree = data['created_hashtree']
            block_id = data['block_id']
            meta = json.loads(created_hashdata[0])
            url = meta[0]
            pop = meta[1]
            nonce = meta[2]
            elms = [0]
            for i, entry in enumerate(created_hashdata[1:]):
                this_data = json.loads(entry)
                if this_data[0] in keywords:
                    elms.append(i+1)

            if len(elms) > 1:
                evidence_data, evidence_hashtree =\
                    HashTreeService.give_selective_proof(created_hashdata,
                                                         elms)
                evidences.append({"evidence_data": evidence_data,
                                  "evidence_hashtree": evidence_hashtree,
                                  "block_id": block_id})
        return evidences           
            

