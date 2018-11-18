import re
import os

class KeyWordHTMLService(object):
    @classmethod
    def get_keyword_positions(cls, html):
        visible_text = get_visible_text(html)

        keywords_positions = dict()
        keywords_totals = dict()

        spliter = visible_text.split()
        for i, sp in enumerate(spliter):
            if sp not in keywords_positions:
                keywords_positions[sp] = list()
            keywords_positions[sp].append(i)
            keywords_totals[sp] = keywords_totals.get(sp, 0)+1

        sorted_keys = keywords_positions.keys()
        
        sorted_keys.sort(key=lambda x: -len(keywords_positions[x]))
        sorted_keys = sorted_keys[:100]
        new_pos = dict()
        new_totals = dict()
        for key in sorted_keys:
            new_pos[key] = keywords_positions[key]
            new_totals[key] = keywords_totals[key]
        return new_pos, new_totals

def get_visible_text(html):
    return " ".join([t.strip() for t in re.findall(r"<[^>]+>|[^<]+",html) if not '<' in t])

def main():
    keyword = "bitcoin"
    for filename in os.listdir("../htmls"):
        if ".html" in filename:
            print filename
            html = open("../htmls/"+filename).read()
            pos, tot = KeyWordHTMLService.get_keyword_positions(html)
            for keyw in tot:
                if keyw.lower() == keyword:
                    print [keyw, tot.get(keyw)]
if __name__=='__main__':
    main()
