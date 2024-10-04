import csv
import os

def search_csv(filename, query):
    match_indices = []
    with open(filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        lines = list(reader)
        
        for i, line in enumerate(lines):
            if any(query in field for field in line):
                match_indices.append(i)
        
        if match_indices:
            print(f"Matches for", query, "found in Runs:")
            for index in match_indices:
                print(f"Run {lines[index][0]} = {', '.join(lines[index])}")
        else:
            print("No matches found.")

# sometimes the code has trouble reading files from my computer bc they are stored under a different user. if you are directly accessing then feel free to remove basepath & file_name
basepath = "example/users/documents"
file_name = 'example.csv'
filename = os.path.join(basepath, file_name)
query = '28'

search_csv(filename, query)
