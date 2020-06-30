
from Bio import Entrez, SeqIO
from bs4 import BeautifulSoup


def parse_ncbi(query):
    # Always tell ncbi who you are. Using mine until testing is over and the user will input theirs
    Entrez.email = "wwinnett@iastate.edu"

    # searches for those who fit your request
    handle = Entrez.esearch(db="nucleotide", term=query)

    # Records those who match the query and then formats them so it can fetch them
    record = Entrez.read(handle)
    gi_query = ",".join(record["IdList"])

    # Fetches those matching IDs from esearch
    # rettype gb = genebank(text as retmode), fasta = fasta (use xml as retmode)
    handle = Entrez.efetch(db="nucleotide", id=gi_query, rettype="gb", retmode="xml")

    raw_data = Entrez.read(handle)
    print(raw_data[0])

    # if using an xml, then do "wb". if .txt do "w"
    # We are pulling a xml and then parsing it to get what parts we want as a fasta
    fasta_out = open("./output.txt", "w")

    # Goes through each
    for i in range(int(len(raw_data))):
        identifier = "> " + raw_data[i]["GBSeq_locus"] + " " + raw_data[i]["GBSeq_organism"]
        sequence = raw_data[i]["GBSeq_sequence"].upper()

        fasta_out.write(identifier)
        fasta_out.write("\n")

        fasta_out.write(sequence)
        fasta_out.write("\n")
        fasta_out.write("\n")


    # Writes the text to a .txt (This is mostly for testing the outputs of xml

    fasta_out.close()





# Only here for testing prior to R-shiny application
def get_info():
    # Gets information to the pass into main function
    organism_name = input("Organism name: ")
    gene_name = input("Gene name: ")
    option = input("And/or (default is And)")

    return organism_name + " OR " + gene_name if option.lower() == "or" else organism_name + " AND " + gene_name


def main():
    test_identifier = "Opuntia AND rpl16"

    parse_ncbi(test_identifier)
    # print(get_info())

    # Gve it a taxonomic id 9606
    # Download gene bank files for a taxonomic id


if __name__=="__main__":
    main()

# Commented out section
# dict_keys(['GBSeq_locus', 'GBSeq_length', 'GBSeq_strandedness', 'GBSeq_moltype',
# 'GBSeq_topology', 'GBSeq_division', 'GBSeq_update-date', 'GBSeq_create-date', 'GBSeq_definition',
# 'GBSeq_primary-accession', 'GBSeq_accession-version', 'GBSeq_other-seqids', 'GBSeq_source', 'GBSeq_organism',
# 'GBSeq_taxonomy', 'GBSeq_references', 'GBSeq_feature-table', 'GBSeq_sequence'])

#
