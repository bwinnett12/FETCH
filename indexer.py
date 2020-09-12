
import glob

# Adds a term to index. Either to genes.lst or species.lst
def add_to_index(index, term):

    file = open(open_clarify(index), "a+")

    # If term not there, appends to end
    if not check_index(index, term):
        file.write(";" + term + "\n")
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
        if line == (term + "\n") or line == (";" + term + "\n") or line == term or line == (";" + term):
            file.close()
            return True
    file.close()
    return False


# Sets the index back to none selected (;gene vs gene)
def reset_indexes():

    # Gets a list of all the fasta... Uses this to update the indexes with whats found
    def get_file_list(index):

        lines = open(open_clarify(index), "r")
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

        # Gets an accurate list of what is in the local files (Currently ./storage/
        full_list = get_file_list(index)

        # Saves full_list to replace index
        for entry in full_list:
            add_to_index(index, entry)

        # Saves lines of index to be then added back in with a
        file = open(open_clarify(index), "r+")
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
        refresh(index)






# Does normalization on lists
# Sorts alphabetically,
def refresh(index):

    # Common recursive sort algorithm for sorting through each index
    def quicksort(R):
        if len(R) < 2:
            return R

        pivot = R[0]
        low = quicksort([i for i in R if i < pivot])
        high = quicksort([i for i in R if i > pivot])
        return low + [pivot] + high


    file = open(open_clarify(index), "r+")
    lines = quicksort(file.readlines())
    file.close()

    file = open(open_clarify(index), "w")

    # Has to rewrite everything
    for line in lines:
        file.write(line)
    file.close()


# Finds which genes are unmarked to pull from the local files
def get_query_from_indexes():
    # [[species], [genes]]
    query_to_fetch = [[], []]
    indexes = ["species", "genes"]

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
    test_index = "genes"
    test_term = "Catt"

    test_array = [3,4,5,1,7,2,8,20]
    test_array_long = ["Bob", "chad", "Kyle", "Tom", "Fred", "d qs", "dqwd ", "!", "d w ", "gr we"," feqw", " few"]

    print("Hello from indexer")
    # add_to_index(test_index, test_term)

    # reset_index(test_index)
    # delete_from_index(test_index, test_term)

    # refresh(test_index)
    reset_indexes()





def sandbox():
    r = 2



if __name__ == '__main__':
    main()


def quick_sort(array):
    if len(array) <= 1:
        return array
    else:
        return quick_sort([e for e in array[1:] if e <= array[0]]) + [array[0]] + quick_sort(
            [e for e in array[1:] if e > array[0]])
