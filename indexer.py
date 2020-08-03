
import mysql.connector

def add_to_index(index, term):
    if index.lower() == "species":
        file = open("./Indexes/species.lst", "a+")
    elif index == "gene":
        file = open("./Indexes/genes.lst", "a+")
    else:
        return "Failed to index"

    file.write(term + "\n")
    file.close()



def quicksort(R):
    if len(R) < 2:
        return R

    pivot = R[0]
    low = quicksort([i for i in R if i < pivot])
    high = quicksort([i for i in R if i > pivot])
    return low + [pivot] + high


def refresh(index):
    if index.lower() == "species":
        file = open("./Indexes/species.lst", "r+")
    elif index == "gene":
        file = open("./Indexes/genes.lst", "r+")
    else:
        return "Failed to index"

    



    R_to_sort = []
    for line in file.readlines():
        R_to_sort.append(line)






def main():
    test_index = "Species"
    test_term = "Hi. I'm phil"

    test_array = [3,4,5,1,7,2,8,20]
    test_array_long = ["Bob", "chad", "Kyle", "Tom", "Fred", "d qs", "dqwd ", "!", "d w ", "gr we"," feqw", " few"]

    print("Hello")
    add_to_index(test_index, test_term)

    refresh(test_index)

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
