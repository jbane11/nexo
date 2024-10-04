import csv
import os

def search_csv(filename):
    # Function to read CSV file and search for specified strings
    try:
        # Prompt user for comma-separated search strings
        search_input = input("Enter comma-separated strings to search for: ")
        search_strings = [s.strip() for s in search_input.split(',')]

        if not search_strings:
            print("No search strings provided.")
            return

        # Dictionary to store unique rows for each search string
        matches = {search_string: set() for search_string in search_strings}

        # Read the CSV file and search for each string
        with open(filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header if exists

            for row in reader:
                for search_string in search_strings:
                    if any(search_string in field for field in row):
                        matches[search_string].add(tuple(row))

        # Output the matches
        for search_string, rows in matches.items():
            print(f"Matching runs for '{search_string}':")
            if rows:
                for row in rows:
                    print(f"Run {row[0]} = {', '.join(row[1:])}")
            else:
                print(f"No matches found for '{search_string}'.")

    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Example usage:
basepath = "C:/Users/jasonbane/Desktop/example_folder"
file_name = 'test_csv.csv'
filename = os.path.join(basepath, file_name)

search_csv(filename)

import csv
import os
import tkinter as tk
from tkinter import scrolledtext

def search_csv(queries):
    base_path = "C:/Users/jasonbane/Desktop/example_folder"
    filename = "RunList.csv"
    filepath = os.path.join(base_path, filename)

    results = []  # List to store results as text

    try:
        with open(filepath, "r") as file:
            reader = csv.reader(file)
            headers = next(reader)  # Read header row

            for query in queries:
                query = query.strip()  # Remove any leading/trailing whitespace

                found_runs = set()  # Use a set to store unique matching run IDs
                found_rows = []  # List to store unique matching rows for output

                file.seek(0)  # Reset file pointer to beginning for each query

                for row in reader:
                    if any(query.lower() in field.lower() for field in row):
                        run_id = int(row[0])
                        if run_id not in found_runs:
                            found_runs.add(run_id)
                            found_rows.append(f"RUN {run_id}: [{', '.join(row)}]")

                if found_rows:
                    results.append(f"Run(s) matching '{query}':\n")
                    results.extend(found_rows)
                    results.append("\n")
                else:
                    results.append(f"No matching run for '{query}'\n")

        return "\n".join(results)  # Return results as a single string

    except FileNotFoundError:
        return f"File '{filename}' not found."
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Example tkinter GUI
def display_results():
    queries = entry.get().split(',')  # Get queries from entry widget
    results_text = search_csv(queries)
    textbox.delete('1.0', tk.END)  # Clear previous content
    textbox.insert(tk.END, results_text)  # Insert new results

root = tk.Tk()
root.title("CSV Search Tool")

label = tk.Label(root, text="Enter comma-separated queries:")
label.pack()

entry = tk.Entry(root, width=50)
entry.pack()

button = tk.Button(root, text="Search", command=display_results)
button.pack()

textbox = scrolledtext.ScrolledText(root, width=100, height=20)
textbox.pack()

root.mainloop()

