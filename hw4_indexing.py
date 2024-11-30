from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import (
    CountVectorizer,
    TfidfTransformer,
    TfidfVectorizer,
)
from pymongo import MongoClient
import pandas as pd
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


def create_term(col, id, term, pos, docs):

    # Value to be inserted
    term = {"_id": id, "term": term, "pos": pos, "docs": docs}

    # Insert the document
    col.insert_one(term)


def create_document(col, id, content):
    # Value to be inserted
    doc = {
        "_id": id,
        "content": content,
    }
    # Insert the document
    col.insert_one(doc)


def get_pos(col, term):
    pos = col.find_one({"term": term}, {"_id": 0, "term": 0})
    return pos["pos"]


def check_document_for_term(term, doc):
    doc = doc.lower()
    if term in doc:
        return True


def get_tfidf_value(pos, matrix, doc_id):
    return matrix[doc_id, pos]


def update_reference_document_object(col, termid, doc_id, tdidf):
    reference = {doc_id: tdidf}
    expression = {"$push": {"docs": reference}}

    col.update_one({"_id": termid}, expression)


db = connect_database()
terms = db["terms"]


# Document set
doc1 = "After the medication, headache and nausea were reported by the patient."
doc2 = "The patient reported nausea and dizziness caused by the medication."
doc3 = "Headache and dizziness are common effects of this medication."
doc4 = "The medication caused a headache and nausea, but no dizziness was reported."

test = ["After the medication, headache and nausea were reported by the patient."]

# Add documents to a list
document_collection = []
document_collection.append(
    doc1.lower().translate(str.maketrans("", "", string.punctuation))
)
document_collection.append(
    doc2.lower().translate(str.maketrans("", "", string.punctuation))
)
document_collection.append(
    doc3.lower().translate(str.maketrans("", "", string.punctuation))
)
document_collection.append(
    doc4.lower().translate(str.maketrans("", "", string.punctuation))
)

vectorizer = CountVectorizer(analyzer="word", ngram_range=(1, 3))
vectorizer.fit(document_collection)
vector = vectorizer.transform(document_collection)
term_dict = vectorizer.vocabulary_
length_of_vector = len(term_dict)
index = 0
for key in term_dict:
    id = index
    term = key
    pos = term_dict[key]
    docs = []
    create_term(terms, id, term, pos, docs)
    index += 1

# retrieve the terms found in the corpora
count_tokens = vectorizer.get_feature_names_out()

tfidf_vector = TfidfTransformer()
tfidf_vector.fit(vector)
tfidf_matrix = tfidf_vector.transform(vector)

print(length_of_vector)

index = 0
for doc in document_collection:
    step = 0
    for key in term_dict:
        if check_document_for_term(key, doc):
            position = get_pos(terms, key)
            current_tfidf = get_tfidf_value(position, tfidf_matrix, index)
            update_reference_document_object(
                terms, str(step), str(index), current_tfidf
            )
        step += 1
    index += 1
