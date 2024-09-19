# -------------------------------------------------------------------------
# AUTHOR: Chidi Okpara
# FILENAME: indexing.py
# SPECIFICATION: This program will generate a document term matrix
# FOR: CS 5180- Assignment #1
# TIME SPENT: 5 hrs
# -----------------------------------------------------------*/

# Importing some Python libraries
import csv
import math

documents = []

# Reading the data in a csv file
with open("collection.csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    for i, row in enumerate(reader):
        if i > 0:  # skipping the header
            documents.append(row[0])

# Conducting stopword removal for pronouns/conjunctions. Hint: use a set to define your stopwords.
# --> add your Python code here
stopWords = ["I", "and", "She", "her", "They", "their"]
i = 0
j = 0
while i < len(documents):
    for x in stopWords:
        documents[i] = documents[i].replace(stopWords[j], "")
        j += 1
    j = 0
    i += 1


# Conducting stemming. Hint: use a dictionary to map word variations to their stem.
# --> add your Python code here
steeming = {"cat": "cats", "love": "loves", "dog": "dogs"}
keyList = list(steeming.keys())
newDocuments = []
j = 0
while j < len(documents):
    splitWords = documents[j].split()
    i = 0
    while i < len(splitWords):
        for x in steeming:
            if steeming[x] == splitWords[i]:
                splitWords[i] = x
        i += 1
    splitWords = " ".join(splitWords)
    newDocuments.append(splitWords)
    j += 1


# Identifying the index terms.
# --> add your Python code here
terms = []
i = 0
while i < len(newDocuments):
    keyTerms = newDocuments[i].split()
    for element in keyTerms:
        if element not in terms:
            terms.append(element)
    i += 1


# Building the document-term matrix by using the tf-idf weights.
# --> add your Python code here
def get_document_frequency(term, document_set):
    count = 0
    term_documents = 0
    for x in document_set:
        temp = x.split()
        for i in temp:
            if i == term:
                count += 1
        if count > 0:
            term_documents += 1
        count = 0
    return term_documents


def get_term_frequency(term, document_set, number):
    count = 0
    term_freq = 0
    temp = document_set[number].split()
    for i in temp:
        if i == term:
            count += 1
    term_freq = count / len(temp)
    return term_freq


def inverse_document_frequency(term, document_set):
    idf = math.log10(len(document_set) / get_document_frequency(term, document_set))
    return idf


def generate_document_matrix(terms, document_set):
    i = 0
    j = 0
    doc_matrix = []
    temp = []
    while i < len(document_set):
        while j < len(terms):
            temp.append(
                round(
                    (
                        get_term_frequency(terms[j], document_set, i)
                        * inverse_document_frequency(terms[j], document_set)
                    ),
                    2,
                )
            )
            j += 1
        j = 0
        doc_matrix.append(temp)
        temp = []
        i += 1
    return doc_matrix


docTermMatrix = generate_document_matrix(terms, newDocuments)

# Printing the document-term matrix.
# --> add your Python code here
print("-----------Document Term Matrix-----------")
for row in docTermMatrix:
    print(row)
