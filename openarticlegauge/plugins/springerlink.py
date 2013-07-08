
"""
This plugin handles SpringerLink articles.

Note this plugin supports a mark that Springer have used to show that an article
is publicly accessible but without a license statement. This searchers for the html
calling the image for the mark, not for plain text. Some SpringerLink articles are
licensed with Creative Commons licenses but this is not obvious from the top page.
"""

from openarticlegauge import plugin

class SpringerlinkPlugin(plugin.Plugin):
    _short_name = __name__.split('.')[-1]
    __version__='0.1' # consider incrementing or at least adding a minor version
                    # e.g. "0.1.1" if you change this plugin

    # The domains that this plugin will say it can support.
    # Specified without the schema (protocol - e.g. "http://") part.
    base_urls = ["link.springer.com/article"]
    # so if the http://link.springer.com/article/10.1007%2Fs12154-012-0090-1 URL comes in,
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
            {'This article is distributed under the terms of the Creative Commons Attribution License which permits any use, distribution, and reproduction in any medium, provided the original author(s) and the source are credited.':
                {'type': 'cc-by', # license type, see the licenses module for available ones
                }
            },
            {'This article is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/3.0/" target="_blank" title="This link will open in a new browser window">Creative Commons Attribution-NonCommercial 3.0 Unported Licence.':
                {'type' : 'cc-nc',
                 'version' : '3.0',
                 'url' : 'http://creativecommons.org/licenses/by-nc/3.0/'}
            },
            {'This content is freely available online to anyone, anywhere at any time.' :
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
