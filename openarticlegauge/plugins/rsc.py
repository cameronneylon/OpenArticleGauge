
"""
This plugin handles Frontiers articles.

Note this plugin supports a legacy mark that RSC have used to show that an article
is publicly accessible but without a license statement. This searchers for the html
calling the image for the mark, not for plain text.
"""

from openarticlegauge import plugin

class RSCPlugin(plugin.Plugin):
    _short_name = __name__.split('.')[-1]
    __version__='0.1' # consider incrementing or at least adding a minor version
                    # e.g. "0.1.1" if you change this plugin

    # The domains that this plugin will say it can support.
    # Specified without the schema (protocol - e.g. "http://") part.
    base_urls = ["pubs.rsc.org/"]
    # so if the http://pubs.rsc.org/en/Content/ArticleLanding/2013/EE/c3ee00043e URL comes in,
    # it should be supported.
    
    def supports(self, provider):
        """
        Does this plugin support this provider
        """
        
        work_on = self.clean_urls(provider.get("url", []))

        for url in work_on:
            if self.supports_url(url):
                return True

        return False

    def supports_url(self, url):
        """
        Same as the supports() function but answers the question for a single URL.
        """
        for bu in self.base_urls:
            if self.clean_url(url).startswith(bu):
                return True
        return False

    def license_detect(self, record):

        """
        To respond to the provider identifier: http://pubs.acs.org
        
        This should determine the licence conditions of the RSC article and populate
        the record['bibjson']['license'] (note the US spelling) field.
        """

        lic_statements = [
            {'This article is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/3.0/" target="_blank" title="This link will open in a new browser window">Creative Commons Attribution 3.0 Unported Licence.':
                {'type': 'cc-by', # license type, see the licenses module for available ones
                 'version' : '3.0',
                 'url' : 'http://creativecommons.org/licenses/by/3.0/'}
            },
            {'<img  class="list_icon_openaccess" src="http://sod-a.rsc-cdn.org/pubs.rsc.org/content/NewImages/open_access_blue.png" alt="Open Access" />' :
                {'type' : 'publisher-asserted-accessible'
                }
            }    
        ]
        
        # some basic protection against missing fields in the incoming record
        if "provider" not in record:
            return
        if "url" not in record["provider"]:
            return
        
        # For all URL-s associated with this resource...
        for url in record['provider']['url']:
            # ... run the dumb string matcher if the URL is supported.
            if self.supports_url(url):
                self.simple_extract(lic_statements, record, url)
