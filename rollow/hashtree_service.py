import hashlib
import json
import random

class HashTreeService(object):
    @classmethod
    def nonce(cls):
        return cls.hash_func(str(random.random()))[0:8]

    @classmethod
    def hash_func(cls, string):
        return hashlib.sha224(string).hexdigest()

    @classmethod
    def form_hash_data(cls, keyword_positions, url, pop):
        key_list = keyword_positions.keys()
        key_list.sort(key=lambda x: (-len(keyword_positions[x]), x))

        output = [[x, keyword_positions[x], cls.nonce()] for x in key_list]
        output.insert(0, [url, pop, cls.nonce()])
        output = [json.dumps(x) for x in output]
        return output

    @classmethod
    def get_hashtree(cls, data_list):
        hash_entries = [[cls.hash_func(x) for x in data_list]]
        while len(hash_entries[-1]) > 1:
            hash_entries.append(list())
            cur_append = list()
            for entry in hash_entries[-2]:
                if not cur_append:
                    cur_append.append(entry)
                else:
                    hash_entries[-1].append(cls.hash_func(cur_append[0]+entry))
                    cur_append = list()
            if cur_append:
                hash_entries[-1].append(cls.hash_func(cur_append[0]))
        return hash_entries
                
    @classmethod
    def give_selective_proof(cls,created_data, elms): 
        full_hash_tree = cls.get_hashtree(created_data)

        new_data = list()
        for i, data in enumerate(created_data):
            if i in elms:#this is a kept element
                new_data.append(data)
            else:
                new_data.append("")

        selective_hash_tree = list()
        for depth, level in enumerate(full_hash_tree):
            selective_hash_tree.append([])
           
            for i in range(len(level)):
                #j = int(i/2**(depth+1))*(2**(depth+1))
                j = int(i/2)*(2**(depth+1))

                checks = range(j,j+2**(depth+1))
              
                for c in checks:
                    if c<len(new_data) and new_data[c]:
                        selective_hash_tree[-1].append(level[i])
                  
                        break
                else:
                    selective_hash_tree[-1].append("")
         
        #print "==================="
        #print new_data
        #print ""
        #print selective_hash_tree
                
           
        #return new_data, full_hash_tree
        return new_data, selective_hash_tree

   

def main():
    d= {"a": [0,1],
        "b": [2],
        "c": [5, 8],
        "d": [5,7,8],
        "e": [8,4,2],
        "f": [0,1],
        "g": [1]}
    nonce = '1'
    pop = None
    url = "http://hello.com"

    #created_data = HashTreeService.form_hash_data(d, url, pop, nonce)
    #created_hashtree = HashTreeService.get_hashtree(created_data)

    print HashTreeService.hash_func("aab")
    import pdb
    pdb.set_trace()
    

if __name__=='__main__':
    main()
