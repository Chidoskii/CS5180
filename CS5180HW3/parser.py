from bs4 import BeautifulSoup
from pymongo import MongoClient


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


def store_faculty_info(col, id, name, title, office, phone, email, website):

    # Value to be inserted
    webpage = {
        "_id": id,
        "name": name,
        "title": title,
        "office": office,
        "phone": phone,
        "email": email,
        "website": website,
    }

    # Insert the document
    col.insert_one(webpage)


def get_html_by_id(col, id):

    html_object = col.find_one({"_id": id})

    if html_object:
        return str(html_object["html"])


db = connect_database()
professors = db["professors"]
pages = db["pages"]

sample = get_html_by_id(pages, 33)
parsed_sample = BeautifulSoup(sample, "html.parser")

professor_details = parsed_sample.find_all("div", {"class": "clearfix"})

name = professor_details[0].h2.get_text("", strip=True)
list_of_professors = []
list_of_details = []

for prof in professor_details:
    if prof.h2 != None:
        prof_name = prof.h2.get_text("", strip=True)
        prof_title = prof.strong.next_sibling.get_text("", strip=True)
        list_of_details.append(prof.p.get_text(", ", strip=True))
        # use .replace(": ", "") to clean up text
        list_of_professors.append(prof_name)

index = 0
document_id = 1
name = ""
title = ""
office = ""
phone = ""
email = ""
website = ""
while len(list_of_professors) == len(list_of_details) and index < len(
    list_of_professors
):
    try:
        name = list_of_professors[index]
        details_array = list_of_details[index].split(", ")
        title = details_array[1]
        office = details_array[3]
        phone = details_array[5]
        email = details_array[7]
        website = details_array[9]
    except IndexError:
        website = ""
    store_faculty_info(
        professors, document_id, name, title, office, phone, email, website
    )
    document_id += 1
    index += 1
