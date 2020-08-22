
from indexer import *
from shutil import copy

import glob

def move_sequences_to(out_loc):
    query = get_query_from_indexes()
    indexes = ["species", "gene"]

    # Species
    for species in query[0]:
        print(species)
        for pos in glob.glob("./storage/fa/*.*"):
            if pos.split("_")[-1].split(".")[0] == species.replace(" ", "-"):
                copy(pos, out_loc)

        for pos in glob.glob("./storage/faa/*.*"):
            print(pos.split("_")[-1].split(".")[0])
            print(pos.split("_")[-1].split(".")[0] == species.replace(" ", "-"))
            if pos.split("_")[-1].split(".")[0] == species.replace(" ", "-"):
                copy(pos, out_loc)

    # Gene
    # for gene in query[1]:
    #     for pos in glob.glob("./storage/fa/*.*"):
    #         if pos.split("_")[-1].split(".")[0] == species.replace(" ", "-"):
    #             copy(pos, out_loc)



def main():
    test_out_loc = "./output"
    move_sequences_to(test_out_loc)
    r = 2



if __name__ == '__main__':
    main()
