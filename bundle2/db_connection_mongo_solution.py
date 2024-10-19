from pymongo import MongoClient
import datetime
import string


def connect_database():

    # Creating a database connection object using pymongo

    DB_NAME = "CPP"
    DB_HOST = "localhost"
    DB_PORT = 27017

    try:

        client = MongoClient(host=DB_HOST, port=DB_PORT)
        db = client[DB_NAME]

        return db

    except:
        print("Database not connected successfully")


def tokenize(text):
    swap_table = str.maketrans("", "", string.punctuation)
    tokens = text.translate(swap_table)
    tokens = tokens.lower()
    tokens = tokens.split()
    return tokens


def count_characters(word):
    count = len(word)
    return count


def term_frequency(word, list):
    count = 0
    for item in list:
        if word == item:
            count += 1
    return count


def create_terms(arr):
    terms = []
    checklist = []
    term = ""
    term_count = 0
    num_chars = 0
    for item in arr:
        if item not in checklist:
            checklist.append(item)
            term = item
            term_count = term_frequency(term, arr)
            num_chars = count_characters(term)
            term_object = {"term": term, "count": term_count, "num_chars": num_chars}
            terms.append(term_object)
    return terms


def create_document(col, docId, docText, docTitle, docDate, docCat):

    docId = int(docId)
    term_list = tokenize(docText)
    terms = create_terms(term_list)

    # Value to be inserted
    document = {
        "_id": docId,
        "text": docText,
        "title": docTitle,
        "date": datetime.datetime.strptime(docDate, "%m/%d/%Y %H:%M:%S"),
        "category": docCat,
        "terms": terms,
    }

    # Insert the document
    col.insert_one(document)


def update_document(col, docId, docText, docTitle, docDate, docCat):

    docId = int(docId)

    # Document fields to be updated
    document = {
        "$set": {
            "_id": docId,
            "text": docText,
            "title": docTitle,
            "date": docDate,
            "category": docCat,
        }
    }

    # Updating the document
    col.update_one({"_id": docId}, document)


def delete_document(col, docId):

    docId = int(docId)

    # Delete the document from the database
    col.delete_one({"_id": docId})


def get_index(col):

    pipeline = [
        {"$unwind": {"path": "$terms"}},
        {"$project": {"_id": 0, "terms.term": 1, "terms.count": 1, "title": 1}},
        {"$sort": {"terms.term": 1}},
    ]
    document_index = col.aggregate(pipeline)

    if document_index:
        result = set()
        entry = ""
        for doc in document_index:
            entry += (
                "'"
                + doc["terms"]["term"]
                + "': '"
                + doc["title"]
                + ":"
                + str(doc["terms"]["count"])
                + "',"
            )
        result.add(entry)
        return result
    else:
        return []
