
__author__ = "Bill Winnett"
__email__ = "bwinnett12@gmail.com"

import os
from Bio import SeqIO, Seq
from Bio.Data.CodonTable import TranslationError
from indexer import *

def write_to_gb(raw_data, output_folder):

    # if empty then there's nothing to do
    if raw_data == "":
        return "No files downloaded. Search query had no results"

    files_downloaded = []

    # Creates a variable to store all the genbank file
    lines = raw_data.split("\n")

    for line in lines:
        # By default, genbank files have "ORGANISM ID". Gets the ID and creates a file for it. Sets writing location
        if 'ORGANISM' in line:

            # Splits line and declares the file id based on desired folder and organism
            gb_location = output_folder + "gb/" + '-'.join(line.split()[1:]) + ".gb"

            # If there is no file, creates one and then adds the name for log outputting
            if not os.path.isfile(gb_location):
                current_file = open(gb_location, "x")

            current_file = open(gb_location, "w")

            # Writes the entire genbank to file
            current_file.write(raw_data)
            current_file.close()

            # Piggy backs genome writing to here
            write_genome(gb_location, output_folder)

    return str(len(files_downloaded)) + " files downloaded. Names are: " + str(files_downloaded)


# Writes the whole genome to a fasta in the genome folder of local storage
def write_genome(file, output_folder):

    # From here to the next section is just to get the file name of the organism
    lines = open(file, "r").readlines()
    out_loc = ""

    for line in lines:
        # Only looks for the name of the organism
        if 'ORGANISM' in line:

            # Splits line and declares the file id based on desired folder and organism
            out_loc = output_folder + "genome/" + '-'.join(line.split()[1:]) + ".fa"

            # If there is no file, creates one and then adds the name for log outputting
            if not os.path.isfile(out_loc):
                current_file = open(out_loc, "x")
            # No need to keep iterating so break from loop
            break

    with open(file, "r") as input_handle:

        with open(out_loc, "w") as output_handle:
            sequences = SeqIO.parse(input_handle, "genbank")
            count = SeqIO.write(sequences, output_handle, "fasta")



    print("Converted %i records" % count)



# Creates a fasta for each file
# Also uses information from this which is then sent into a translated .faa file
def write_to_fasta(raw, output_location):
    files_downloaded = amino_downloaded = []

    # Loops through each locus fetched
    for j in range(0, len(raw)):

        # Saves the sequence to avoid calling it repeatedly
        sequence = raw[j]["GBSeq_sequence"]

        # Variable for the to be named output location
        out_loc = output_location + "full_fa/" + "-".join(raw[j]["GBSeq_organism"].split(" ")) + ".fa"

        # For the DNA version
        if not os.path.isfile(out_loc):
            current_file = open(out_loc, "x")
            files_downloaded.append(raw[j]["GBSeq_locus"])
        current_file = open(out_loc, "w")

        # For the amino acid version
        out_loc_protein = output_location + "full_faa/" + "-".join(raw[j]["GBSeq_organism"].split(" ")) + ".faa"
        if not os.path.isfile(out_loc_protein):
            current_file_protein = open(out_loc_protein, "x")
            amino_downloaded.append(raw[j]["GBSeq_locus"])
        current_file_protein = open(out_loc_protein, "w")

        # Loops through the features of each gene
        for i, feature in enumerate(raw[j]["GBSeq_feature-table"]):

            # Gene locus, Organism, Feature name
            if feature['GBFeature_key'] == "gene" or feature['GBFeature_key'] == "source":
                continue

            else:
                try:
                    locus = raw[j]["GBSeq_locus"]
                    product_name = gene_name = ""

                    # Since the ncbi doesn't have an official indexing location for each component (product and
                    # gene name), has to iterate through each spot where it could be (All under qual)
                    for n, qual in enumerate((raw[j]["GBSeq_feature-table"][i]['GBFeature_quals'])):
                        if qual['GBQualifier_name'] == "product":
                            product_name = qual['GBQualifier_value']

                        if qual['GBQualifier_name'] == "gene":
                            gene_name = qual['GBQualifier_value']
                            add_to_index("genes", gene_name)

                        if qual['GBQualifier_name'] == 'note':
                            product_name = qual['GBQualifier_value']

                    # Creates a header based on what we have
                    header = " ".join([">", locus, gene_name,
                                       "-", product_name,
                                       raw[j]["GBSeq_organism"]])



                # For the genes that aren't setup the same as the others
                except KeyError:
                    # print("Header - Key Error")
                    continue

                # For the genes that aren't setup the same as the others
                except IndexError:
                    # print("Header - Index Error")
                    continue

                try:
                    # Many genes are listed as "complimentary". So gets sequence if they are on the other strand
                    if int(feature["GBFeature_intervals"][0]['GBInterval_from']) > \
                       int(feature["GBFeature_intervals"][0]['GBInterval_to']):

                        sequence_gene = sequence[int(feature["GBFeature_intervals"][0]['GBInterval_to']) - 1:
                                                 int(feature["GBFeature_intervals"][0]['GBInterval_from']) - 1].upper()

                    # Gets sequence of gene from index locations of source strand
                    else:
                        sequence_gene = sequence[int(feature["GBFeature_intervals"][0]['GBInterval_from']) - 1:
                                                 int(feature["GBFeature_intervals"][0]['GBInterval_to']) - 1].upper()

                # This is an exception for in case the entry is a feature or similar with only one location index
                except KeyError:
                    # print("Sequence - KeyError")
                    sequence_gene = feature['GBFeature_intervals'][0]['GBInterval_point']




                # Writes each part individually
                try:
                    current_file.write(header + "\n")
                except UnboundLocalError:
                    print(UnboundLocalError)

                # Loops through to 75 nucleotides per line
                for n in range(0, len(sequence_gene), 75):
                    current_file.write(sequence_gene[n:n + 75] + "\n")

                # Spacer
                current_file.write(" " + "\n")

                # TODO - have a better return policy
                write_fasta_to_individual(out_loc, output_location, "fa")
                write_fasta_to_individual(out_loc_protein, output_location, "faa")

                amino_downloaded.append(write_translation_to_fasta(
                    header, sequence_gene, current_file_protein))

        current_file_protein.close()
        current_file.close()

    return str(len(files_downloaded)) + " fasta - Names are: " + str(files_downloaded) + "\n" + \
        str(len(amino_downloaded)) + " amino fasta - Names are: " + str(amino_downloaded)



# Makes a .fasta that includes a protein copy with it
# Piggy tails off the DNA to fasta version (The only difference is the translated sequence)
def write_translation_to_fasta(header, sequence, out_file):
    translated_protein = ""
    files_downloaded = ""

    try:
        translated_protein = Seq.translate(sequence, table=4)
    except TranslationError:
        r = 2

    out_file.write(header + "\n")

    for n in range(0, len(translated_protein), 75):
        out_file.write(translated_protein[n:n + 75] + "\n")

    out_file.write(" " + "\n")

    return files_downloaded if files_downloaded != "" else ""


# Takes a fasta and breaks every gene into its own file
# Can be used for .fa or .faa
# TODO - update chart selector
def write_fasta_to_individual(file, output_folder, option):

    for record in SeqIO.parse(file, "fasta"):
        # IF record is empty or gene name is missing, skips it
        if record.description.split()[1] == '-' or record.seq == '':
            continue

        # Options based on if the option is fasta or if it needs to be translated
        if option == "fa":
            location = output_folder + "fa/" + record.description.split()[1] + "_" + file.split("/")[-1]
        elif option == "faa":
            location = output_folder + "faa/" + record.description.split()[1] + "_" + file.split("/")[-1]

        # Creates a file if not there else uses file
        if not os.path.isfile(location):
            current_file = open(location, "x")
        current_file = open(location, "w")

        # Writes the header first
        current_file.write("> " + record.description + "\n")

        # if .faa, translates sequence. Else keeps previous
        try:
            sequence = Seq.translate(record.seq, table=4) if option == "faa" else record.seq
        except TranslationError:
            sequence = record.seq

        # Loops through to 75 nucleotides per line
        for n in range(0, len(sequence), 75):
            current_file.write(str(sequence[n:n + 75]) + "\n")

        # Spacer
        current_file.write(" " + "\n")






