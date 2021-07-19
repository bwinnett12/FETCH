import glob
import os

from Bio.Align.Applications import MafftCommandline
from Bio.Phylo.Applications import _Fasttree


'''
This module is for hooking up different tools, plugins, and other pieces to the pipeline
Currently supported tools / features:
mafft - alignment, FastTree - tree building
work in progress:
RAxML, PAL2NAL

'''

# When called, makes an aligned version of the fasta just pulled
# Uses the tool mafft
def align_fasta(in_file_loc):

    # Gets the base file *.fa
    out_file_base = in_file_loc.split(".fa")[0] + ".aln"

    # Runs command line to work with mafft
    mafft_cline = MafftCommandline(input=in_file_loc)

    # runs mafft using what our file was and to an output of base.aln
    stdout, stderr = mafft_cline()
    with open(out_file_base, "w") as handle:
        handle.write(stdout)

# out_folder, fasttree_path
# This method can be used to run fasttree on all
def tool_fasttree(out_folder, fasttree_path, generate_error_output):

    # Only operating on aligned files
    for file_in in glob.glob(out_folder.rstrip("/") + "/*.aln"):

        # File for out (default .tree) and file for the output text
        file_out = file_in.rstrip(".aln") + ".tree"
        error_out = file_in.rstrip(".aln") + "_(info).tree"

        # Set with default options nt and gtr
        cmd = _Fasttree.FastTreeCommandline(fasttree_path, nt=True, gtr=True, input=file_in, out=file_out)
        out, err = cmd()

        # Writing the error as well.. Reliant on using config to set optional
        if generate_error_output:
            if not os.path.isfile(error_out):
                file_error = open(error_out, "x")
            file_error = open(error_out, "w")
            file_error.write(err)