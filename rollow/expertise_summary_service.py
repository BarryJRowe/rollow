
class ExpertiseSummaryService(object):
    @classmethod
    def find_summary(cls, evidences, keywords):
        keyword_evidence = dict()
        for evidence in evidences:
            evidence_data = [json.loads(x) for x in evidence['evidence_data']]
            url = evidence_data[0][0]
            block_id = evidence['block_id']
            for entry in evidence_data[1:]:
                if entry[0]:
                    if not entry[0] in keyword_evidence:
                        keyword_evidence[entry[0]] = list()
                    keyword_evidence[entry[0]].append([url,entry[1]])
        return keyword_evidence
        

