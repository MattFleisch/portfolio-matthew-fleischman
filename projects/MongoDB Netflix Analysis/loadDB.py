from pymongo import MongoClient
import csv
from datetime import datetime
import re

CONNECTION_STRING = ""
client = MongoClient(CONNECTION_STRING)

# inserting into db

csv_file_path = "Assignment1/netflix.csv"
db = client["netflix"]

# creating two distinct collections
collection_movies = db["movies"]
collection_shows = db["shows"]

with open(csv_file_path,"r", encoding = "utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    m = 1
    s = 1
    for row in reader:
        # Convert comma-separated strings to lists
        row["cast"] = row["cast"].split(', ') if row["cast"] else None
        row["listed_in"] = row["listed_in"].split(', ') if row["listed_in"] else None
        row["country"] = row["country"].split(', ') if row["country"] else None
        row["director"] = row["director"].split(', ') if row["director"] else None

        # Convert date_added to ISO format
        if row["date_added"]:
            try:
                row["date_added"] = datetime.strptime(row["date_added"], "%B %d, %Y").date().isoformat()
            except ValueError:
                row["date_added"] = None
        else:
            row["date_added"] = None

        # Remove empty fields (None values) from the dictionary
        row = {key: value for key, value in row.items() if value}

        # split data based on movie or tv show
        if row["type"] == "Movie":
            del row["type"]
            row["_id"] = f"mov{m}"
            collection_movies.insert_one(row)
            m += 1
        else:
            # "type" is TV Show
            del row["type"]
            row["_id"] = f"tv{s}"
            collection_shows.insert_one(row)
            s += 1

print("Data import successful")

client.close()