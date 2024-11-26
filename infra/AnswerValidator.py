import pandas as pd
import sqlite3
import os, sys
from pathlib import Path

from numpy.array_api import astype

SCRIPT_DIR = Path(__file__).parent
QUESTIONS_DIR = SCRIPT_DIR / 'Questions'
SLOUTIONS_DIR = SCRIPT_DIR / 'Sloutions'
OUTPUT_DIR = SCRIPT_DIR / 'output'
DBOUTPUT_DIR = SCRIPT_DIR / 'output' / 'generated_data.db'

class AnswerValidator:
    def __init__(self, answer_path):
        self.db_filename = r'C:\Users\Moshe\PycharmProjects\Practic_Questions_Platform\Questions\Sample_Question\example_solution.sql'
        self.db_path = DBOUTPUT_DIR
        print(self.db_filename)

    def load_sql(self):
        with open(self.db_filename, 'r') as file:
            self.query = file.read()


    def execute_query(self):
        conn = sqlite3.connect(self.db_path)
        self.answer_df = pd.read_sql_query(self.query, conn,index_col=None)
        conn.close()

    def validate_answer(self, solution_file):
        solution_df = pd.read_csv(solution_file,index_col=None)

        # if self.answer_df.equals(solution_df):
        diff=self.answer_df.compare(solution_df)

        if diff.empty:
            print("Congrats! You passed.")
        else:
            print("Redo your SQL answer and try again.")
            print(diff)


