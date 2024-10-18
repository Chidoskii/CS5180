# -------------------------------------------------------------------------
# AUTHOR: Chidi Okpara
# FILENAME: index_mongo.py
# SPECIFICATION: CRUD operations using python and MongoDB
# FOR: CS 5180- Assignment #2
# TIME SPENT: 5hrs
# -----------------------------------------------------------*/

from pymongo import MongoClient  # import mongo client to connect
from db_connection_mongo_solution import *

if __name__ == "__main__":

    # Connecting to the database
    db = connect_database()

    # Creating a collection
    documents = db["documents"]

    # print a menu
    print("")
    print("######### Menu ##############")
    print("#a - Create a document")
    print("#b - Update a document")
    print("#c - Delete a document.")
    print("#d - Output the inverted index ordered by term.")
    print("#q - Quit")

    option = ""
    while option != "q":

        print("")
        option = input("Enter a menu choice: ")

        if option == "a":

            docId = input("Enter the ID of the document: ")
            docText = input("Enter the text of the document: ")
            docTitle = input("Enter the title of the document: ")
            docDate = input("Enter the date of the document: ")
            docCat = input("Enter the category of the document: ")

            create_document(documents, docId, docText, docTitle, docDate, docCat)

        elif option == "b":

            docId = input("Enter the ID of the document: ")
            docText = input("Enter the text of the document: ")
            docTitle = input("Enter the title of the document: ")
            docDate = input("Enter the date of the document: ")
            docCat = input("Enter the category of the document: ")

            update_document(documents, docId, docText, docTitle, docDate, docCat)

        elif option == "c":

            docId = input("Enter the document ID to be deleted: ")

            delete_document(documents, docId)

        elif option == "d":

            index = get_index(documents)
            for doc in index:
                print(doc)

        elif option == "q":

            print("Leaving the application ... ")

        else:

            print("Invalid Choice.")
