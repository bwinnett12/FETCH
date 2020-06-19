
from bio import Entrez


def parse_ncbi(query):
    # Always tell ncbi who you are. Using mine until testing is over and the user will input theirs
    Entrez.email = "wwinnett@iastate.edu"

    # searches for those who fit your request
    handle = Entrez.esearch(db="nucleotide", term=query)

    # Records those who match the query and then formats them so it can fetch them
    record = Entrez.read(handle)
    gi_query = ",".join(record["IdList"])

    # Fetches those matching IDs from esearch
    handle = Entrez.efetch(db="nucleotide", id=gi_query, rettype="gb", retmode="text")

    # Writes the text to a .txt (This is mostly for testing the outputs of xml
    text = handle.read()
    print(text)   # Just to show what the output looks like (in xml)
    print(len(text))

    # if using an xml, then do "wb". if .txt do "w"
    xml_out = open("./output.txt", "w")
    # xml_out.write(text)
    xml_out.write(text)

    print(handle.read())
    xml_out.close()


def main():
    test_identifier = "Opuntia AND rpl16"

    parse_ncbi(test_identifier)

    # Gve it a taxonomic id 9606
    # Download gene bank files for a taxonomic id


if __name__=="__main__":
    main()

