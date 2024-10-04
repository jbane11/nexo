import csv
import os

def search_csv(filename):
    search_input = input("Enter queries (comma-separated): ")
    queries = [s.strip() for s in search_input.split(',')]
    
    #dictionary stores matches for each query
    matches = {query: set() for query in queries}
    
    with open(filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        lines = list(reader)
        
        for i, line in enumerate(lines):
            for query in queries:
                if any(query in field for field in line):
                    matches[query].add(tuple(line))
        
        for query, rows in matches.items():
            if rows:
                print(f"Matching runs for '{query}':")
                for row in rows:
                    print(f"Run {row[0]} = {', '.join(row[1:])}")
            else:
                print(f"No matches found for '{query}'.")

#like other search fct: i use join bc i have problems accessing the file directly from vscode. feel free to skip if unnecessary
basepath = "C:/Users/jasonbane/Desktop/example_folder"
file_name = 'test_csv.csv'
filename = os.path.join(basepath, file_name)

search_csv(filename)


search_csv(filename)
