
__author__ = "Bill Winnett"
__email__ = "bwinnett12@gmail.com"

import os
import sys
from Bio import Entrez


# Debugging:
# if its a xml -> Entrez.read(handle), if its text -> handle.read()

# TODO - Have a cleaner way of sorting the files
# TODO - Add exceptions to not double download or release
# TODO - Have a file checking method BEFORE parsing the gene bank
def parse_ncbi(query_from_user, email, out_type, out_location):
    print(query_from_user)
    query = query_from_user

    # print("Opuntia AND rpl16" == query_from_user)
    print(query_from_user == query)
    # Always tell ncbi who you are. Using mine until testing is over and the user will input theirs
    Entrez.email = email

    # searches for those who fit your request
    handle = Entrez.esearch(db="nucleotide", term=query)

    # Records those who match the query and then formats them so it can fetch them
    record = Entrez.read(handle)
    gi_query = ",".join(record["IdList"])

    rettype_input = ("gb", "fasta")[out_type == "fasta"]
    retmode_input = ("text", "xml")[out_type == "fasta"]

    # Fetches those matching IDs from esearch
    # rettype gb = genebank(text as retmode), fasta = fasta (use xml as retmode)
    handle = Entrez.efetch(db="nucleotide", id=gi_query, rettype=rettype_input, retmode=retmode_input)

    # TODO make this part each function. Or alternatively have the function itself send this in\

    if retmode_input == "xml":
        raw_data = Entrez.read(handle)

    else:
        raw_data = handle.read()

    return raw_data

    # if using an xml, then do "wb". if .txt do "w"
    # We are pulling a xml and then parsing it to get what parts we want as a fasta

    print(raw_data)
    return raw_data


# TODO - Make this usable
# TODO - Add comments
# TODO - Turn it into a .fasta
# Allows for the user to download the files as fasta
# Only allows for one large File. Probably won't add individuals unless requested
def to_fasta(raw_data, output_location):
    print("got to to_fasta")
    fasta_out = open(output_location, "wb")
    genes_written = []

    # print(raw_data[0]["GBSeq_locus"])

    for i in range(int(len(raw_data))):
        identifier = "> " + raw_data[i]["GBSeq_locus"] + " " + raw_data[i]["GBSeq_organism"]
        sequence = raw_data[i]["GBSeq_sequence"].upper()

        fasta_out.write(identifier)
        fasta_out.write("\n")

        fasta_out.write(sequence)
        fasta_out.write("\n")
        fasta_out.write("\n")

        genes_written += raw_data[i]["GBSeq_locus"]

    return str(int(len(raw_data))) + " sequences written to a file. \n Sequences: " + genes_written


# TODO - Figure out a way to not use a temp file
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


def battery(search, email, out_type, output_location):
    if out_type == "gb" or out_type == "esame":
        return_to_r = to_gb(parse_ncbi(search, email, "gb", output_location), output_location)

    elif out_type == "fasta":
        return_to_r = to_fasta(parse_ncbi(search, email, "fasta", output_location), output_location + "test.fa")

    else:
        return "Failed"

    return return_to_r


def main():
    # delete_folder_contents()

    # print(battery("Optunia AND rpl16", "Wwinnett@iastate.edu", "fasta", "./output/"))
    # print(battery("Opuntia AND rpl16", "Wwinnett@iastate.edu", "gb", "./output/"))

    # print(parse_ncbi("Opuntia AND rp116", "Wwinnett@iastate.edu", "gb", "./output/"))

    r = 2


if __name__ == "__main__":
    main()
