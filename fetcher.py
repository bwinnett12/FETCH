
__author__ = "Bill Winnett"
__email__ = "bwinnett12@gmail.com"

from Bio import Entrez
from writer import write_to_gb, write_to_fasta
from indexer import reset_indexes


# TODO - Have the user to input their email
# Parses the genebank and fetches what the user inputs
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
    handle = Entrez.efetch(db="nucleotide", id=gi_query, rettype="gb", retmode=retmode_input)

    # for xml... if using .txt it should be handle.read()
    if output_type == "fasta":
        raw_data = Entrez.read(handle)
    else:
        raw_data = handle.read()

    return raw_data


# Something to run to run both functions. Ultimately will be done using R (Front End)
# TODO - make this neater
def battery(search_query, output_folder):

    return_to_r = write_to_fasta(parse_ncbi(search_query, "fasta"), output_folder)
    # return_to_r += "\n" + write_to_gb(parse_ncbi(search_query, "text"), output_folder)

    reset_indexes()

    return return_to_r


def main():

    # test_genes = ['NC_005089', 'NC_000845', 'NC_008944', 'NC_024511']
    output_folder = "./storage/"
    test_genes = ['NC_015654.1']
    test_genes = ['txid36190[Organism] mitochondria']
    test_genes = ['Human AND Mouse']
    test_genes = ['NC_015654', 'NC_0467762', 'NC_039543']



    for i in range(len(test_genes)):
        print(battery(test_genes[i], output_folder))

    # battery(test_genes, output_folder)




if __name__ == "__main__":
    main()
