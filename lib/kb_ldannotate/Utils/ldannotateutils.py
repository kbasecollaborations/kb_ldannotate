import os
import subprocess


class ldannotateutils:

    def __init__(self):
       self.callbackURL = os.environ['SDK_CALLBACK_URL']
       pass

    def validate_params(self, params):
            if 'vcf_ref' not in params:
                raise ValueError('required vcf_ref field was not defined')
            elif 'gff_ref' not in params:
                raise ValueError('require gff_ref field was not defined')
            elif 'candidate_snps' not in params:
                raise ValueError('required candidate_snps field was not defined')
            elif 'feature_type' not in params:
                raise ValueError('required feature_type field was not defined')
            elif 'threshold' not in params:
                raise ValueError('required threshold field was not defined')
            elif 'output_file' not in params:
                raise ValueError('required output_file field was not defined')


    def build_ldannotate_command(self, params, output_dir):
        vcf_file = params.get("vcf_ref")
        gff_file = params.get("gff_ref")
        candidate_snp_file = params.get("candidate_snps")
        feature_type = params.get("feature_type")
        threshold = params.get("threshold")
        output_file = params.get("output_file")

        command = "python3 /kb/module/deps/LD-annot0.4.py " +  vcf_file + " " +gff_file + " "+ candidate_snp_file, + " "+ candidate_snp_file + " " + feature_type + " " + threshold + " " + output_dir+"/"+output_file

        return command

    def run_ldannotate_command(self, command):
        try:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if stdout:
                print("ret> ", process.returncode)
                print("OK> output ", stdout)
            if stderr:
                print("ret> ", process.returncode)
                print("Error> error ", stderr.strip())

        except OSError as e:
            print("OSError > ", e.errno)
            print("OSError > ", e.strerror)
            print("OSError > ", e.filename)

