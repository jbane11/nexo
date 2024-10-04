import csv
import os
import customtkinter as ctk  # Assuming CustomTKinter is imported as ctk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")
class CustomTkinterFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        # Label and Entry for queries
        self.query_label = ctk.CTkLabel(self, text="Enter comma-separated queries:")
        self.query_label.pack(pady=5)
        self.entry = ctk.CTkEntry(self, width=150)
        self.entry.pack(pady=5)

        # Search Button
        self.search_button = ctk.CTkButton(self, text="Search", command=self.search_and_display)
        self.search_button.pack(pady=10)

        # Result Textbox
        self.result_label = ctk.CTkLabel(self, text="Search Results:")
        self.result_label.pack(pady=5)
        self.result_textbox = ctk.CTkTextbox(self, state="normal", height=600, width=800)
        self.result_textbox.pack(padx=10, pady=10)

    def search_and_display(self):
        base_path = "C:/Users/jasonbane/Desktop/example_folder"
        filename = "RunList.csv"
        queries = self.get_queries()

        results_text = self.search_csv(base_path, filename, queries)
        self.result_textbox.delete('1.0', 'end')
        self.result_textbox.insert('end', results_text)

    def get_queries(self):
        entry_text = self.entry.get()
        queries = entry_text.split(',')
        return [query.strip() for query in queries]

    def search_csv(self, base_path, filename, queries):
        filepath = os.path.join(base_path, filename)
        results = []

        try:
            with open(filepath, "r") as file:
                reader = csv.reader(file)
                headers = next(reader)  # Read header row

                for query in queries:
                    query = query.strip()

                    found_runs = set()
                    found_rows = []

                    file.seek(0)

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

            return "\n".join(results)

        except FileNotFoundError:
            return f"File '{filename}' not found."
        except Exception as e:
            return f"An error occurred: {str(e)}"

# Example usage outside the customtkinter frame
def main():
    root = ctk.CTk()
    root.title("CSV Search Tool")

    custom_frame = CustomTkinterFrame(root)
    custom_frame.pack(padx=20, pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
