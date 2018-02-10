import falcon
from diploma.generate_resource import StartResource, GenerateResource
from middleware import RedirectToHTTPS
import os

app = falcon.API(middleware=[RedirectToHTTPS()])
app.req_options.auto_parse_form_urlencoded = True

app.add_route('/', StartResource())
app.add_route('/generate', GenerateResource())
app.add_static_route('/static', os.path.abspath("static"))
