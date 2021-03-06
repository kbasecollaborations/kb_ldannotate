# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os
import uuid
#from kb_ldannotate.Utils.ldannotateutils import ldannotateutils
from kb_ldannotate.Utils.downloaddatautils import downloaddatautils
from kb_ldannotate.Utils.calculate_ldannotate import calculate_ldannotate
from installed_clients.KBaseReportClient import KBaseReport
#END_HEADER


class kb_ldannotate:
    '''
    Module Name:
    kb_ldannotate

    Module Description:
    A KBase module: kb_ldannotate
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = ""
    GIT_COMMIT_HASH = "HEAD"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        #self.lau = ldannotateutils()
        self.du = downloaddatautils()
        self.cld = calculate_ldannotate()
        #END_CONSTRUCTOR
        pass


    def run_kb_ldannotate(self, ctx, params):
        """
        This example function accepts any number of parameters and returns results in a KBaseReport
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_kb_ldannotate

        logging.info("validating input parameters")
        self.cld.validate_params(params)


        output_dir = os.path.join(self.shared_folder, str(uuid.uuid4()))
        os.mkdir(output_dir)

        #parsing input parameters
        vcf_file = params.get("vcf_ref")
        gff_file = params.get("gff_ref")
        candidate_snp_file = params.get("candidate_snps")
        feature_type = params.get("feature_type")
        threshold = params.get("threshold")
        output_file = params.get("output_file")

        #cmd = self.lau.build_ldannotate_command(vcf_file, gff_file, candidate_snp_file, feature_type, threshold, output_file, output_dir)

        #self.lau.run_ldannotate_command(cmd)
        self.cld.create_output_file(vcf_file, gff_file, candidate_snp_file, feature_type, threshold, output_file, output_dir)

        report = KBaseReport(self.callback_url)
        report_info = report.create({'report': {'objects_created':[],
                                                'text_message': 'Nice Report'},
                                                'workspace_name': params['workspace_name']})
        output = {
            'report_name': report_info['name'],
            'report_ref': report_info['ref'],
        }
        #END run_kb_ldannotate

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_kb_ldannotate return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
