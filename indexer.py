
# Adds a term to index. Either to genes.lst or species.lst
def add_to_index(index, term):
    file = open_spec(index, "a+")

    if not check_index(index, term):
        file.write(term + "\n")
    file.close()


# Deletes a term from the index. Either to genes.lst or species.lst
def delete_from_index(index, term):
    # Stores all of the data in "lines"
    file = open_spec(index, "r+")
    lines = file.readlines()
    file.close()

    # Opens the list to write to it
    file = open_spec(index, "w")

    # writes every line EXCEPT the one that needs to be deleted
    for line in lines:
        if term not in line:
            file.write(line)

    file.close()



# Function that cycles through the .lst to see if the term is there
# Helper just for saving time
def check_index(index, term):

    file = open_spec(index, "r")

    for line in file.readlines():
        if term in line:
            file.close()
            return True
    file.close()
    return False



# Does normalization on lists
# Sorts alphabetically,
# TODO - set up refreshing of downloaded files
def refresh(index):

    # Common recursive sort algortihm for sorting through each index
    def quicksort(R):
        if len(R) < 2:
            return R

        pivot = R[0]
        low = quicksort([i for i in R if i < pivot])
        high = quicksort([i for i in R if i > pivot])
        return low + [pivot] + high


    file = open_spec(index, "r+")

    lines = quicksort(file.readlines())
    file.close()

    file = open_spec(index, "w")

    for line in lines:
        file.write(line)
    file.close()


# A helper method for simplifying all of the other methods
def open_spec(index, method):
    if index.lower() == "species":
        return open("./Indexes/species.lst", method)
    elif index.lower() == "gene":
        return open("./Indexes/gene.lst", method)
    else:
        return ""




def main():
    test_index = "atp"
    test_term = "C"

    test_array = [3,4,5,1,7,2,8,20]
    test_array_long = ["Bob", "chad", "Kyle", "Tom", "Fred", "d qs", "dqwd ", "!", "d w ", "gr we"," feqw", " few"]

    print("Hello")
    add_to_index(test_index, test_term)
    # delete_from_index(test_index, test_term)

    # refresh(test_index)









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
