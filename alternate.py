import os

from fetcher import parse_ncbi


# interval_to = int(raw[0]["GBSeq_feature-table"][i]["GBFeature_intervals"][0]['GBInterval_to'])
def write_gb_to_fasta(raw):

    files_made = ""

    # Loops through each locus fetched
    for j in range(0, len(raw)):

        # Variable for the to be named output location
        out_loc = "./output/" + raw[j]["GBSeq_locus"] + ".fa"

        if not os.path.isfile(out_loc):
            current_file = open(out_loc, "x")
        current_file = open(out_loc, "w")

        # Loops through the features of each gene
        for i, feature in enumerate(raw[j]["GBSeq_feature-table"]):

            # Gene locus, Organism, Feature name
            if feature['GBFeature_key'] != "gene" or feature['GBFeature_key'] == "source":

                try:
                    header = " ".join([">", raw[j]["GBSeq_locus"], feature['GBFeature_quals'][0]['GBQualifier_value'],
                                       " - ", feature['GBFeature_quals'][2]['GBQualifier_value'],
                                       raw[j]["GBSeq_organism"]])

                    # Here for testing.. Ignore this
                    # if len(raw[j]["GBSeq_sequence"][int(feature["GBFeature_intervals"][0]['GBInterval_from']):
                    #                 int(feature["GBFeature_intervals"][0]['GBInterval_to'])].upper()) == 0:
                    #     print("zero length: " + feature['GBFeature_quals'][2]['GBQualifier_value'])
                    #     print("At: " + raw[j]["GBSeq_sequence"][int(feature["GBFeature_intervals"][0]['GBInterval_to'])])

                # For the genes that aren't setup the same as the others
                except KeyError:
                    header = " ".join([">", raw[j]["GBSeq_locus"], raw[j]["GBSeq_organism"]])
                    print("Key Error")

                # For the genes that aren't setup the same as the others
                except IndexError:
                    print(feature['GBFeature_quals'])
                    print("Index Error")

            else:
                continue

            # Goes from interval from to to
            sequence = raw[j]["GBSeq_sequence"]

            try:
                sequence = sequence[int(feature["GBFeature_intervals"][0]['GBInterval_from']):
                                    int(feature["GBFeature_intervals"][0]['GBInterval_to'])].upper()

            except KeyError:
                print(feature)

                sequence = feature['GBFeature_intervals'][0]['GBInterval_point']

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


def main():
    # test_gene = "Opuntia AND Rpl16"
    test_gene = "NC_012920"
    parsed = parse_ncbi(test_gene)
    write_gb_to_fasta(parsed)

    # print(parsed[0]["GBSeq_feature-table"][3]['GBFeature_quals'][0]['GBQualifier_value'])


if __name__ == "__main__":
    main()
