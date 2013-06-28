
"""
This plugin handles Co-Action articles.

"""

from openarticlegauge import plugin

class CoactionPlugin(plugin.Plugin):
    _short_name = __name__.split('.')[-1]
    __version__='0.1' # consider incrementing or at least adding a minor version
                    # e.g. "0.1.1" if you change this plugin

    # The domains that this plugin will say it can support.
    # Specified without the schema (protocol - e.g. "http://") part.
    base_urls = ["www.cellmoloto.net",
                 "diabeticfootandankle.net",
                 "www.eht-journal.net",
                 "www.ethicsandglobalpolitics.net",
                 "www.eurojnlofpsychotraumatol.net",
                 "www.foodandnutritionresearch.net",
                 "www.globalhealthaction.net",
                 "www.infectionecologyandepidemiology.net",
                 "www.circumpolarhealthjournal.net",
                 "www.ijqhw.net/index.php/qhw",
                 "www.journalofextracellularvesicles.net",
                 "www.aestheticsandculture.net",
                 "www.jchimp.net",
                 "www.journaloforalmicrobiology.net",
                 "www.libyanjournalofmedicine.net",
                 "www.mechanicalcirculatorysupport.net",
                 "www.med-ed-online.net",
                 "www.microbecolhealthdis.net",
                 "www.nano-reviews.net",
                 "www.childlitaesthetics.net",
                 "www.pathobiologyofaging.net",
                 "www.polarresearch.net",
                 "www.researchinlearningtechnology.net",
                 "www.socioaffectiveneuroscipsychol.net",
                 "www.tellusa.net",
                 "www.tellusb.net",
                 "www.unipedtidsskrift.net",
                 "www.vulnerablegroupsandinclusion.net"]
    # so if the http://www.journalofextracellularvesicles.net/index.php/jev/article/view/20424 URL comes in,
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
        To respond to the Co-action provider identifiers
        
        This should determine the licence conditions of the Co-action article and populate
        the record['bibjson']['license'] (note the US spelling) field.
        """

        lic_statements = [
            {'Tidskriftet publiseres under en <a href="http://creativecommons.org/licenses/by/3.0/" rel="license">Creative Commons Attribution 3.0 Unported (CC BY 3.0) Licence':
                {'type': 'cc-by', # license type, see the licenses module for available ones
                 'version' : '3.0',
                 'url' : 'http://creativecommons.org/licenses/by/3.0/'}
            },
            {'This journal is published under the terms of the <a href="http://creativecommons.org/licenses/by/3.0/" target="_blank">Creative Commons Attribution 3.0 Unported (CC BY 3.0) License':
                {'type': 'cc-by', # license type, see the licenses module for available ones
                 'version' : '3.0',
                 'url' : 'http://creativecommons.org/licenses/by/3.0/'}
            },
            {'This journal is published under the terms of the <a href="http://creativecommons.org/licenses/by-nc/3.0/" rel="license">Creative Commons Attribution-Noncommercial 3.0 Unported License':
                {'type' : 'cc-nc',
                 'version' : '3.0',
                 'url' : 'http://creativecommons.org/licenses/by-nc/3.0/'}
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
