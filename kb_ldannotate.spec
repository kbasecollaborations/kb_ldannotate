/*
A KBase module: kb_ldannotate
*/

module kb_ldannotate {
    typedef structure {
        string report_name;
        string report_ref;
    } ReportResults;

    typedef structure {
        string workspace_name;
	    string vcf_ref;
	    string gff_ref;
        string candidate_snps;
        string feature_type;
        string threshold;
        string output_file;
	} ldannotate_input;
    /*
        This example function accepts any number of parameters and returns results in a KBaseReport
    */
    funcdef run_kb_ldannotate(ldannotate_input params) returns (ReportResults output) authentication required;

};
