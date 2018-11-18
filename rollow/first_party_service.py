from tornado.template import Template

first_party_template = Template(open("./templates/first_party.html").read())

class FirstPartyService(object):
    @classmethod
    def render_html(cls, evidences, keywords):
        html = first_party_template.generate(evidences=evidences, 
                                             keywords=keywords)
        return html
