import glob

"""
This module is a way to work with the indexes that are used for pulling and keeping track of the files
Features: adding, deleting, resetting, and refreshing.
Helpers: open_clarify(reduces 4 lines to 1), check_index(Looks through the index)
"""


# Adds a term to index. Either to genes.lst or species.lst
def add_to_index(index, term):
    file = open(open_clarify(index), "a+")

    # If term not there, appends to end
    if not check_index(index, term):
        file.write(";" + term.lower() + "\n")
    file.close()


# Deletes a term from the index. Either to genes.lst or species.lst
# Deleting entries is harder than adding, files needs to be re-written for each entry
def delete_from_index(index, term):
    # Stores all of the data in "lines"
    file = open(open_clarify(index), "r+")

    lines = file.readlines()
    file.close()

    # Opens the list to write to it
    file = open(open_clarify(index), "w")

    # writes every line EXCEPT the one that needs to be deleted
    for line in lines:
        if term not in line:
            file.write(line)

    file.close()


# Function that cycles through the .lst to see if the term is there
# Helper just for saving time
def check_index(index, term):
    file = open(open_clarify(index), "r")

    for line in file.readlines():
        # if line == (term + "\n") or line == (";" + term + "\n") or line == term or line == (";" + term):
        if term.lower() in line:
            file.close()
            return True
    file.close()
    return False


# Sets the index back to none selected (;gene vs gene)
# Also resets the indexes to what is found inside the storage folder
# TODO - Stop hard-coding the path and Make reseting indexes optional
def reset_indexes():
    # Gets a list of all the fasta... Uses this to update the indexes with whats found
    def get_file_list(index):

        path = "./storage/"

        fulllist = []

        if index == "species":
            for file in glob.glob("./storage/gb/*.gb"):
                fulllist.append(file.split("/")[-1].split(".")[0])
            for file in glob.glob("./storage/full_fa/*.fa"):
                fulllist.append(file.split("/")[-1].split(".")[0])

        if index == "genes":
            for file in glob.glob("./storage/fa/*.fa"):
                fulllist.append(file.split("/")[-1].split("_")[0])
            for file in glob.glob("./storage/faa/*.faa"):
                fulllist.append(file.split("/")[-1].split("_")[0])

        return list(set(fulllist))

    # Ran once for each index
    for index in ["species", "genes"]:

        # Gets an accurate list of what is in the local files (Currently ./storage/)
        full_list = get_file_list(index)

        file = open(open_clarify(index), "w")
        file.close()

        # Saves full_list to replace index
        for entry in full_list:
            add_to_index(index, entry)

        # Saves lines of index to be then added back in later unchecked (with ;)
        file = open(open_clarify(index), "r")
        lines = file.readlines()
        file.close()

        file = open(open_clarify(index), "w")

        # Adds a semicolon if there isn't a semicolon
        # TODO - Make this optional. Might stink to do after specifying many genes
        for line in lines:
            if line[0] == ";":
                file.write(line)
            else:
                file.write(";" + line)
        file.close()

        # Refreshes to organize and sort it again
        refresh(index)


# Does normalization on lists
# Sorts alphabetically,
def refresh(index):
    # Common recursive sort algorithm for sorting through each index. So widespread that it doesn't need comments
    def quicksort(R):
        if len(R) < 2:
            return R

        pivot = R[0]
        low = quicksort([i for i in R if i < pivot])
        high = quicksort([i for i in R if i > pivot])
        return low + [pivot] + high

    # Copies all of the info from the indexes first. then sorts the lines.
    file = open(open_clarify(index), "r+")

    appended = []
    for line in file.readlines():
        if ';' in line:
            appended.append(line.split(";")[-1].split("\n")[0])

    file.seek(0)

    lines = quicksort([gene.strip(";") for gene in file.readlines()])
    file.close()

    # Reopens so it can paste back in
    file = open(open_clarify(index), "w")

    # Has to rewrite everything
    for line in lines:
        print(line.strip("\n"))
        file.write(";" + str(line)) if line.strip("\n") in appended else file.write(line)
    file.close()


# Finds which genes are unmarked to pull from the local files
# TODO - Make the structure a dictionary rather than an array
def get_query_from_indexes():
    # [[species], [genes]]
    query_to_fetch = [[], []]
    indexes = ["species", "genes"]

    # loops twice. Once for each index
    for i in range(len(indexes)):
        lines = open(open_clarify(indexes[i]))

        # Picks up all the unmarked ones and adds to a list
        for line in lines:
            if ";" not in line:
                query_to_fetch[i].append(line.split("\n")[0])

    return query_to_fetch


# A helper method for simplifying all of the other methods
def open_clarify(index):
    if index.lower() == "species":
        return "./Indexes/species.lst"
    elif index.lower() == "genes":
        return "./Indexes/genes.lst"
    else:
        return False


def main():
    print("Hello from indexer")
    # reset_indexes()
    # refresh("genes")


if __name__ == '__main__':
    main()


# Very pythonic alternative to the quicksort from earlier
def quick_sort(array):
    if len(array) <= 1:
        return array
    else:
        return quick_sort([e for e in array[1:] if e <= array[0]]) + [array[0]] + quick_sort(
            [e for e in array[1:] if e > array[0]])
