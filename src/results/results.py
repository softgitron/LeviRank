from results.result import Result


class Results:
    entries: list[Result] = []
    method: str

    def append(self, result: Result):
        self.entries.append(result)

    def __iter__(self):
        return iter(self.entries)

    def write_results_csv(self, csv_path: str):
        # Initialize string that will be written to the file
        results_string = ""
        for result in self.entries:
            # Write results to the string
            results_string += f"{result.topic_number} {result.stance} {result.document_id} {result.rank} {result.score} {self.method}\n"

        # Remove final line ending
        results_string = results_string[:-1]

        # Open results file for writing
        try:
            results_file = open(csv_path, "w")
        except OSError as error:
            print(error)
            print("Couldn't open results file for writing, is the file path correct?")
            exit(1)

        # Write results
        results_file.write(results_string)
        results_file.close()

        print(f'Results saved to the "{csv_path}"')

    def load_results_csv(self, csv_path: str):
        # Open results file for reading
        try:
            results_file = open(csv_path, "r")
        except OSError as error:
            print(error)
            print("Couldn't open results file for reading, is the file path correct?")
            exit(1)

        # Empty current results
        self.entries = []

        for line in results_file:
            # Split lines to tokens
            tokens = line[:-1].split(" ")
            topic_number = int(tokens[0])
            stance = tokens[1]
            document_id = tokens[2]
            rank = int(tokens[3])
            score = float(tokens[4])

            result = Result(topic_number, stance, document_id, rank, score)
            self.entries.append(result)

        # Read method from the last line
        self.method = tokens[5]

        results_file.close()

    def group_by_topic_number(self) -> dict[list[Result]]:
        by_id = {}

        for result in self.entries:
            if not by_id.get(result.topic_number):
                by_id[result.topic_number] = []
            by_id[result.topic_number].append(result)

        return by_id

    def remove_section_identifiers(self):
        for result in self.entries:
            fixed_document_id = result.document_id
            fixed_document_id = fixed_document_id.split("_")[0]
            result.document_id = fixed_document_id
