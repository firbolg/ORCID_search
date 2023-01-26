import orcid
import requests
import io
import pandas as pd
import json
from xml.etree import ElementTree

institution_key = 'XXX-XXXXXXXXX'
institution_secret = 'XXX-XXX-XXX-XXX-XXX'

api = orcid.PublicAPI(institution_key, institution_secret, sandbox=True)

search_token = api.get_search_token_from_orcid()
#search_results = api.search('https://pub.orcid.org/v2.0/search/?q=affiliation-org-name:"University+of+Johannesburg"')

#user_id = 'dolanl@mailinator.com'
#user_password = 'ORCIDTest1'
#redirect_uri = 'http://localhost/myApp'

#token = api.get_token(user_id, user_password, redirect_uri)

summary = api.read_record_public('0000-0002-2419-4941', 'record', search_token)
#summary = api._search('keyword','start','rows','headers=text/csv''Indiana'+'University'), 'record', search_token

#r = requests.get('https://pub.sandbox.orcid.org/v3.0/search/?q=pmid:24857732')

#r = requests.get('https://pub.sandbox.orcid.org/v3.0/search/?q=affiliation-org-name:(%22Boston%20University%22+OR+BU)')

#df = pd.read_csv(io.StringIO(r.decode('utf-8')))

#tree = ElementTree.fromstring(r.content)

#df = pd.read_json(r)



print(json.dumps(summary, indent=4))






