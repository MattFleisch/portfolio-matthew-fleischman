from pymongo import MongoClient
import pymongo


CONNECTION_STRING = "mongodb://localhost:27017"


#Attempt to connect to mongoDb database
try:
    client = MongoClient(CONNECTION_STRING)
except:
  print("Failed to establish connection. Please make sure that mongod.exe is running proir to attempting to connect")

db = client["netflix"]
collection_movies = db["movies"]
collection_shows = db["shows"]


def Query1():
  # Describe query
  print("A query that shows all TV shows made in a specific country (e.g. South Africa) in alphabetical order:\n")
  
  # Setting Query Parameters
  location = {"country": "South Africa"}
  visibleFields = {"title": 1, "_id": 0}

  # Executing the query
  results = collection_shows.find(location, visibleFields).sort("title", pymongo.ASCENDING)

  # Output the results 
  for row in results:
      print(row)
  print("\n")


def Query2():
  
    # Describe query
    print(" Find Indian shows, and update their listed_in field to include ‘Bollywood’ (the first 3 outputs are shown):\n")
    
    # Setting Query Parameters
    location = {"country": "India"}
    genre = {"listed_in": "Bollywood"}
    visibleFields = {"_id": 1, "title": 1,"country": 1 ,"listed_in": 1}
    
    # Executing the query
    collection_shows.update_many(
                    location,
                    {"$addToSet": genre}
                  )
   
    results = collection_shows.find(
                  location,visibleFields
                ).limit(3)
    
    # Output the results 
    for row in results:
        print(row)
    print("\n")


def Query3():
  
  #Describe query
  print(" Querying shows that Justin Roiland, Aaron Paul, Duncan Trussell, Bryan Cranston or Bob Odenkirk are cast members of." 
        "Returning the title, release year and the specific cast member who is featured and sorted by the release year:\n"
        )
  
  # Setting Query Parameters
  cast = {"cast": {"$in": ["Justin Roiland", "Aaron Paul", "Duncan Trussell", "Bryan Cranston", "Bob Odenkirk"]}}
  visibleFields = {"_id": 0, "title":1, "release_year": 1, "cast.$": 1}
  releaseYearSortOrder = {"release_year": 1}
  
  # Executing the query
  results = collection_shows.find(
                              cast
                              ,visibleFields).sort(releaseYearSortOrder)
  # Output the results 
  for row in results:
      print(row)
  print("\n")


def Query4():
  # Describe query
  print("Update all the TV Shows with the word ‘sex’ in their description to a rating of ‘TV-MA’"
        "(which is the correct adult designation) only the title, rating, and description are shown:\n")
 
  # Setting Query Parameters
  description = {"description": {"$regex": 'sex'}}
  rating = {"rating": 'TV-MA'}
 
  # Executing the query
  results = collection_movies.update_many(description, {"$set": rating})

  # Output the results 
  print(results)
  print("\n")


def Query5():
  # Describe query
  print("Find the movie with the longest runtime in minutes for each listed genre.Only the title, genre and runtime is shown.\n")
   
  # Setting Query Parameters
  convertToIntStage = {
    "$addFields":{
        "convertedDuration" : {"$toInt": 
              { "$trim": { "input": "$duration",  "chars": " min"  } }
            }
          }
        }
  groupingParameters ={
                "_id": "$listed_in",
                "runtime": { "$max": "$convertedDuration" },
                "title":{"$first":"$title"},
              } 
  runtimeOrdering = { "runtime": -1 }
  visibleFields = {"_id":1,"title":1,"runtime" : 1}
  convertedDurationOrder = { "convertedDuration": -1 }


  # Executing the query
  results = collection_movies.aggregate([
            {"$unwind": "$listed_in"},
              convertToIntStage,{"$sort":convertedDurationOrder},
            { 
              "$group": groupingParameters
          },{ "$sort": runtimeOrdering},
          {
             "$project": visibleFields
          } 
        ]
      )
  # Output the results 
  for row in results:
      print(row)
  print("\n") 
    
#Calling query functions 
print("Query 1 by Ariel Levy (LVYARI002)")
Query1()
print("Query 2 by Matthew Fleischman (FLSMAT002)")
Query2()
print("Query 3 by Thomas Schroeder (SCHTHO025)")
Query3()
print("Query 4 by Sam Frost (FRSSAM005)")
Query4()
print("Query 5 by Nicola Sartori (SRTNIC002)")
Query5()



client.close()