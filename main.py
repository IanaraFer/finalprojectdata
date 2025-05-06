# This script connects to a MySQL database and a Neo4j database, allowing users to view and manipulate data related to actors, directors, films, and studios.

import os
import json
import mysql.connector

# Filepath to the JSON file
file_path = r"c:\Users\35387\Downloads\FinalProject\FinalProject\finalprojectdata\actorsMarried.json"

# Check if the file exists and is not empty
if not os.path.exists(file_path):
    print(f"Error: File not found at {file_path}")
elif os.path.getsize(file_path) == 0:
    print(f"Error: File is empty at {file_path}")
else:
    # Open and read the file as plain text
    with open(file_path, 'r') as file:
        content = file.read()

    # Print the content
    print("File content:")
    print(content)

relations = [
    {"ActorID": 1, "Relation": "MARRIED_TO", "PartnerID": 81},
    {"ActorID": 9, "Relation": "DIVORCED_FROM", "PartnerID": 81}
]
print(relations)

import numpy
import pandas as pd
from neo4j import GraphDatabase  # Import Neo4j driver

try:
    # Connect to MySQL
    mysql_conn = mysql.connector.connect(
        host="localhost",  # Replace with your MySQL server host
        user="root",       # Replace with your MySQL username
        password="your_password",  # Replace with your MySQL password
        database="your_database"   # Replace with your MySQL database name
    )
    print("MySQL connection established successfully!")

    # Create a cursor object
    mysql_cursor = mysql_conn.cursor()

    # Test query
    mysql_cursor.execute("SHOW DATABASES")
    print("Databases:")
    for db in mysql_cursor.fetchall():
        print(db)

except mysql.connector.Error as err:
    print(f"Error: {err}")

def main_menu():
    while True:
        print("\nMoviesDB Menu")
        print("1. View Directors & Films")
        print("2. View Actors by Months of Birth")
        print("3. Add New Actor")
        print("4. View Married Actors")
        print("5. Add Marriage Actor")
        print("6. View Studios")
        print("7. Search Director by Name")
        print("X. Exit Application")
        
        choice = input("Choice: ").strip().lower()
        
        if choice == "1":
            view_directors_and_films()
        elif choice == "2":
            view_actors_by_month()  # Updated to call the correct function
        elif choice == "3":
            add_new_actor()
        elif choice == "4":
            view_married_actors()
        elif choice == "5":
            add_marriage_actor()
        elif choice == "6":
            view_studios()
        elif choice == "7":
            search_director_by_name()
        elif choice == "x":
            print("Exiting application...")
            break
        else:
            print("Invalid choice, try again.")

# \f1 1\uc0\u65039 \u8419 \f0  View Directors & Films (MySQL)\
def view_directors_and_films():
    mysql_cursor.execute("SELECT directors.name, films.title FROM directors JOIN films ON directors.id = films.director_id")
    for row in mysql_cursor.fetchall():
        print(row)
 
# \f1 2\uc0\u65039 \u8419 \f0  View Actors by Month of Birth (MySQL)\
def view_actors_by_birth_month():
    month = input("Enter birth month (1-12): ")
    mysql_cursor.execute("SELECT name FROM actors WHERE MONTH(birth_date) = %s", (month,))
    for row in mysql_cursor.fetchall():
        print(row)

# \f1 3\uc0\u65039 \u8419 \f0  Add New Actor (MySQL)\
def add_new_actor():
    name = input("Enter actor name: ")
    birth_date = input("Enter birth date (YYYY-MM-DD): ")
    nationality = input("Enter nationality: ")
    mysql_cursor.execute("INSERT INTO actors (name, birth_date, nationality) VALUES (%s, %s, %s)", (name, birth_date, nationality))
    mysql_conn.commit()
    print("Actor added successfully!")

# \f1 4\uc0\u65039 \u8419 \f0  View Married Actors (Neo4j)
def view_married_actors():
     with neo4j_driver.session() as session:
         result = session.run("MATCH (a:Actor) WHERE a.married = true RETURN a.name")
         for record in result:
             print(record["a.name"])

# \f1 5\uc0\u65039 \u8419 \f0  Add Marriage Actor (Neo4j)
def add_marriage_actor():
     actor_name = input("Enter actor name: ")
     with neo4j_driver.session() as session:
         session.run("MATCH (a:Actor {name: $name}) SET a.married = true", name=actor_name)
         print("Marriage status updated!")
\
# \f1 6\uc0\u65039 \u8419 \f0  View Studios (MySQL)
def view_studios():
     mysql_cursor.execute("SELECT name FROM Studios")
     for row in mysql_cursor.fetchall():
         print(row)
# Initialize Neo4j driver
neo4j_driver = GraphDatabase.driver(
    uri="bolt://localhost:7687",  # Replace with your Neo4j URI
    auth=("neo4j", "your_password")  # Replace with your Neo4j username and password
)

# Close Neo4j driver after the program ends
neo4j_driver.close()

# Getting the Director name.
def get_director_name():
    mysql_cursor.execute("SELECT name FROM directors WHERE name LIKE '%Dav%'")
    for row in mysql_cursor.fetchall():
        print(row)

# Call the function to get the director name
get_director_name()

def search_director_by_name():
    # Prompt the user for the director's name or part of the name
    director_name = input("Enter Director name: ").strip()
    
    # SQL query to fetch the director's name, films, and studio
    query = """
        SELECT directors.name AS director_name, films.title AS film_title, studios.name AS studio_name
        FROM directors
        JOIN films ON directors.id = films.director_id
        JOIN studios ON films.studio_id = studios.id
        WHERE directors.name LIKE %s
    """
    
    # Print the query and input for debugging
    print(f"Executing query: {query} with value: {director_name}%")
    
    # Execute the query with the user input
    mysql_cursor.execute(query, (f"{director_name}%",))  # Match names starting with the input
    results = mysql_cursor.fetchall()
    
    # Check if results are found
    if results:
        print("\nDirectors, Films, and Studios found:")
        for row in results:
            print(f"Director: {row[0]}, Film: {row[1]}, Studio: {row[2]}")
    else:
        print("No directors found with that name.")

# Test the function directly
search_director_by_name()

# ou.py

# Sample data for actors
actors = [
    {"name": "Actor One", "birth_date": "1985-01-15", "gender": "Male"},
    {"name": "Actor Two", "birth_date": "1990-02-20", "gender": "Female"},
    {"name": "Actor Three", "birth_date": "1988-01-30", "gender": "Male"},
    {"name": "Actor Four", "birth_date": "1995-03-10", "gender": "Female"},
]

def view_actors_by_month():
    # Map of month abbreviations to their numeric values
    month_map = {
        "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
        "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12
    }
    
    # Prompt user to enter a month
    month_input = input("Enter a month (1-12 or Jan-Dec): ").strip().lower()
    
    # Validate the input
    if month_input.isdigit():
        month = int(month_input)
        if not (1 <= month <= 12):
            print("Invalid month. Please enter a number between 1 and 12.")
            return
    elif month_input in month_map:
        month = month_map[month_input]
    else:
        print("Invalid month. Please enter a number (1-12) or the first 3 letters of a month (e.g., Jan, Feb).")
        return
    
    print(f"\nActors born in month {month}:\n")
    
    # Filter and display actors born in the given month
    found = False
    for actor in actors:
        birth_month = int(actor["birth_date"].split("-")[1])
        if birth_month == month:
            found = True
            print(f"Name: {actor['name']}")
            print(f"Birth Date: {actor['birth_date']}")
            print(f"Gender: {actor['gender']}\n")
    
    if not found:
        print("No actors found for the given month.")

if __name__ == "__main__":
    main_menu()

# Run the Menu
main_menu()

# Close Neo4j driver after the program ends
neo4j_driver.close()

