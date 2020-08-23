import os

from Bio import SeqIO
from indexer import get_query_from_indexes
from shutil import copy

import glob

def move_individual_fasta_to(out_loc):
    query = get_query_from_indexes()

    # Species
    for species in query[0]:
        print(species)
        for pos in glob.glob("./storage/fa/*.fa"):
            if pos.split("_")[-1].split(".")[0] == species.replace(" ", "-"):
                copy(pos, out_loc)

        for pos in glob.glob("./storage/faa/*.faa"):
            if pos.split("_")[-1].split(".")[0] == species.replace(" ", "-"):
                copy(pos, out_loc)

        for pos in glob.glob("./storage/gb/*.gb"):
            print(pos.split("/")[-1].split(".")[0] == species.replace(" ", "-"))
            if pos.split("/")[-1].split(".")[0] == species.replace(" ", "-"):
                copy(pos, out_loc)


    # Gene
    for gene in query[1]:
        for pos in glob.glob("./storage/fa/*.fa"):
            # print(pos.split("_")[0].split("/")[-1], gene)
            if pos.split("_")[0].split("/")[-1] == gene:
                copy(pos, out_loc)

        for pos in glob.glob("./storage/faa/*.faa"):
            # print(pos.split("_")[0].split("/")[-1], gene)
            if pos.split("_")[0].split("/")[-1] == gene:
                copy(pos, out_loc)



def pull_query_to_fasta(out_loc):
    query = get_query_from_indexes()

    for gene in query[1]:

        out_loc_file = out_loc + gene + ".fa"

        if not os.path.isfile(out_loc_file):
            current_file = open(out_loc_file, "x")
        current_file = open(out_loc_file, "w")

        files_array = []

        for pos in glob.glob("./storage/fa/*.fa"):
            if pos.split("_")[0].split("/")[-1] == gene:
                files_array.append(pos)


        for file in files_array:

            # TODO - Fix this so it reads the files
            for record in SeqIO.parse(file, "fasta"):
                current_file.write(">" + record.description + " " + str(len(record.seq)) + "\n")

                for n in range(0, len(record.seq), 75):
                    current_file.write(str(record.seq[n:n + 75]) + "\n")
                current_file.write("\n")

        current_file.close()
        # print(files_array)



def main():
    test_out_loc = "./output/"
    # move_sequences_to(test_out_loc)
    pull_query_to_fasta(test_out_loc)
    r = 2



if __name__ == '__main__':
    main()
