
"""
This plugin handles Frontiers articles.
"""

from openarticlegauge import plugin

class FrontiersPlugin(plugin.Plugin):
    _short_name = __name__.split('.')[-1]
    __version__='0.1' # consider incrementing or at least adding a minor version
                    # e.g. "0.1.1" if you change this plugin

    # The domains that this plugin will say it can support.
    # Specified without the schema (protocol - e.g. "http://") part.
    base_urls = ["www.frontiersin.org", "frontiersin.org"]
    # so if the http://www.biomedcentral.com/1471-2164/13/425 URL comes in,
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
        To respond to the provider identifier: http://www.frontiersin.org
        
        This should determine the licence conditions of the Frontiers article and populate
        the record['bibjson']['license'] (note the US spelling) field.
        """

        lic_statements = [
            {'This is an open-access article distributed under the terms of the <a href="http://creativecommons.org/licenses/by/3.0/" target="_blank">Creative Commons Attribution License</a>, which permits use, distribution and reproduction in other forums, provided the original authors and source are credited':
                {'type': 'cc-by', # license type, see the licenses module for available ones
                 'version' : '3.0',
                 'url' : 'http://creativecommons.org/licenses/by/3.0/'}
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
