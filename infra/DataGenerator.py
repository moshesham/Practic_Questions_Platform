import csv
import random
import sqlite3
import yaml
import pandas as pd
from pathlib import Path


class DataGenerator:
    def __init__(self, sample_data=None, yaml_config=None, num_records=10000, base_dir=None):
        # Use the calling script's directory as base if not provided
        self.base_dir = base_dir or Path(__file__).resolve().parent.parent

        # Ensure all directory paths are relative to the base directory
        self.output_dir = self.base_dir / 'output'
        self.config_dir = self.base_dir / 'config'

        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.sample_data = sample_data
        self.yaml_config = yaml_config or self.config_dir / 'config.yml'
        self.num_records = num_records
        self.records = []

        # Load configuration
        if self.yaml_config:
            self.load_yaml_config(self.yaml_config)

        # Set up database path
        self.db_path = self.output_dir / 'generated_data.db'
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
        # Ensure the output directory exists
        output_file = self.output_dir / filename
        self.records.to_csv(output_file, index=False)
        print(f"CSV file '{output_file}' with {self.num_records} records has been generated.")

    def save_to_sqlite(self):
        self.records.to_sql('searches', self.conn, if_exists='replace', index=False)
        self.conn.close()
        print(f"Data saved to SQLite database '{self.db_path}'.")


def main():
    # Use current script's directory to determine base directory
    base_dir = Path(__file__).resolve().parent.parent

    # Initialize DataGenerator with relative paths
    data_gen = DataGenerator(
        yaml_config=base_dir / 'config' / 'config.yml',
        num_records=10000,
        base_dir=base_dir
    )

    # Generate records
    data_gen.generate_records()

    # Write to CSV
    data_gen.write_to_csv()

    # Save data to SQLite
    data_gen.save_to_sqlite()


if __name__ == "__main__":
    main()