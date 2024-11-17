from urllib.request import urlopen
from bs4 import BeautifulSoup
from pymongo import MongoClient
from urllib.error import HTTPError
from urllib.error import URLError


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


def store_webpage(col, id, url, html, target):

    # Value to be inserted
    webpage = {
        "_id": id,
        "url": url,
        "html": html,
        "target": target,
    }

    # Insert the document
    col.insert_one(webpage)


def get_resource(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        print(e)
    except URLError as e:
        print("The server could not be found!")
    else:
        return html


def filter_links(soup):
    for link in soup.find_all("a", href=True):
        href = link["href"]

        # Check for empty or invalid links
        if not href or href.startswith("#") or href.startswith("javascript:"):
            link.decompose()  # Remove the link from the soup

        # Check for relative links that may not be accessible
        # elif not href.startswith("https") or not href.startswith(
        #     "https://www.cpp.edu/sci/"
        # ):
        #     link.decompose()

        elif not href.endswith("html") or not href.endswith("shtml"):
            link.decompose()

    return soup


def get_links(parsed_html, links_array):
    links = parsed_html.find_all("a")
    for link in links:
        href = link.get("href")
        if href and not href.startswith("https://www.cpp.edu"):
            href = "https://www.cpp.edu" + href
        if href not in links_array:
            links_array.append(href)


def target_page(parsed_html, target_tag):
    target = False
    actual_tag = str(parsed_html.find("h1", {"class": "cpp-h1"}))
    if actual_tag == target_tag:
        target = True
    return target


def flag_target_page(col, id, target):
    # Value to be updated
    webpage = {"$set": {"target": target}}

    # Insert the document
    col.update_one({"_id": id}, webpage)


def crawler_thread(frontier, target_tag):
    target = False
    document_id = 1
    index = 0
    while index < len(frontier):
        url = frontier[index]
        html = get_resource(url)
        bs = BeautifulSoup(html.read(), "html.parser")
        bs_text = str(bs.prettify())
        store_webpage(pages, document_id, url, bs_text, target)
        if target_page(bs, target_tag):
            flag_target_page(pages, document_id, True)
            frontier.clear()
        else:
            bs = filter_links(bs)
            get_links(bs, frontier)
        document_id += 1
        index += 1


frontier = []
url = "https://www.cpp.edu/sci/computer-science/"
tester = (
    "https://www.cpp.edu/sci/computer-science/faculty-and-staff/permanent-faculty.shtml"
)
frontier.append(url)
target_tag = '<h1 class="cpp-h1">Permanent Faculty</h1>'

db = connect_database()
pages = db["pages"]

crawler_thread(frontier, target_tag)
