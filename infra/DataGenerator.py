import argparse
import random
import sqlite3
from pathlib import Path
from typing import Optional, Union, List, Dict, Any

import pandas as pd
import yaml


class DataGenerator:
    def __init__(
        self,
        sample_data: Optional[List[Dict[str, Any]]] = None,
        yaml_config: Optional[Union[Path, str]] = None,
        num_records: Optional[int] = None,
        base_dir: Optional[Union[Path, str]] = None,
        table_name: Optional[str] = None
    ) -> None:
        # Use the calling script's directory as base if not provided
        self.base_dir = base_dir or Path(__file__).resolve().parent.parent

        # Ensure all directory paths are relative to the base directory
        self.output_dir = self.base_dir / 'output'
        # Config lives under infra/config relative to repo root
        self.config_dir = self.base_dir / 'infra' / 'config'

        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.sample_data = sample_data
        self.yaml_config = yaml_config or self.config_dir / 'config.yml'
        self.num_records = num_records
        self.records = []
        self.table_name = table_name

        # Load configuration
        if self.yaml_config:
            self.load_yaml_config(self.yaml_config)

        # Apply data generation settings from config when available
        cfg_gen = self.config.get('data_generation', {}) if hasattr(self, 'config') else {}
        cfg_num_records = cfg_gen.get('num_records')
        cfg_seed = cfg_gen.get('seed')
        cfg_table_name = cfg_gen.get('table_name') or 'searches'

        # Prefer explicit arg, otherwise fall back to config value, finally default to 10000
        self.num_records = self.num_records or cfg_num_records or 10000

        # Table name default
        self.table_name = self.table_name or cfg_table_name

        # Seed random for reproducibility when provided
        if cfg_seed is not None:
            random.seed(cfg_seed)

        # Set up database path
        self.db_path = self.output_dir / 'generated_data.db'
        self.conn = sqlite3.connect(self.db_path)

    def load_yaml_config(self, yaml_file: Union[Path, str]) -> None:
        with open(yaml_file, 'r') as file:
            self.config = yaml.safe_load(file)

    def generate_random_record(self) -> Dict[str, Any]:
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

    def generate_records(self) -> None:
        records = self.sample_data.copy() if self.sample_data else []
        while len(records) < self.num_records:
            records.append(self.generate_random_record())
        self.records = pd.DataFrame(records)

    def write_to_csv(self, filename: str = 'generated_data.csv') -> None:
        # Ensure the output directory exists
        output_file = self.output_dir / filename
        self.records.to_csv(output_file, index=False)
        print(f"CSV file '{output_file}' with {self.num_records} records has been generated.")

    def save_to_sqlite(self) -> None:
        self.records.to_sql(self.table_name, self.conn, if_exists='replace', index=False)
        self.conn.close()
        print(f"Data saved to SQLite database '{self.db_path}'.")


def parse_args():
    parser = argparse.ArgumentParser(description="Generate synthetic data for the SQL practice platform.")
    parser.add_argument("--config", type=str, default=None, help="Path to YAML config (defaults to infra/config/config.yml)")
    parser.add_argument("--num-records", type=int, default=None, help="Override number of records (else use config)")
    parser.add_argument("--seed", type=int, default=None, help="Override RNG seed (else use config)")
    parser.add_argument("--table", type=str, default=None, help="SQLite table name (else use config table_name or 'searches')")
    return parser.parse_args()


def main():
    args = parse_args()

    # Use current script's directory to determine base directory
    base_dir = Path(__file__).resolve().parent.parent

    # Resolve config path
    yaml_path = Path(args.config) if args.config else base_dir / 'infra' / 'config' / 'config.yml'

    # Initialize DataGenerator with relative paths
    data_gen = DataGenerator(
        yaml_config=yaml_path,
        num_records=args.num_records,
        base_dir=base_dir,
        table_name=args.table
    )

    # If user overrides seed, apply it after config load
    if args.seed is not None:
        random.seed(args.seed)

    # Generate records
    data_gen.generate_records()

    # Write to CSV
    data_gen.write_to_csv()

    # Save data to SQLite
    data_gen.save_to_sqlite()


if __name__ == "__main__":
    main()