import pandas as pd
import sqlite3
from pathlib import Path


class AnswerValidator:
    def __init__(self, answer_path=None, base_dir=None, question_name=None):
        # Use the calling script's directory as base if not provided
        self.base_dir = base_dir or Path(__file__).resolve().parent.parent

        # Ensure all directory paths are relative to the base directory
        self.output_dir = self.base_dir / 'output'
        self.questions_dir = self.base_dir / 'Questions' / 'Sample_Question'
        self.solutions_dir = self.base_dir / 'Sloutions'

        # Default paths with flexibility
        self.db_path = self.output_dir / 'generated_data.db'

        # If a specific answer path is provided, use it, otherwise look for a default
        if answer_path:
            self.db_filename = Path(answer_path)
        else:
            # Try to find a default solution file
            self.db_filename = next(self.questions_dir.rglob('example_solution.sql'), None)

        if not self.db_filename:
            raise FileNotFoundError("No SQL solution file found")

        print(f"Using solution file: {self.db_filename}")

    def load_sql(self):
        with open(self.db_filename, 'r') as file:
            self.query = file.read()

    def execute_query(self):
        conn = sqlite3.connect(self.db_path)
        self.answer_df = pd.read_sql_query(self.query, conn, index_col=None)
        conn.close()

    def validate_answer(self, solution_file=None):
        # If no solution file provided, try to find a default
        if solution_file is None:
            solution_file = next(self.solutions_dir.rglob('sloution_df.csv'), None)

        if solution_file is None:
            raise FileNotFoundError("No solution DataFrame file found")

        solution_df = pd.read_csv(solution_file, index_col=None)

        # Compare DataFrames
        diff = self.answer_df.compare(solution_df)

        if diff.empty:
            print("Congrats! You passed.")
        else:
            print("Redo your SQL answer and try again.")
            print(diff)


def main():
    # Use current script's directory to determine base directory
    base_dir = Path(__file__).resolve().parent.parent

    # Initialize the AnswerValidator with relative paths
    validator = AnswerValidator(base_dir=base_dir)

    # Load the SQL file
    validator.load_sql()

    # Execute the query and get the result in a DataFrame
    validator.execute_query()

    # Validate the answer
    validator.validate_answer()


if __name__ == "__main__":
    main()