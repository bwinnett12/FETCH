
__author__ = "Bill Winnett"
__email__ = "bwinnett12@gmail.com"

import os
from Bio import Entrez
from writer import write_to_gb, write_to_fasta


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


# Allows the user to delete all files from the folder
# Mostly for testing purposes
def delete_folder_contents():
    num_deleted = 0
    for file in os.scandir("./output/"):
        if file.name.endswith(".gb") or file.name.endswith(".fa"):
            num_deleted += 1
            os.unlink(file.path)

    return "Files Deleted: %d" % num_deleted


# Something to run to run both functions. Ultimately will be done using R (Front End)
def battery(search_query, output_folder):

    table = {
        'ATA': 'I', 'ATC': 'I', 'ATT': 'I', 'ATG': 'M',
        'ACA': 'T', 'ACC': 'T', 'ACG': 'T', 'ACT': 'T',
        'AAC': 'N', 'AAT': 'N', 'AAA': 'K', 'AAG': 'K',
        'AGC': 'S', 'AGT': 'S', 'AGA': 'R', 'AGG': 'R',
        'CTA': 'L', 'CTC': 'L', 'CTG': 'L', 'CTT': 'L',
        'CCA': 'P', 'CCC': 'P', 'CCG': 'P', 'CCT': 'P',
        'CAC': 'H', 'CAT': 'H', 'CAA': 'Q', 'CAG': 'Q',
        'CGA': 'R', 'CGC': 'R', 'CGG': 'R', 'CGT': 'R',
        'GTA': 'V', 'GTC': 'V', 'GTG': 'V', 'GTT': 'V',
        'GCA': 'A', 'GCC': 'A', 'GCG': 'A', 'GCT': 'A',
        'GAC': 'D', 'GAT': 'D', 'GAA': 'E', 'GAG': 'E',
        'GGA': 'G', 'GGC': 'G', 'GGG': 'G', 'GGT': 'G',
        'TCA': 'S', 'TCC': 'S', 'TCG': 'S', 'TCT': 'S',
        'TTC': 'F', 'TTT': 'F', 'TTA': 'L', 'TTG': 'L',
        'TAC': 'Y', 'TAT': 'Y', 'TAA': '_', 'TAG': '_',
        'TGC': 'C', 'TGT': 'C', 'TGA': '_', 'TGG': 'W',
    }

    return_to_r = write_to_fasta(parse_ncbi(search_query, "fasta"), output_folder, table)
    return_to_r += "\n" + write_to_gb(parse_ncbi(search_query, "text"), output_folder)
    return return_to_r


def main():


    # delete_folder_contents()
    test_gene = "QEHR01000001"
    output_folder = "./output/"

    print(battery(test_gene, output_folder))
    r = 2


if __name__ == "__main__":
    main()
