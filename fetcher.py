
from Bio import Entrez, SeqIO
import os
import sys
# import contextlib

# Debugging:
# if its a xml -> Entrez.read(handle), if its text -> handle.read()

# TODO - Have a cleaner way of sorting the files
# TODO - Have a generalized function
# TODO - Add comments to the read me

# TODO - Add exceptions to not double download or release
# TODO - Have a file checking method BEFORE parsing the gene bank


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
    handle = Entrez.efetch(db="nucleotide", id=gi_query, rettype="gb", retmode="text")

    # TODO make this part each function. Or alternatively have the function itself send this in
    # raw_data = Entrez.read(handle) # if .xml
    raw_data = handle.read()  # if text
    print(raw_data[0])

    # if using an xml, then do "wb". if .txt do "w"
    # We are pulling a xml and then parsing it to get what parts we want as a fasta

    return raw_data


# TODO - Merge this into main app or just omit and have R shiny do thi
# Only here for testing prior to R-shiny application
# Gets information to the pass into main function
def get_info():
    organism_name = input("Organism name: ")
    gene_name = input("Gene name: ")
    option = input("And/or (default is And)")

    return organism_name + " OR " + gene_name if option.lower() == "or" else organism_name + " AND " + gene_name


# TODO - Make this usable
# TODO - Add comments
# TODO - Turn it into a .fasta
# Allows for the user to download the files as fasta
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

    # Creates a temp file and saves the parsed (ncbi) data to. If no temp file, creates one
    # I know this is extra work, I'm just not sure how to do it cleaner
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

            if not os.path.isfile(gb_location):
                current_file = open(gb_location, "x")

            current_file = open(gb_location, "w")

        current_file.write(line)

    # Removes temp file
    try:
        temp_file.close()
        os.remove("./temp.txt")
    except FileNotFoundError as e:
        print(e)


def main():
    # test_identifier = "Opuntia AND rpl16"
    test_identifier = sys.argv[1]
    test_output_folder = "./output/"

    test_parse = parse_ncbi(test_identifier)

    # to_fasta(test_parse, test_output)
    to_gb(test_parse, test_output_folder)

    # Gve it a taxonomic id 9606
    # Download gene bank files for a taxonomic id


if __name__ == "__main__":
    main()

# Commented out section
# dict_keys(['GBSeq_locus', 'GBSeq_length', 'GBSeq_strandedness', 'GBSeq_moltype',
# 'GBSeq_topology', 'GBSeq_division', 'GBSeq_update-date', 'GBSeq_create-date', 'GBSeq_definition',
# 'GBSeq_primary-accession', 'GBSeq_accession-version', 'GBSeq_other-seqids', 'GBSeq_source', 'GBSeq_organism',
# 'GBSeq_taxonomy', 'GBSeq_references', 'GBSeq_feature-table', 'GBSeq_sequence'])

#
