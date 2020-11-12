__author__ = "Bill Winnett"
__email__ = "bwinnett12@gmail.com"

import glob
import os
import time

from Bio import Entrez
from writer import battery_writer
from indexer import ensure_folder_scheme


# Parses the genebank and fetches what the user inputs
def parse_ncbi(query_from_user, output_type, email):
    # Always tell ncbi who you are. Or else it won't let you fetch
    Entrez.email = email

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
def fetch(search_query, output_folder, email):
    # In case the storage is gone for some reason
    ensure_folder_scheme(output_folder)
    search_query = search_query.split(',')

    # I like timing things
    millis_before = int(round(time.time() * 1000))

    # Staggers the fetching or else ncbi will complain
    for i in range(0, len(search_query) - 1, 2):
        sett = search_query[i:i + 2]
        # We can get away with two series then a 1 second wait
        for sing_query in sett:
            text_to_write = parse_ncbi(sing_query, "text", email)
            battery_writer("text", text_to_write, output_folder)
            # time.sleep(.25)

            xml_to_write = parse_ncbi(sing_query, "fasta", email)
            battery_writer("xml", xml_to_write, output_folder)
            # time.sleep(.25)
        time.sleep(.5)

    millis_after = int(round(time.time() * 1000))
    print("Search time (sec): ", (millis_after - millis_before) / 1000)


def delete_folder_contents(folder):
    # structure = [folder + "*", folder + "*/*"]
    structure = [folder + "*/*"]
    for style in structure:
        files = glob.glob(style)
        for f in files:
            os.remove(f)
