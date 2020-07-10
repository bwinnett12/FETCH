
__author__ = "Bill Winnett"
__email__ = "bwinnett12@gmail.com"

import os
import sys
from Bio import Entrez


# Debugging:
# if its a xml -> Entrez.read(handle), if its text -> handle.read()

# TODO - Have a cleaner way of sorting the files
# TODO - Add exceptions to not double download or release
def parse_ncbi(query_from_user):

    # Always tell ncbi who you are. Using mine until testing is over and the user will input theirs
    Entrez.email = "wwinnett@iastate.edu"

    # searches for those who fit your request
    handle = Entrez.esearch(db="nucleotide", term=query_from_user)

    # Records those who match the query and then formats them so it can fetch them
    record = Entrez.read(handle)
    gi_query = ",".join(record["IdList"])

    # TODO - add rhis back in
    # rettype_input = ("gb", "fasta")[out_type == "fasta"]
    # retmode_input = ("text", "xml")[out_type == "fasta"]

    # Fetches those matching IDs from esearch
    # rettype gb = genebank(text as retmode), fasta = fasta (use xml as retmode)
    # handle = Entrez.efetch(db="nucleotide", id=gi_query, rettype=rettype_input, retmode=retmode_input)
    handle = Entrez.efetch(db="nucleotide", id=gi_query, rettype="gb", retmode="xml")

    # for xml... if using .txt it should be handle.read()
    raw_data = Entrez.read(handle)

    return raw_data

    # if using an xml, then do "wb". if .txt do "w"
    # We are pulling a xml and then parsing it to get what parts we want as a fasta


# interval_to = int(raw[0]["GBSeq_feature-table"][i]["GBFeature_intervals"][0]['GBInterval_to'])
def write_gb_to_fasta(raw):

    files_made = ""

    # Loops through each locus fetched
    for j in range(len(raw)):
        # Variable for the to be named output location
        out_loc = "./output/" + raw[j]["GBSeq_locus"] + ".fa"

        if not os.path.isfile(out_loc):
            current_file = open(out_loc, "x")
        current_file = open(out_loc, "w")

        # Loops through the features of each gene
        for i, feature in enumerate(raw[j]["GBSeq_feature-table"]):

            # Gene locus, Organism, Feature name
            header = ": ".join([">", raw[j]["GBSeq_locus"], raw[j]["GBSeq_organism"], feature['GBFeature_key']])

            # Goes from interval from to to
            sequence = raw[j]["GBSeq_sequence"][int(feature["GBFeature_intervals"][0]['GBInterval_from']):
                                                int(feature["GBFeature_intervals"][0]['GBInterval_to'])].upper()

            # Writes each part individually
            current_file.write(header + "\n")

            # Loops through to 75 nucleotides per line
            for n in range(0, len(sequence), 75):
                current_file.write(sequence[n:n + 75] + "\n")

            # Spacer
            current_file.write(" " + "\n")

        files_made += raw[j]["GBSeq_locus"] + ", "
        current_file.close()
    return "Files downloaded: " + files_made


# TODO - Figure out a way to not use a temp file (REDO basically)
# TODO - Add exceptions in case it doesn't work
def to_gb(raw_data, output_folder):

    if raw_data == "":
        return "No files downloaded. Search query had no results"

    files_downloaded = []
    # Creates a temp file and saves the parsed (ncbi) data to. If no temp file, creates one
    # I know this is extra work, but I'm just not sure how to do it cleaner
    try:
        temp_file = open("./temp.txt", "x")
    except FileExistsError as e:
        pass

    temp_file = open("./temp.txt", "w")
    temp_file.write(raw_data)

    # parses data from text and saves it as a line
    with open('./temp.txt', 'r') as raw_text:
        lines = raw_text.readlines()

    # Declares a variable to write to. This will be changed to Locus ID after first iteration
    current_file = temp_file

    # TODO - Refine and add exceptions
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
        if file.name.endswith(".gb"):
            num_deleted += 1
            os.unlink(file.path)

    return "Files Deleted: %d" % num_deleted


def battery(search_query):

    return_to_r = write_gb_to_fasta(parse_ncbi(search_query))

    return return_to_r


def main():
    test_query = "Opuntia AND rpl16"

    # print(battery("Optunia AND rpl16", "Wwinnett@iastate.edu", "fasta", "./output/"))
    # print(battery("Opuntia AND rpl16", "Wwinnett@iastate.edu", "gb", "./output/"))
    print(battery(test_query))

    # print(parse_ncbi("Opuntia AND rp116", "Wwinnett@iastate.edu", "gb", "./output/"))

    r = 2


if __name__ == "__main__":
    main()
