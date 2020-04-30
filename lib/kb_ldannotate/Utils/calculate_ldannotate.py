#!/usr/bin/python3

import sys, fileinput
import string
import math
import time
import sys
import operator
import copy
import numpy as np
import os
import subprocess


class calculate_ldannotate:

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

    def validate_vcf(self, vcf_file):
        print("checking format for vcf file:")
        print('\t', vcf_file)
        f = open(vcf_file, 'r')
        a = 0
        ln = []
        for line in f:
            l = line.strip().split('\t')
            if line[0] == '#CHROM':
                a += 1
                if l[1] != 'POS' or l[3] != REF or l[4] != ALT:
                    print("There's a problem with the vcf input file, please verify your file")
                    exit(1)
                else:
                    pass
            elif a >= 1:
                if l[0].isnumeric() or l[0] == 'X' or l[0] == 'Y':
                    ln.append(l[0])
                else:
                    print("chromosome numbers should be numbers or X or Y")
                    exit(1)
            else:
                pass

    def run_command(self, command):
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

    def get_meanLD(self, meanld_file):
        mean = 0
        try:
            with open(meanld_file, 'r') as temp:
                line = temp.readline()
                line = line.strip().split()
                mean = int(float(line[0]))
        except IOError:
            print("Could not read file:", meanld_file)

        return mean

    def run_ld(self, vcf_file):
        cmd1 = "plink1.9 --vcf " + vcf_file + " --r2 --ld-window-r2 0.4 --out mydata --noweb --allow-extra-chr --chr-set 95"
        self.run_command(cmd1)
        cmd2 = "awk '{if ($7 > \"'$5'\" && $1 != \"0\") sum+= ($5-$2)} END {print sum/NR}' mydata.ld > meanLD"
        self.run_command(cmd2)

    def create_output_file(self, vcf_file, gff_file, candidate_snp, feature_type, threshold, outputfile, output_dir):

        self.validate_vcf(vcf_file)
        self.run_ld(vcf_file)

        mean = self.get_meanLD("meanLD")

        # dictionnary of all genes annotations
        try:
            with open(gff_file, 'r') as gff_handle:
                annotation_dict = {}
                for line in gff_handle:
                    if line[0] != '#':
                        l = line.strip().split('\t')
                        if l[2] == feature_type:
                            reg = l[0] + '_' + l[3] + '_' + l[4]
                            annotation_dict[reg] = l[-1]
        except IOError:
            print("Could not read file:", gff_file)

        # list of candidate SNPs
        # SNP = 'chr_pos'

        try:
            with open(candidate_snp, 'r') as candidate_handle:
                candidatesnp_lst = []
                line = candidate_handle.readline()

                for line in candidate_handle:
                    l = line.strip().split('\t')
                    SNP = l[0] + '_' + l[1]
                    candidatesnp_lst.append(SNP)
        except IOError:
            print("Could not read file:", candidate_snp)

        # dictionnary of candidate regions
        # SNP = 'chr_pos'

        try:
            with open('mydata.ld', 'r') as ldfile_handle:

                snplinkage_dict = {}
                filtered_ldsnp_lst = []
                for line in ldfile_handle:
                    l = line.strip().split(' ')

                    SNP1 = l[0] + '_' + l[1]
                    SNP2 = l[3] + '_' + l[4]

                    if SNP1 in candidatesnp_lst:
                        if float(l[-1]) >= float(threshold):
                            if SNP1 in snplinkage_dict.keys():
                                snplinkage_dict[SNP1].append(l[4])
                            else:
                                snplinkage_dict[SNP1] = [l[4]]
                    else:
                        if SNP1 not in filtered_ldsnp_lst:
                            filtered_ldsnp_lst.append(SNP1)
                        else:
                            pass

                    if SNP2 in candidatesnp_lst:
                        if float(l[-1]) >= float(threshold):
                            if SNP2 in snplinkage_dict.keys():
                                snplinkage_dict[SNP2].append(l[1])
                            else:
                                snplinkage_dict[SNP2] = [l[1]]

                    else:
                        if SNP2 not in filtered_ldsnp_lst:
                            filtered_ldsnp_lst.append(SNP2)
                        else:
                            pass
        except IOError:
            print("Could not read file: mydata.ld")

        # at the end we get a dictionnary with position for SNPs in linkage

        # writing output

        try:
            with open(output_dir + '/' + outputfile, 'w') as outfile:

                outfile.write("SNP\tchromosome\tregion_start\tregion_end\tgene_start\tgene_end\tannotation\n")

                for i in candidatesnp_lst:
                    j = i.split('_')
                    if i not in snplinkage_dict.keys() and i not in filtered_ldsnp_lst:
                        z = str(i) + '_alone'
                        snplinkage_dict[z] = [(int(j[1]) - mean), (int(j[1]) + mean)]
                    else:
                        pass

                for i in snplinkage_dict:
                    j = i.split('_')
                    up = int(max(snplinkage_dict[i]))
                    down = int(min(snplinkage_dict[i]))
                    for k in annotation_dict.keys():
                        l = k.split('_')
                        if j[0] == l[0]:
                            if int(l[1]) < up < int(l[2]) or int(l[1]) < down < int(l[2]) or down < int(
                                    l[1]) < up or down < int(l[2]) < up:
                                res = [str(i), str(l[0]), str(down), str(up), str(l[1]), str(l[2])]
                                res.append(annotation_dict[k])
                                outfile.write('\t'.join(res) + '\n')
                            else:
                                pass
                        else:
                            pass
        except IOError:
            print("Could not read file:", outputfile)


