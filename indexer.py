
# Adds a term to index. Either to genes.lst or species.lst
import os


def add_to_index(index, term):

    file = open(open_clarify(index), "a+")

    # If term not there, appends to end
    if not check_index(index, term):
        file.write(";" + term + "\n")
    file.close()

    # refresh(index)


# Deletes a term from the index. Either to genes.lst or species.lst
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
def reset_index(index):

    # Gets a list of all the fasta... Uses this to update the indexes with whats found
    def get_file_list():

        lines = open(open_clarify(index), "r")
        path = "./storage/"

        fulllist = []

        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".fa"):
                    if os.path.join(root, file).split("/")[-1] not in lines and\
                            os.path.join(root, file).split("/")[-1] not in fulllist:
                        fulllist.append(os.path.join(root, file).split("/")[-1])
        return fulllist

    full_list = get_file_list()

    for entry in full_list:
        add_to_index(index, entry)


    file = open(open_clarify(index), "r+")
    lines = file.readlines()
    file.close()

    file = open(open_clarify(index), "w")

    # Adds a semicolon if there isn't a semicolon
    for line in lines:
        if line[0] == ";":
            file.write(line)
        else:
            file.write(";" + line)
    file.close()





# Does normalization on lists
# Sorts alphabetically,
# TODO - set up refreshing of downloaded files
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

    print("Hello")
    # add_to_index(test_index, test_term)

    # reset_index(test_index)
    # delete_from_index(test_index, test_term)

    refresh(test_index)








def sandbox():
    r = 2
    # mydb = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     password="",
    #     database="testdb"
    # )
    #
    # mycursor = mydb.cursor()

    # mycursor.execute("CREATE TABLE students (name VARCHAR(255), age INTEGER(10))")
    # mycursor.execute()

    # for db in mycursor:
    #     print(db)

    # for tb in mycursor:
    #     print(tb)
    #
    # sqlFormula = "INSERT INTO students (name, age) VALUES (%s, %s)"
    #
    # students = [("Rachel", 22), ("Bob", 21), ("Jacob", 23), ("Ryan", 26), ("Rachel", 12)]
    # student1 = ("Rachel", 22)
    # student2 = ("James", 21)
    #
    # mycursor.executemany(sqlFormula, students)
    #
    # for tb in mycursor:
    #     print(tb)

    # mycursor.execute("SELECT * FROM students")
    # myresult = mycursor.fetchall()
    #
    # for row in myresult:
    #     print(row)

    # mydb.commit()



if __name__ == '__main__':
    main()


def quick_sort(array):
    if len(array) <= 1:
        return array
    else:
        return quick_sort([e for e in array[1:] if e <= array[0]]) + [array[0]] + quick_sort(
            [e for e in array[1:] if e > array[0]])
