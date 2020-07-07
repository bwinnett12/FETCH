
__author__ = "Bill Winnett"
__email__ = "bwinnett12@gmail.com"

import glob
import os
import sys
from Bio import Entrez


# Debugging:
# if its a xml -> Entrez.read(handle), if its text -> handle.read()

# TODO - Have a cleaner way of sorting the files
# TODO - Have a generalized function
# TODO - Add comments to the read me

# TODO - Add exceptions to not double download or release
# TODO - Have a file checking method BEFORE parsing the gene bank

# REMINDER - Change emails
def parse_ncbi(query, email):
    # Always tell ncbi who you are. Using mine until testing is over and the user will input theirs
    Entrez.email = "wwinnett@iastate.edu"

    # searches for those who fit your request
    handle = Entrez.esearch(db="nucleotide", term=query)

    # Records those who match the query and then formats them so it can fetch them
    record = Entrez.read(handle)
    gi_query = ",".join(record["IdList"])

    # Fetches those matching IDs from esearch
    # rettype gb = genebank(text as retmode), fasta = fasta (use xml as retmode)
    handle = Entrez.efetch(db="nucleotide", id=gi_query, rettype="gb", retmode="text")

    # TODO make this part each function. Or alternatively have the function itself send this in
    # raw_data = Entrez.read(handle) # if .xml
    raw_data = handle.read()  # if text
    print(raw_data[0])

    # if using an xml, then do "wb". if .txt do "w"
    # We are pulling a xml and then parsing it to get what parts we want as a fasta

    return raw_data


# TODO - Something for user email
# Gets information from R-shiny to then pass into main function
def get_info():
    organism_name = sys.argv[1]
    gene_name = sys.argv[2]
    option = sys.argv[3]

    # For the email. I'm just using mine for testing purposes
    # email = sys.argv[4]

    return " ".join([organism_name, option, gene_name])


# TODO - Make this usable
# TODO - Add comments
# TODO - Turn it into a .fasta
# Allows for the user to download the files as fasta
# Only allows for one large File. Probably won't add individuals unless requested
def to_fasta(raw_data, output_location):
    fasta_out = open(output_location, "w")

    for i in range(int(len(raw_data))):
        identifier = "> " + raw_data[i]["GBSeq_locus"] + " " + raw_data[i]["GBSeq_organism"]
        sequence = raw_data[i]["GBSeq_sequence"].upper()

        fasta_out.write(identifier)
        fasta_out.write("\n")

        fasta_out.write(sequence)
        fasta_out.write("\n")
        fasta_out.write("\n")


# TODO - Figure out a way to not use a temp file
# TODO - Add exceptions in case it doesn't work
def to_gb(raw_data, output_folder):

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


def battery(search, email, method, output_location):

    print("Got to battery")
    output_location = "./output/"
    method = "esame"
    return_to_r = ""

    if method == "gb" or method == "esame":
        print("Got to to_gb")
        return_to_r = to_gb(parse_ncbi(search, email), output_location)

    elif method == "fasta":
        # TODO - make this return something
        return_to_r = to_fasta(parse_ncbi(search, email), output_location)
    else:
        return_to_r = "Failed"
        print("Failed")
        return "Failed"

    print("exited function")
    return return_to_r


def delete_folder_contents():
    # files = glob.glob("./output/")
    # for f in files:
    #     os.remove(f)

    for file in os.scandir("./output/"):
        if file.name.endswith(".gb"):
            os.unlink(file.path)


def main():
    test_identifier = "Opuntia AND rpl16"
    r = 2
    # test_output_folder = "./output/"
    # print(battery(test_identifier, " ", "esame", " "))

    # delete_folder_contents()


if __name__ == "__main__":
    main()




# Commented out section
# dict_keys(['GBSeq_locus', 'GBSeq_length', 'GBSeq_strandedness', 'GBSeq_moltype',
# 'GBSeq_topology', 'GBSeq_division', 'GBSeq_update-date', 'GBSeq_create-date', 'GBSeq_definition',
# 'GBSeq_primary-accession', 'GBSeq_accession-version', 'GBSeq_other-seqids', 'GBSeq_source', 'GBSeq_organism',
# 'GBSeq_taxonomy', 'GBSeq_references', 'GBSeq_feature-table', 'GBSeq_sequence'])

#
