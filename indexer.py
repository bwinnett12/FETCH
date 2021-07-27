import glob
import os

"""
This module is a way to work with the indexes that are used for pulling and keeping track of the files
Features: adding, deleting, resetting, and refreshing.
Helpers: open_clarify(reduces 4 lines to 1), check_index(Looks through the index)
"""


# Deletes a term from the index. Either to genes.lst or species.lst
# Deleting entries is harder than adding, files needs to be re-written for each entry
def delete_from_index(term, index, index_type, indexes_path):
    # Stores all of the data in "lines"
    file = open(open_clarify(index, index_type, indexes_path), "r+")

    lines = file.readlines()
    file.close()

    # Opens the list to write to it
    file = open(open_clarify(term, index, indexes_path), "w")

    # writes every line EXCEPT the one that needs to be deleted
    for line in lines:
        if term not in line:
            file.write(line)


# Sets the index back to none selected (;gene vs gene)
# Also resets the indexes to what is found inside the storage folder
def reset_indexes(storage_path, indexes_path):

    # Gets a list of all the fasta... Uses this to update the indexes with whats found
    def get_file_list(index, path):
        path = path.rstrip("/")
        fulllist = []

        if index == "species":
            for file in glob.glob(path + "/gb/*.gb"):
                fulllist.append(file.split("/")[-1].split(".")[0])
            for file in glob.glob(path + "/full_fa/*.fa"):
                fulllist.append(file.split("/")[-1].split(".")[0])

        if index == "genes":
            for file in glob.glob(path + "/fa/*.fa"):
                fulllist.append(file.split("/")[-1].split("_")[0])
            for file in glob.glob(path + "/faa/*.faa"):
                fulllist.append(file.split("/")[-1].split("_")[0])

        return list(set(fulllist))

    # Ran once for each index
    for index in ["species", "genes"]:

        # Gets an accurate list of what is in the local files (Currently ./storage/)
        full_list = get_file_list(index, storage_path)

        file = open(open_clarify("master", index, indexes_path), "w")

        # Saves full_list to replace index
        for entry in full_list:
            entry = entry.rstrip("_full")  # Catch for species on "full_fa"
            if os.name == "nt":
                file.write(";" + entry.split('\\')[-1] + "\n")
            else:
                file.write(";" + entry + "\n")

        # Saves lines of index to be then added back in later unchecked (with ;)
        file = open(open_clarify("master", index, indexes_path), "r")
        lines = file.readlines()
        file.close()

        file = open(open_clarify("master", index, indexes_path), "w")

        # Adds a semicolon if there isn't a semicolon
        for line in lines:
            if line[0] == ";":
                file.write(line)
            else:
                file.write(";" + line)
        file.close()

        # Refreshes to organize and sort it again
        refresh("master", index, indexes_path)
    fill_gene_indexes(indexes_path, storage_path)
    fill_species_indexes(indexes_path, storage_path)


# Does normalization on lists
# Sorts alphabetically,
def refresh(index, index_type, indexes_path):
    # Common recursive sort algorithm for sorting through each index. So widespread that it doesn't need comments
    def quicksort(R):
        if len(R) < 2:
            return R

        pivot = R[0]
        low = quicksort([i for i in R if i < pivot])
        high = quicksort([i for i in R if i > pivot])
        return low + [pivot] + high

    # Copies all of the info from the indexes first. then sorts the lines.
    # BUT FIRST, we have to get the right file
    file = open(open_clarify(index, index_type, indexes_path), "r+")

    appended = []
    for line in file.readlines():
        if ';' in line:
            appended.append(line.split(";")[-1].split("\n")[0])

    # Reset the pointer location to beginning to re-get lines
    file.seek(0)

    lines = quicksort([gene.strip(";") for gene in file.readlines()])
    file.close()

    # Reopens so it can paste back in
    file = open(open_clarify(index, index_type, indexes_path), "w")

    # Has to rewrite everything
    for line in lines:
        file.write(";" + str(line)) if line.strip("\n") in appended else file.write(line)
    file.close()


def fill_gene_indexes(indexes_path, storage_path):
    def get_file_list(path):   # Returns a list of all file available in storage
        path = path.rstrip("/")
        fulllist = []

        for file in glob.glob(path + "/fa/*.fa"):
            fulllist.append(file.split("/")[-1])
        for file in glob.glob(path + "/faa/*.faa"):
            fulllist.append(file.split("/")[-1])

        return list(set(fulllist))

    gene_list_lines = open(indexes_path.rstrip("/") + "/genes.lst", "r").readlines()
    all_files = get_file_list(storage_path)

    species_list = []  # Writes to a list to keep track of whats been added
    for gene in gene_list_lines:
        gene = gene.lstrip(";").rstrip("\n")

        # Creates an index file if one is not present. Else, opens one
        file_gene_index = open(open_clarify(gene, "genes", indexes_path), "w")

        for file_storage in all_files:  # Check if gene is in the name of the file, then adds

            split_file_storage = file_storage.split("_")  # index 0 is the gene and index 1 is the species
            # If first part of file is gene and is not part of the gene
            if split_file_storage[0] == gene and split_file_storage[1].split(".")[0] not in species_list:

                file_gene_index.write(";" + split_file_storage[1].split(".")[0] + "\n")  # Writes to the index
                species_list.append(split_file_storage[1].split(".")[0])  # THe list of whats in the file

        file_gene_index.close()  # Closes the file early so that refresh works
        refresh(gene, "genes", indexes_path)
        species_list = []  # Resets for the next gene


# Updates species indexes
def fill_species_indexes(indexes_path, storage_path):
    def get_file_list(path):   # Returns a list of all file available in storage
        path = path.rstrip("/")
        fulllist = []

        for file in glob.glob(path + "/fa/*.fa"):
            fulllist.append(file.split("/")[-1])
        for file in glob.glob(path + "/faa/*.faa"):
            fulllist.append(file.split("/")[-1])

        return list(set(fulllist))

    species_list_lines = open(open_clarify("master", "species", indexes_path), "r").readlines()
    all_files = get_file_list(storage_path)
    genes_list = []

    for species in species_list_lines:
        species = species.lstrip(";").rstrip("\n")

        # Creates an index file if one is not present. Else, opens one
        file_species_index = open(open_clarify(species, "species", indexes_path), "w")

        for file_storage in all_files:  # Check if species is in the name of the file, then adds to index

            split_file_storage = file_storage.split("_")  # index 0 is the gene and index 1 is the species
            split_file_storage[1] = split_file_storage[1].split(".")[0]

            # If first part of file is gene and is not part of the gene
            if split_file_storage[1] == species and split_file_storage[0] not in genes_list:
                file_species_index.write(";" + split_file_storage[0] + "\n")  # Writes to the index
                genes_list.append(split_file_storage[0])  # THe list of whats in the file

        file_species_index.close()  # Closes the file early so that refresh works
        refresh(species, "species", indexes_path)
        genes_list = []  # Resets for the next gene


# Finds which genes are unmarked to pull from the local files
# TODO - Make the structure a dictionary rather than an array
def get_query_from_indexes(indexes_path):
    # [[species], [genes]]
    query_to_fetch = [[], []]
    indexes = ["species", "genes"]

    # loops twice. Once for each index
    for i in range(len(indexes)):
        lines = open(open_clarify("master", indexes[i], indexes_path))

        # Picks up all the unmarked ones and adds to a list
        for line in lines:
            if ";" not in line:
                query_to_fetch[i].append(line.split("\n")[0])

    return query_to_fetch


# Sets up a default folder scheme for storage in any specified location
def ensure_folder_scheme_storage(path):
    folders = ["/fa/", "/full_fa/", "/faa/", "/full_faa/", "/gb/", "/genome/"]
    for folder in folders:
        os.makedirs(path.rstrip("/") + folder, exist_ok=True)


# Sets up a default folder scheme for indexes
def ensure_folder_scheme_indexes(path):
    folders = ["/genes/", "/species/"]
    for folder in folders:
        os.makedirs(path.rstrip("/") + folder, exist_ok=True)

    # To ensure genes.lst is present
    if not os.path.isfile(path.rstrip("/") + "/genes.lst"):
        current_file = open(path.rstrip("/") + "/genes.lst", "x")

    # To ensure species.lst is present
    if not os.path.isfile(path.rstrip("/") + "/species.lst"):
        current_file = open(path.rstrip("/") + "/species.lst", "x")


# A helper method for simplifying individual indexes
def open_clarify(index, index_type, index_path):
    if index.lower() == "master":
        if index_type.lower() == "species":
            return index_path.rstrip("/") + "/species.lst"
        elif index_type.lower() == "genes":
            return index_path.rstrip("/") + "/genes.lst"
        else:
            return False

    if index_type.lower() == "species":
        # In case of a new gene or species, then creates a new file
        record_index = index_path.rstrip("/") + "/species/" + index + ".lst"
        if not os.path.isfile(record_index):
            current_file = open(record_index, "x")
        return record_index

    elif index_type.lower() == "genes":
        # In case of a new gene or species, then creates a new file
        record_index = index_path.rstrip("/") + "/genes/" + index + ".lst"
        if not os.path.isfile(record_index):
            current_file = open(record_index, "x")
        return record_index
    else:
        return False
