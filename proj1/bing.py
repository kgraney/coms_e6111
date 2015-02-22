import base64
import os
import urllib
import urllib2

_BING_URL = 'https://api.datamarket.azure.com/Bing/Search/Web?'

def execute_query(query, account_key):
    account_key_enc = base64.b64encode(account_key + ':' + account_key)
    headers = {'Authorization': 'Basic ' + account_key_enc}
    url_params = {'Query': "'%s'" % query,
                  '$top': 10,
                  '$format': 'json'}
    req = urllib2.Request(_BING_URL + urllib.urlencode(url_params), headers = headers)
    response = urllib2.urlopen(req)
    return response.read()

def execute_query_fake(query, account_key):
    fname = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                         'sample_data', 'sample_output.json')
    with open(fname, 'r') as f:
        return f.read()

