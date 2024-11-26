import csv
import random
import sqlite3
import yaml
import pandas as pd
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
QUESTIONS_DIR = SCRIPT_DIR / 'Questions'
SLOUTIONS_DIR = SCRIPT_DIR / 'Sloutions'
OUTPUT_DIR = SCRIPT_DIR / 'output'
DBOUTPUT_DIR = SCRIPT_DIR / 'output' / 'generated_data.db'

class DataGenerator:
    def __init__(self, sample_data=None, yaml_config=None, num_records=10000):
        self.sample_data = sample_data
        self.yaml_config = yaml_config
        self.num_records = num_records
        self.records = []
        if yaml_config:
            self.load_yaml_config(yaml_config)

        # DBOUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        self.db_path=DBOUTPUT_DIR
        self.conn = sqlite3.connect(self.db_path)

    def load_yaml_config(self, yaml_file):
        with open(yaml_file, 'r') as file:
            self.config = yaml.safe_load(file)

    def generate_random_record(self):
        record = {}
        for field in self.config['fields']:
            field_name = field['name']
            field_type = field['type']
            field_values = field['values']
            if field_type == 'int':
                value = random.choice(range(field_values['min'], field_values['max'] + 1))
            elif field_type == 'str':
                value = random.choice(field_values)
            elif field_type == 'bool':
                value = random.choice([True, False])
            record[field_name] = value
        return record

    def generate_records(self):
        records = self.sample_data.copy() if self.sample_data else []
        while len(records) < self.num_records:
            records.append(self.generate_random_record())
        self.records = pd.DataFrame(records)

    def write_to_csv(self, filename='generated_data.csv'):
        self.records.to_csv(filename, index=False)
        print(f"CSV file '{filename}' with {self.num_records} records has been generated.")

    def save_to_sqlite(self):
        self.records.to_sql('searches', self.conn, if_exists='replace', index=False)
        self.conn.close()
        print(f"Data saved to SQLite database '{self.db_path}'.")

# Initialize DataGenerator with YAML configuration from the config folder
data_gen = DataGenerator(yaml_config='config/config.yml', num_records=10000)

# Generate records
data_gen.generate_records()

# Write to CSV
data_gen.write_to_csv()

# Save data to SQLite
data_gen.save_to_sqlite()
