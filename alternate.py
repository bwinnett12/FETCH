import os

from fetcher import parse_ncbi


# interval_to = int(raw[0]["GBSeq_feature-table"][i]["GBFeature_intervals"][0]['GBInterval_to'])
def write_gb_to_fasta(raw):

    # Loops through each locus fetched
    for j in range(len(raw)):
        # Variable for the to be named output location
        out_loc = "./output/" + raw[j]["GBSeq_locus"] + ".fa"

        if not os.path.isfile(out_loc):
            current_file = open(out_loc, "x")
        current_file = open(out_loc, "w")

        # Loops through the features of each gene
        for i, feature in enumerate(raw[j]["GBSeq_feature-table"]):

            # Gene locus, Organism, Feature name
            header = ": ".join([">", raw[j]["GBSeq_locus"], raw[j]["GBSeq_organism"], feature['GBFeature_key']])

            # Goes from interval from to to
            sequence = raw[j]["GBSeq_sequence"][int(feature["GBFeature_intervals"][0]['GBInterval_from']):
                                                int(feature["GBFeature_intervals"][0]['GBInterval_to'])].upper()

            # Writes each part individually
            current_file.write(header + "\n")

            # Loops through to 75 nucleotides per line
            for n in range(0, len(sequence), 75):
                current_file.write(sequence[n:n + 75] + "\n")

            # Spacer
            current_file.write(" " + "\n")

        current_file.close()


def main():
    test_gene = "Opuntia AND rpl16"
    parsed = parse_ncbi(test_gene)
    write_gb_to_fasta(parsed)


if __name__ == "__main__":
    main()
