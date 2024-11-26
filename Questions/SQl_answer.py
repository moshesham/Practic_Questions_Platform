import sys
import os
from pathlib import Path

# Add the infra folder to the Python path

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname('Sample_Questions'))))
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname('Questions'))))
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'infra')))
#
SCRIPT_DIR = Path().parent
QUESTIONS_DIR = SCRIPT_DIR / 'Questions' / 'Sample_Question'/ 'example_solution.sql'
SLOUTIONS_DIR = SCRIPT_DIR / 'Sloutions' / 'Sample_Answer'/ 'example_solution.sql'
# OUTPUT_DIR = SCRIPT_DIR / 'output'

from infra.AnswerValidator import AnswerValidator

def main():
    # Initialize the AnswerValidator
    validator = AnswerValidator(answer_path=QUESTIONS_DIR)

    # Load the SQL file from the questions folder

    validator.load_sql()

    # Execute the query and get the result in a DataFrame
    validator.execute_query()

    validator.validate_answer(r'C:\Users\Moshe\PycharmProjects\Practic_Questions_Platform\Sloutions\Sample_Answer\sloution_df.csv')

if __name__ == "__main__":
    main()
