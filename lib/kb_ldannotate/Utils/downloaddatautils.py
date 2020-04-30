import os
from installed_clients.VariationUtilClient import VariationUtil
from installed_clients.GenomeFileUtilClient import GenomeFileUtil

class downloaddatautils:

    def __init__(self):
        self.callbackURL = os.environ['SDK_CALLBACK_URL']
        self.gfu = GenomeFileUtil(self.callbackURL)
        self.vfu = VariationUtil(self.callbackURL)
        pass

    def download_genome(self, params):
        file = self.gfu.genome_to_gff({'genome_ref': params['gff_ref']})
        return file

    def download_vcf(self, params):
        params['input_var_ref'] = params['vcf_ref']
        self.vu.export_variation_as_vcf(params)

