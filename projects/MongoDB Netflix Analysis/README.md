# Netflix Database Management & Analysis

This project demonstrates how to manage, preprocess, and query Netflix Movies & TV Shows data using MongoDB and PyMongo in Python.

## Project Structure

* ```netflix.csv``` – Original dataset containing 8,807 Netflix titles with metadata (title, cast, director, release year, genres, etc.).
* ```loadDB.py``` – Python script to preprocess and load the dataset into MongoDB.
  * Splits into two collections: Movies and TV Shows
  * Converts date fields to ISO format
  * Splits comma-separated fields (e.g., cast, genres, country) into lists
* ```QueryProgram.py``` – Python script to execute and display 5 sample queries on the MongoDB collections.
* ```Netflix Database Management & Analysis.pdf``` – Report explaining design decisions, database choices, and detailed query results.

## Setup Instructions

1. Requirements
   * Python 3.x
   * MongoDB (local or Atlas)
   * Packages: 
     ```bash
     pip install pymongo
     ```

2. Load Data into MongoDB
   * Start MongoDB locally or connect via Atlas.
   * Update the CONNECTION_STRING in ```loadDB.py```.
   * Run: 
     ```bash
     python loadDB.py
     ```
    * Collections created:
      * ```netflix.movies```
      * ```netflix.shows```

3. Run Queries

    To test and analyze:
    ```bash
    python QueryProgram.py
    ```
   This will print query results such as:

   * All TV shows from a given country (alphabetical)
   * Movies with "adventure" in the title/description
   * Updating Bollywood tags for Indian shows
   * Longest runtime per genre
   * Updating ratings for adult-themed content

## Contributors

* Matthew Fleischman
* Sam Frost
* Ariel Levy
* Nicola Sartori
* Thomas Schroeder