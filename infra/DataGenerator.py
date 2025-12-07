import argparse
import random
import sqlite3
from pathlib import Path
from typing import Optional, Union, List, Dict, Any

import pandas as pd
import yaml
from jsonschema import validate, ValidationError as JSONValidationError

from .config.schemas import validate_config
from .exceptions import ConfigurationError, DataGenerationError, FileIOError, DatabaseError, ValidationError


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
        self._validate_num_records(self.num_records)

        # Table name default
        self.table_name = self.table_name or cfg_table_name

        # Seed random for reproducibility when provided
        if cfg_seed is not None:
            self._validate_seed(cfg_seed)
            random.seed(cfg_seed)

        # Set up database path
        self.db_path = self.output_dir / 'generated_data.db'
        self.conn = sqlite3.connect(self.db_path)

    def _validate_num_records(self, num_records: int) -> None:
        """Validate num_records parameter.
        
        Raises:
            ValidationError: If num_records is invalid.
        """
        if not isinstance(num_records, int) or num_records < 1 or num_records > 10_000_000:
            raise ValidationError(f"num_records must be an integer between 1 and 10,000,000, got {num_records}")

    def _validate_seed(self, seed: Optional[int]) -> None:
        """Validate seed parameter.
        
        Raises:
            ValidationError: If seed is invalid.
        """
        if seed is not None and (not isinstance(seed, int) or seed < 0):
            raise ValidationError(f"seed must be a non-negative integer, got {seed}")

    def _validate_config(self, config: Dict[str, Any]) -> None:
        """Validate config structure.
        
        Raises:
            ValidationError: If config structure is invalid.
            ConfigurationError: If config fails schema validation.
        """
        if not isinstance(config, dict):
            raise ValidationError("Config must be a dictionary")
        if 'data_generation' not in config:
            raise ValidationError("Config must contain 'data_generation' key")
        if 'fields' not in config:
            raise ValidationError("Config must contain 'fields' key")
        if not isinstance(config['fields'], list) or len(config['fields']) == 0:
            raise ValidationError("'fields' must be a non-empty list")
        for field in config['fields']:
            if not isinstance(field, dict):
                raise ValidationError("Each field must be a dictionary")
            if 'name' not in field or 'type' not in field or 'values' not in field:
                raise ValidationError("Each field must have 'name', 'type', and 'values' keys")
            if field['type'] not in ['int', 'str', 'bool']:
                raise ValidationError(f"Field type must be 'int', 'str', or 'bool', got {field['type']}")
        # Also validate against JSON schema
        try:
            validate_config(config)
        except ValueError as e:
            raise ConfigurationError(f"Configuration validation failed: {e}") from e

    def load_yaml_config(self, yaml_file: Union[Path, str]) -> None:
        """Load and validate YAML configuration file.
        
        Args:
            yaml_file: Path to the YAML file.
            
        Raises:
            FileIOError: If file cannot be read.
            ConfigurationError: If YAML parsing fails or config is invalid.
        """
        try:
            with open(yaml_file, 'r') as file:
                self.config = yaml.safe_load(file)
        except (IOError, OSError) as e:
            raise FileIOError(f"Failed to read config file '{yaml_file}': {e}") from e
        except yaml.YAMLError as e:
            raise ConfigurationError(f"Failed to parse YAML config file '{yaml_file}': {e}") from e
        
        # Validate the loaded config
        self._validate_config(self.config)

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
        """Write generated records to CSV file.
        
        Args:
            filename: Name of the CSV file.
            
        Raises:
            FileIOError: If writing to file fails.
        """
        # Ensure the output directory exists
        output_file = self.output_dir / filename
        try:
            self.records.to_csv(output_file, index=False)
            print(f"CSV file '{output_file}' with {self.num_records} records has been generated.")
        except (IOError, OSError) as e:
            raise FileIOError(f"Failed to write CSV file '{output_file}': {e}") from e

    def save_to_sqlite(self) -> None:
        """Save generated records to SQLite database.
        
        Raises:
            DatabaseError: If database operation fails.
        """
        try:
            self.records.to_sql(self.table_name, self.conn, if_exists='replace', index=False)
            self.conn.close()
            print(f"Data saved to SQLite database '{self.db_path}'.")
        except sqlite3.Error as e:
            raise DatabaseError(f"Failed to save data to SQLite database '{self.db_path}': {e}") from e


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