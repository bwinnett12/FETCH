
__author__ = "Bill Winnett"
__email__ = "bwinnett12@gmail.com"

import glob
import os

from Bio import Entrez
from writer import battery_writer
from indexer import reset_indexes


# TODO - Have the user to input their email
# Parses the genebank and fetches what the user inputs
def parse_ncbi(query_from_user, output_type, email):

    # Always tell ncbi who you are. Using mine until testing is over and the user will input theirs
    Entrez.email = "wwinnett@iastate.edu"

    # searches for those who fit your request
    handle = Entrez.esearch(db="nucleotide", term=query_from_user)

    # Records those who match the query and then formats them so it can fetch them
    record = Entrez.read(handle)
    gi_query = ",".join(record["IdList"])

    retmode_input = ("text", "xml")[output_type == "fasta"]

    # Fetches those matching IDs from esearch
    handle = Entrez.efetch(db="nucleotide", id=gi_query, rettype="gb", retmode=retmode_input)

    # for xml... if using .txt it should be handle.read()
    if output_type == "fasta":
        raw_data = Entrez.read(handle)
    else:
        raw_data = handle.read()

    return raw_data


# Something to run to run both functions. Ultimately will be done using R (Front End)
# TODO - make this neater
def fetch(search_query, output_folder, email):
    for sing_query in search_query.split(","):
        text_to_write = parse_ncbi(sing_query, "text", email)
        battery_writer("text", text_to_write, output_folder)

    xml_to_write = parse_ncbi(search_query, "fasta", email)
    battery_writer("xml", xml_to_write, output_folder)


def delete_folder_contents(folder):
    # structure = [folder + "*", folder + "*/*"]
    structure = [folder + "*/*"]
    for style in structure:
        files = glob.glob(style)
        for f in files:
            os.remove(f)


def main():
    print("hello from fetcher! \n Try running everything from main.py or through python3 main.py --help")


if __name__ == "__main__":
    main()
