    def save_csv(self):

        now = datetime.now()
        current_time_insert = now.strftime("%H:%M:%S")
        base_path = format(path_config["base_path"])
        filename = format(path_config["filename"])
        filepath = os.path.join(base_path, filename)

        # Function to handle overwrite confirmation
        def show_question():
            message = CTkMessagebox(
                title="Overwrite Warning",
                message=f"Do you want to overwrite Run {self.input_data['Run No.'].get()}?",
                icon="question",
                options=["Cancel", "No", "Yes"]
            )
            response = message.get()
            if response == "Yes":
                print(f"Overwriting save for Run {self.input_data['Run No.'].get()} at {current_time_insert}")
                return True
            else:
                print("Dialog closed or Overwrite declined")
                return False
            

        # Function to check if run number already exists in the CSV
        def check_for_run():
            with open(filepath, "r", newline="") as file:
                reader = csv.reader(file)
                for row in reader:
                    if self.input_data["Run No."].get() == row[0]:
                        return True
                return False

        # Check if run number already exists
        if check_for_run():
            if not show_question():
                return  # Stop save process if user cancels or declines overwrite

        # Proceed with saving to CSV
        with open(filepath, "a", newline="") as file:
            writer = csv.writer(file)
            row_to_write = [var.get() for key, var in self.input_data.items()]
            writer.writerow(row_to_write)

        print(f"CSV save for Run {self.input_data['Run No.'].get()} successful at {current_time_insert}")