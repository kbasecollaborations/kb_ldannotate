import os
from installed_clients.VariationUtilClient import VariationUtil
from installed_clients.AssemblyUtilClient import GenomeUtil


class downloaddatautils:

    def __init__(self):
        self.callbackURL = os.environ['SDK_CALLBACK_URL']
        self.gu = GenomeUtil(self.callbackURL)
        self.vu = VariationUtil(self.callbackURL)
        pass

    def download_genome(self, params):
        file = self.gu.get_assembly_as_fasta({
          'ref': params['genome_or_assembly_ref']
        })
        return file

    def download_vcf(self, params):
        params['input_var_ref'] = params['vcf_ref']
        self.vu.export_variation_as_vcf(params)

