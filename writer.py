
__author__ = "Bill Winnett"
__email__ = "bwinnett12@gmail.com"

import os
from Bio import SeqIO
from indexer import *

# TODO - This one works but is inefficient
def write_to_gb(raw_data, output_folder):

    if raw_data == "":
        return "No files downloaded. Search query had no results"

    files_downloaded = []
    # Creates a temp file and saves the parsed (ncbi) data to. If no temp file, creates one
    # I know this is extra work, but I'm just not sure how to do it cleaner
    try:
        temp_file = open("./temp.txt", "x")
    except FileExistsError:
        pass

    temp_file = open("./temp.txt", "w")
    temp_file.write(raw_data)

    # parses data from text and saves it as a line
    with open('./temp.txt', 'r') as raw_text:
        lines = raw_text.readlines()

    # Declares a variable to write to. This will be changed to Locus ID after first iteration
    current_file = temp_file

    for line in lines:
        # By default, genebank files have "LOCUS ID". Gets the ID and creates a file for it. Sets writing location
        if 'ORGANISM' in line:
            current_file.close()

            # Splits line and declares the file id based on desired folder and Locus ID
            # split = line.split()
            # print("THIS ONE: ", split)
            gb_location = output_folder + "gb/" + ' '.join(line.split()[1:]) + ".gb"

            # If there is no file, creates one and then adds the name for log outputting
            if not os.path.isfile(gb_location):
                current_file = open(gb_location, "x")
                # files_downloaded.append(split[1])

            current_file = open(gb_location, "w")

        current_file.write(line)

    # Removes temp file
    try:
        temp_file.close()
        os.remove("./temp.txt")
    except FileNotFoundError as e:
        pass

    return str(len(files_downloaded)) + " files downloaded. Names are: " + str(files_downloaded)


# Creates a fasta for each file
# Also uses information from this which is then sent into a translated .faa file
def write_to_fasta(raw, output_location, chart):
    files_downloaded = amino_downloaded = []

    # Loops through each locus fetched
    for j in range(0, len(raw)):

        # Saves the sequence to avoid calling it repeatedly
        # TODO - Change name from full_fa
        sequence = raw[j]["GBSeq_sequence"]

        # Variable for the to be named output location
        out_loc = output_location + "full_fa/" + raw[j]["GBSeq_organism"] + ".fa"

        # For the DNA version
        if not os.path.isfile(out_loc):
            current_file = open(out_loc, "x")
            files_downloaded.append(raw[j]["GBSeq_locus"])
        current_file = open(out_loc, "w")

        # For the amino acid version
        out_loc_protein = output_location + "full_faa/" + raw[j]["GBSeq_organism"] + ".faa"
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


                    header = " ".join([">", locus, gene_name,
                                       "-", product_name,
                                       raw[j]["GBSeq_organism"]])



                # For the genes that aren't setup the same as the others
                except KeyError:
                    print("Header - Key Error")
                    # print(feature)
                    continue

                # For the genes that aren't setup the same as the others
                except IndexError:
                    print("Header - Index Error")

                    # print(feature)
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
                    print("Sequence - KeyError")
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

                # TODO - Fix this
                print(out_loc)
                write_fasta_to_individual(out_loc, output_location, "fa")
                write_fasta_to_individual(out_loc_protein, output_location, "faa")

                amino_downloaded.append(write_translation_to_fasta(
                    header, sequence_gene, chart, current_file_protein))

        # files_made += raw[j]["GBSeq_locus"] + ", "

        current_file_protein.close()
        current_file.close()

        add_to_index("species", raw[j]["GBSeq_organism"])




    return str(len(files_downloaded)) + " fasta - Names are: " + str(files_downloaded) + "\n" + \
        str(len(amino_downloaded)) + " amino fasta - Names are: " + str(amino_downloaded)



# Makes a .fasta that includes a protein copy with it
# Piggy tails off the DNA to fasta version (The only difference is the translated sequence)
def write_translation_to_fasta(header, sequence, chart, out_file):
    translated_protein = ""
    files_downloaded = ""

    for i in range(0, len(sequence) if len(sequence) % 3 == 0 else len(sequence) - (len(sequence) % 3), 3):
        try:
            translated_protein += chart[sequence[i:i+3]]

        except KeyError:
            print(header)


    out_file.write(header + "\n")

    for n in range(0, len(translated_protein), 75):
        out_file.write(translated_protein[n:n + 75] + "\n")

    out_file.write(" " + "\n")

    return files_downloaded if files_downloaded != "" else ""



def write_fasta_to_individual(file, output_folder, option):

    for record in SeqIO.parse(file, "fasta"):
        if record.description.split()[1] == '-':
            continue

        print(record.description.split())
        if option == "fa":
            location = output_folder + "fa/" + record.description.split()[1] + "_" + file.split("/")[-1]
        elif option == "faa":
            location = output_folder + "faa/" + record.description.split()[1] + "_" + file.split("/")[-1]


        if not os.path.isfile(location):
            current_file = open(location, "x")
        current_file = open(location, "w")

        current_file.write(record.description + "\n")

        # Loops through to 75 nucleotides per line
        for n in range(0, len(record.seq), 75):
            current_file.write(str(record.seq[n:n + 75]) + "\n")

        # Spacer
        current_file.write(" " + "\n")



