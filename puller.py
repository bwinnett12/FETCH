import glob
import os
from shutil import copy

from Bio import SeqIO
from Bio.Align.Applications import MafftCommandline

from indexer import get_query_from_indexes


# Pulls all of the fastas from the query into a folder
def move_individual_fasta_to(out_loc):
    query = get_query_from_indexes()
    print(query[0])
    print(query[1])

    # Species is 0
    # the next 5 for loops are nearly identical except first three is species
    for species in query[0]:
        # gets all of the file addresses that are in the folder
        for pos in glob.glob("./storage/fa/*.fa"):
            # if the gene is in the title (Standard packing), then moves file
            if pos.split("_")[-1].split(".")[0].lower() == species.replace(" ", "-").lower():
                copy(pos, out_loc)

        # Repeats for all of the amino fastas
        for pos in glob.glob("./storage/faa/*.faa"):
            if pos.split("_")[-1].split(".")[0].lower() == species.replace(" ", "-").lower():
                copy(pos, out_loc)

        # Repeats for genbank files
        for pos in glob.glob("./storage/gb/*.gb"):
            if pos.split("/")[-1].split(".")[0].lower() == species.replace(" ", "-").lower():
                copy(pos, out_loc)


    # Gene is 1
    for gene in query[1]:
        for pos in glob.glob("./storage/fa/*.fa"):
            if pos.split("_")[0].split("/")[-1].lower() == gene.lower():
                copy(pos, out_loc)

        for pos in glob.glob("./storage/faa/*.faa"):
            if pos.split("_")[0].split("/")[-1].lower() == gene.lower():
                copy(pos, out_loc)



# Pulls all of the instances of the desired gene into a single fasta
def pull_query_to_fasta(out_loc):
    query = get_query_from_indexes()

    for gene in query[1]:
        # names output folder to gene.fa
        out_loc_file = out_loc + gene + ".fa"

        # Makes said file
        if not os.path.isfile(out_loc_file):
            current_file = open(out_loc_file, "x")
        current_file = open(out_loc_file, "w")

        files_array = []

        # Searches for all files with the name as the gene
        for pos in glob.glob("./storage/fa/*.fa"):
            if pos.split("_")[0].split("/")[-1].lower() == gene.lower():
                # Adds names to a list
                files_array.append(pos)


        for file in files_array:
            # writes the fasta into the file
            for record in SeqIO.parse(file, "fasta"):
                current_file.write(">" + record.description + " " + str(len(record.seq)) + "\n")

                for n in range(0, len(record.seq), 75):
                    current_file.write(str(record.seq[n:n + 75]) + "\n")
                current_file.write("\n")

        current_file.close()
        align_fasta(out_loc_file)

    for species in query[0]:
        out_loc_file = out_loc + species + ".fa"

        # Makes said file
        if not os.path.isfile(out_loc_file):
            current_file = open(out_loc_file, "x")
        current_file = open(out_loc_file, "w")

        files_array = []

        for pos in glob.glob("./storage/fa/*.fa"):
            if pos.split("_")[1].strip(".fa").lower() == species.lower():
                # Adds names to a list
                files_array.append(pos)

        for file in files_array:
            # writes the fasta into the file
            for record in SeqIO.parse(file, "fasta"):
                current_file.write(">" + record.description + " " + str(len(record.seq)) + "\n")

                for n in range(0, len(record.seq), 75):
                    current_file.write(str(record.seq[n:n + 75]) + "\n")
                current_file.write("\n")

        current_file.close()
        align_fasta(out_loc_file)


# When called, makes an aligned version of the fasta just pulled
# TODO - Mafft requires an exe location unless on UNIX. Implement cross platform support
def align_fasta(in_file_loc):

    # Gets the base file *.fa
    out_file_base = in_file_loc.split(".fa")[0] + ".aln"

    # Runs command line to work with mafft
    mafft_cline = MafftCommandline(input=in_file_loc)

    # runs mafft using what our file was and to an output of base.aln
    stdout, stderr = mafft_cline()
    with open(out_file_base, "w") as handle:
        handle.write(stdout)



# I like having a sandbox
def sando():
    r = 2
    pulled_from_fasta_seq = []
    pulled_from_fasta_id = []




def main():
    print("hello from puller!")



if __name__ == '__main__':
    main()
