# Practic_Questions_Platform

## Overview
A platform for practicing SQL queries with automated validation and user progress tracking.

## Setup
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run data generation: `python -m infra.DataGenerator`
4. Solve a question: `python SQL_answer.py sql_basic_select`

## Features
- Automated SQL query validation
- User progress tracking
- Flexible question configuration
- Logging and error tracking



Practic_Questions_Platform/
│
├── config/
│   ├── config.yml                    # Data generation configuration
│   └── questions_config.yml          # Questions configuration
│
├── Questions/
│   ├── sql_basic_select/
│   │   ├── question.txt              # Problem description
│   │   ├── example_solution.sql      # Reference SQL solution
│   │   └── sloutions/
│   │       └── sloution_df.csv       # Expected solution DataFrame
│   │
│   ├── sql_join_operations/
│   │   ├── question.txt
│   │   ├── example_solution.sql
│   │   └── sloutions/
│   │       └── sloution_df.csv
│   │
│   └── sql_aggregate_functions/
│       ├── question.txt
│       ├── example_solution.sql
│       └── sloutions/
│           └── sloution_df.csv
│
├── infra/
│   ├── __init__.py
│   ├── DataGenerator.py
│   ├── AnswerValidator.py
│   ├── logging_config.py
│   └── user.py
│
├── output/
│   └── generated_data.db             # SQLite database for questions
│
├── logs/                              # Logging directory
│   ├── sql_basic_select/
│   ├── sql_join_operations/
│   └── sql_aggregate_functions/
│
├── users/                             # User progress tracking
│   └── .gitkeep
│
├── requirements.txt                   # Project dependencies
├── README.md                          # Project documentation
├── SQL_answer.py                      # Main script to solve questions
└── main.py                            # Optional main entry point
