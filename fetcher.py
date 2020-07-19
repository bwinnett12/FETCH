
__author__ = "Bill Winnett"
__email__ = "bwinnett12@gmail.com"

import os
from Bio import Entrez


def parse_ncbi(query_from_user, output_type):

    # Always tell ncbi who you are. Using mine until testing is over and the user will input theirs
    Entrez.email = "wwinnett@iastate.edu"

    # searches for those who fit your request
    handle = Entrez.esearch(db="nucleotide", term=query_from_user)

    # Records those who match the query and then formats them so it can fetch them
    record = Entrez.read(handle)
    gi_query = ",".join(record["IdList"])

    retmode_input = ("text", "xml")[output_type == "fasta"]

    # Fetches those matching IDs from esearch
    # rettype gb = genebank(text as retmode), fasta = fasta (use xml as retmode)
    handle = Entrez.efetch(db="nucleotide", id=gi_query, rettype="gb", retmode=retmode_input)

    # for xml... if using .txt it should be handle.read()
    if output_type == "fasta":
        raw_data = Entrez.read(handle)
    else:
        raw_data = handle.read()

    return raw_data




def write_gb_to_fasta(raw, output_location):
    files_downloaded = []

    # Loops through each locus fetched
    for j in range(0, len(raw)):

        # Saves the sequence to avoid calling it repeatedly
        sequence = raw[j]["GBSeq_sequence"]

        # Variable for the to be named output location
        out_loc = output_location + raw[j]["GBSeq_locus"] + ".fa"

        if not os.path.isfile(out_loc):
            current_file = open(out_loc, "x")
            files_downloaded.append(raw[j]["GBSeq_locus"])
        current_file = open(out_loc, "w")

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

                    header = " ".join([">", locus, product_name,
                                       " - ", gene_name,
                                       raw[j]["GBSeq_organism"]])


                # For the genes that aren't setup the same as the others
                except KeyError:
                    print("Header - Key Error")

                # For the genes that aren't setup the same as the others
                except IndexError:
                    print("Header - Index Error")

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
                    sequence = feature['GBFeature_intervals'][0]['GBInterval_point']

                # Writes each part individually
                current_file.write(header + "\n")

                # Loops through to 75 nucleotides per line
                for n in range(0, len(sequence_gene), 75):
                    current_file.write(sequence_gene[n:n + 75] + "\n")

                # Spacer
                current_file.write(" " + "\n")

        # files_made += raw[j]["GBSeq_locus"] + ", "
        current_file.close()

    return str(len(files_downloaded)) + " files downloaded. Names are: " + str(files_downloaded)





# TODO - Remove use of temp file
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
        if 'LOCUS' in line:
            current_file.close()

            # Splits line and declares the file id based on desired folder and Locus ID
            split = line.split()
            gb_location = output_folder + split[1] + ".gb"

            # If there is no file, creates one and then adds the name for log outputting
            if not os.path.isfile(gb_location):
                current_file = open(gb_location, "x")
                files_downloaded.append(split[1])

            current_file = open(gb_location, "w")

        current_file.write(line)

    # Removes temp file
    try:
        temp_file.close()
        os.remove("./temp.txt")
    except FileNotFoundError as e:
        pass

    return str(len(files_downloaded)) + " files downloaded. Names are: " + str(files_downloaded)


# Allows the user to delete all files from the folder
# Mostly for testing purposes
def delete_folder_contents():
    num_deleted = 0
    for file in os.scandir("./output/"):
        if file.name.endswith(".gb") or file.name.endswith(".fa"):
            num_deleted += 1
            os.unlink(file.path)

    return "Files Deleted: %d" % num_deleted


# Something to run to run both functions. Ultimately will be done using R
def battery(search_query, output_folder):
    return_to_r = write_gb_to_fasta(parse_ncbi(search_query, "fasta"), output_folder)
    return_to_r += "\n" + write_to_gb(parse_ncbi(search_query, "text"), output_folder)
    return return_to_r


def main():
    # delete_folder_contents()
    test_gene = "MN114084.1"
    output_folder = "./output/"

    print(battery(test_gene, output_folder))
    r = 2


if __name__ == "__main__":
    main()
