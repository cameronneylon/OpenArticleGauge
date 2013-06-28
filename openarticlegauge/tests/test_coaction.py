from unittest import TestCase
import requests, os

from openarticlegauge import config
from openarticlegauge.plugins.coaction import CoactionPlugin as MyPlugin

SUPPORTED_URLS = ["http://www.journalofextracellularvesicles.net/index.php/jev/article/view/20424", 
                  "http://www.eht-journal.net/fakjsskjdaf"]

UNSUPPORTED_URLS = ["http://www.biomedcentral.com/", "askjdfsakjdhfsa"]

# The licence object is as defined in the OAG API documentation.  Any fields omitted will
# not be checked.  Any fields included will be checked for an exact match against the actual
# record received when the plugin is run.  See below for the full spec of the licence
# object.
#
# The rules for the comparison licence object are:
# - if a key has a value, there resulting object's value must match exactly
# - if a key has been omitted, it will not be tested
# - if a key's value is the empty string, the resulting object's key's value must be the empty string
# - if a key's value is None, the resulting object MUST NOT have the key or MUST be the empty string
# - if a key's value is -1, the resulting object MUST have the key
#
RESOURCE_AND_RESULT = {
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources", "coaction.10.3402.uniped.v36i1.20975.html") : 
        {
            "id" : None,            # there should be no id field
            "version": "3.0",          # version should be the empty string
            "type": "cc-by",
            "jurisdiction": "",     # jurisdiction should be the empty string
            "open_access": True,
            "BY": True,
            "NC": False,
            "ND": False,
            "SA": False,
            "provenance": {
                "handler": MyPlugin._short_name, # name of plugin which processed this record
                "handler_version": MyPlugin.__version__, # version of plugin which processed this record
                "category": "page_scrape", # category is page_scrape
                "description": 'License decided by scraping the resource at http://www.unipedtidsskrift.net/index.php/uniped/article/view/20975 and looking for the following license statement: "Tidskriftet publiseres under en <a href="http://creativecommons.org/licenses/by/3.0/" rel="license">Creative Commons Attribution 3.0 Unported (CC BY 3.0) Licence".', # description is a long string
                "agent": config.agent, # agent is from configuration
                "source": "http://www.unipedtidsskrift.net/index.php/uniped/article/view/20975", # source is the url where we look this record up
                "date": -1 # date is not null (but we don't know the exact value)
            }
       },
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources", "coaction.10.3402.ijch.v72i0.20988.html") : 
        {
            "id" : None,            # there should be no id field
            "version": "3.0",          # version should be the empty string
            "type": "cc-by",
            "jurisdiction": "",     # jurisdiction should be the empty string
            "open_access": True,
            "BY": True,
            "NC": False,
            "ND": False,
            "SA": False,
            "provenance": {
                "handler": MyPlugin._short_name, # name of plugin which processed this record
                "handler_version": MyPlugin.__version__, # version of plugin which processed this record
                "category": "page_scrape", # category is page_scrape
                "description": 'License decided by scraping the resource at http://www.circumpolarhealthjournal.net/index.php/ijch/article/view/20988 and looking for the following license statement: "This journal is published under the terms of the <a href="http://creativecommons.org/licenses/by/3.0/" target="_blank">Creative Commons Attribution 3.0 Unported (CC BY 3.0) License".', # description is a long string
                "agent": config.agent, # agent is from configuration
                "source": "http://www.circumpolarhealthjournal.net/index.php/ijch/article/view/20988", # source is the url where we look this record up
                "date": -1 # date is not null (but we don't know the exact value)
            }
       },

    os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources", "coaction.10.3402.jev.v2i0.20424.html") : 
        {
            "id" : None,            # there should be no id field
            "version": "3.0",          # version should be the empty string
            "type": "cc-nc",
            "jurisdiction": "",     # jurisdiction should be the empty string
            "open_access": False,
            "BY": True,
            "NC": True,
            "ND": False,
            "SA": False,
            "provenance": {
                "handler": MyPlugin._short_name, # name of plugin which processed this record
                "handler_version": MyPlugin.__version__, # version of plugin which processed this record
                "category": "page_scrape", # category is page_scrape
                "description": 'License decided by scraping the resource at http://www.journalofextracellularvesicles.net/index.php/jev/article/view/20424 and looking for the following license statement: "This journal is published under the terms of the <a href="http://creativecommons.org/licenses/by-nc/3.0/" rel="license">Creative Commons Attribution-Noncommercial 3.0 Unported License".', # description is a long string
                "agent": config.agent, # agent is from configuration
                "source": "http://www.journalofextracellularvesicles.net/index.php/jev/article/view/20424", # source is the url where we look this record up
                "date": -1 # date is not null (but we don't know the exact value)
            }
        }
 
}

"""
Full specification of the OAG licence object, as taken from the API documentation:
{
    "status": "active",
    "maintainer": "",
    "description": "",
    "family": ""
    "title": "Creative Commons Attribution",
    "domain_data": true/false,
    "url": "http://www.opendefinition.org/licenses/cc-by",                
    "version": "",
    "domain_content": true/false,
    "is_okd_compliant": true/false,
    "is_osi_compliant": true/false,
    "domain_software": true/false,
    "type": "cc-by",
    "jurisdiction": "",
    "open_access": true/false,
    "BY": true/false,
    "NC": true/false,
    "ND": true/false,
    "SA": true/false,
    "provenance": {
        "category": "page_scrape",
        "description": "how the content was acquired ...",
        "agent": "OpenArticleGauge Service/0.1 alpha",
        "source": "http://www.plosbiology.org/article/info%3Adoi%2F10...",
        "date": "2013-02-16T21:51:54.669040"
    }
}
"""
################################################################################

CURRENT_REQUEST = None

# Mock response object for the requests library.  If your provider does anything other
# than look at the http response and the page content you will need to extend this
class MockResponse():
    def __init__(self):
        self.status_code = None
        self.text = None
        self.content = None
        self.url = None
    
def mock_get(url, *args, **kwargs):
    resp = MockResponse()
    resp.status_code = 200
    resp.url = CURRENT_REQUEST
    
    for filename, obj in RESOURCE_AND_RESULT.iteritems():
        if obj['provenance']['source'] == CURRENT_REQUEST:
            with open(filename) as f:
                resp.text = f.read()
            break
    resp.content = resp.text
    return resp

class TestProvider(TestCase):

    def setUp(self):
        global CURRENT_REQUEST
        CURRENT_REQUEST = None
        self.old_get = requests.get
        requests.get = mock_get
        
    def tearDown(self):
        global CURRENT_REQUEST
        CURRENT_REQUEST = None
        requests.get = self.old_get

    def test_01_supports_success(self):
        p = MyPlugin()
        for url in SUPPORTED_URLS:
            assert p.supports({"url" : [url]})
        
    def test_02_supports_fail(self):
        p = MyPlugin()
        for url in UNSUPPORTED_URLS:
            assert not p.supports({"url" : [url]})
    
    def test_03_resource_and_result(self):
        global CURRENT_REQUEST
        
        # go through each file and result object
        for path, comparison in RESOURCE_AND_RESULT.iteritems():
            # construct a request object, using the provenance/source url as the provider url
            record = {}
            record['bibjson'] = {}
            record['provider'] = {}
            record['provider']['url'] = [comparison['provenance']['source']]
            
            # set the current request so that the monkey patch knows how to respond
            CURRENT_REQUEST = comparison['provenance']['source']
            
            # run the plugin
            p = MyPlugin()
            p.license_detect(record)
            # check if all the top-level keys were created
            assert "bibjson" in record
            assert "license" in record['bibjson']
            assert record['bibjson']['license'] is not None
            
            # The rules for the comparison licence object are:
            # - if a key has a value, there resulting object's value must match exactly
            # - if a key has been omitted, it will not be tested
            # - if a key's value is the empty string, the resulting object's key's value must be the empty string
            # - if a key's value is None, the resulting object MUST NOT have the key or MUST be the empty string
            # - if a key's value is -1, the resulting object MUST have the key
            licence = record['bibjson']['license'][0]
            for key, value in comparison.iteritems():
                if key == "provenance":
                    # for better layout of code, let's do provenance separately
                    continue
                if value is None:
                    # the resulting object MUST NOT have the key or MUST be the empty string
                    assert key not in licence or licence.get(key) == "", ((key, value), licence.get(key))
                elif value == -1:
                    # the resulting object MUST have the key
                    assert key in licence, ((key, value), licence.get(key))
                else:
                    # the resulting object must match the comparison object
                    assert value == licence.get(key), ((key, value), licence.get(key))
            
            prov = licence.get("provenance", {})
            for key, value in comparison.get("provenance", {}).iteritems():
                if value is None:
                    # the resulting object MUST NOT have the key
                    assert key not in prov or prov.get(key) == "", ((key, value), prov.get(key))
                elif value == -1:
                    # the resulting object MUST have the key
                    assert key in prov, ((key, value), prov.get(key))
                else:
                    # the resulting object must match the comparison object
                    assert value == prov.get(key), ((key, value), prov.get(key))