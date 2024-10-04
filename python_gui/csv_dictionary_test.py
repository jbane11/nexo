import csv
import os

# Example dictionary
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'Los Angeles', 'Chicago']
}

def save_csv():
    # Specify the filename
    csv_filename = 'data.csv'
    base_path = "C:/Users/jasonbane/Desktop/example_folder"
    file_path = os.path.join(base_path, csv_filename)

    # Open the CSV file in write mode with newline='' to prevent extra newline characters
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write header row based on keys of the dictionary
        writer.writerow(data.keys())

        # Zip the values together and write each row
        for row in zip(*data.values()):
            writer.writerow(row)

    print(f"Data has been successfully saved to {csv_filename}")