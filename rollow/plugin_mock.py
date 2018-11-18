import os
import json
import httplib
import datetime
import time
import random

class PluginMock(object):
    @classmethod
    def import_html(cls, url, html, account_id):
        body = json.dumps({
          "html": html,
          "url": url,
          "account_id": account_id,
          "timestamp": str(datetime.datetime.now())
        }) 
        conn = httplib.HTTPConnection("localhost", 1331)
        conn.request("POST", "/html", body)
        rep = conn.getresponse()
        res = rep.read()
        return res

def wikify(name):
    name = name.lower()
    name = name[0].upper()+name[1:]
    name = name.strip().replace(" ", "_")
    return "http://en.wikipedia.org/wiki/"+name

def main(wait=False):
    account_id = ""
    for filename in os.listdir("../htmls"):
        if ".html" in filename:
            html = open("../htmls/"+filename).read()
            url = wikify(filename.split("-")[0].strip())
            PluginMock.import_html(url, html, account_id)
            timeframe = int(3+20*random.random())*60
            print filename, url, len(html) 
            if wait:
                print "Sleeping for "+str(timeframe)+" seconds..."
                time.sleep(timeframe)

if __name__=="__main__":
    main(wait=False)
