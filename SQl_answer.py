from pathlib import Path
from infra.AnswerValidator import AnswerValidator

def main():
    # Use current script's directory to determine base directory
    base_dir = Path(__file__).resolve().parent.parent

    # Initialize the AnswerValidator
    validator = AnswerValidator(base_dir=base_dir)

    # Load the SQL file
    validator.load_sql()

    # Execute the query and get the result in a DataFrame
    validator.execute_query()

    # Validate the answer
    validator.validate_answer()

if __name__ == "__main__":
    main()