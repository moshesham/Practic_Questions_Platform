# Data Generator Project

## Overview
This project generates synthetic data for testing SQL queries. The data can be customized using a YAML configuration file and can be saved to a CSV file and an SQLite database.

## Configuration
The `config` folder contains a YAML file (`config.yaml`) that specifies the structure of the data to be generated. The fields, types, and values can be customized.

## Usage
1. Place your configuration file in the `config` folder.
2. Run the `dataGenerator.py` script in the `infra` folder to generate data.
3. The generated data will be saved to `search_data.csv` and `output/search_data.sqlite`.

## Adding Questions
The `questions` folder is for storing SQL questions and their solutions. Each question should have:
1. A `.txt` file with the SQL question.
2. A `.sql` file with the proposed SQL solution.

## Answer Validation
1. The `sql_answer.py` script in the `questions` folder validates the SQL solution by calling the `AnswerValidator` class.
2. Load the SQL file, execute the query, and save the resulting DataFrame as `answer_df.csv` in the `questions/Solutions/Sample_Answer` folder.
3. Compare the `answer_df` with the provided `solution_df.csv`.
4. If they match, print "Congrats! You passed." Otherwise, print "Redo your SQL answer and try again."
