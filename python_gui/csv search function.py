import csv
import os

def search_csv(query, filename, base_path):
    filepath = os.path.join(base_path, filename)
    with open(filepath, "r") as c:
        reader = csv.reader(c)
        for row in reader:
            if query in ','.join(row): 
                print("RUN", int(row[0]), ":", "[",', '.join(row),"]")
        else:
            print("No matching run")

search_csv("28", "examplecsv.csv", "C:/Users/jasonbane/Desktop/example_folder")

# def search_csv2(filename, basepath, **kwargs):
#     filepath = os.path.join(basepath, filename)
#     knownqueries = set(["Run No.",
#                  "Configuration No.",
#                  "Date",
#                  "Grid No.",
#                  "Run Type",
#                  "Anode V",
#                  "Cathode V",
#                  "Laser Current",
#                  "Laser Freq.",
#                  "Media",
#                  "Target Channel",
#                  "Target Temp.",
#                  "Target Pressure",
#                  "TC 1",
#                  "TC 2",
#                  "TC 3",
#                  "Window",
#                  "Drift Length",
#                  "Notes"])
#     if 

def test_var_args(f_arg, *argv):
    print("first normal arg:", f_arg)
    for arg in argv:
        print("another arg through *argv:", arg)

test_var_args('yasoob', 'python', 'eggs', 'test')

def args(param, *arguments):
    print("this is a parameter:", param)
    for argument in arguments:
        print("given arguments, through *arguments:", argument)

args("french fry", "broccoli", "canned white potatoes", "greek yogurt")

def searchargs(filename, base_path, *arg):
    filepath = os.path.join(base_path, filename)
    with open(filepath, "r") as c:
        reader = csv.reader(c)
        for row in reader:
            for query in arg:
                    if query in ','.join(row): 
                        print("RESULTS FOUND MATCHING", query, ":", " ", "RUN", int(row[0]), ":", "[",', '.join(row),"]")
                    else:
                        print("No matching run")

    # for argument in arg:
    #     def search_csv(query, filename, base_path):
    #         filepath = os.path.join(base_path, filename)
    #         with open(filepath, "r") as c:
    #             reader = csv.reader(c)
    #             for row in reader:
    #                 if query in ','.join(row): 
    #                     print("RUN", int(row[0]), ":", "[",', '.join(row),"]")
    #             else:
    #                 print("No matching run")
    #     search_csv(argument, "test_csv.csv", "C:/Users/jasonbane/Desktop/example_folder")
    #     #print
# array = ["200", "28", "131", "28", "131", "171", "32"]
# for i in array:
#     searchargs("test_csv.csv", "C:/Users/jasonbane/Desktop/example_folder")
    
searchargs("test_csv.csv", "C:/Users/jasonbane/Desktop/example_folder", "200", "28", "131")