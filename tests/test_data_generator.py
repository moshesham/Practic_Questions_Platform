import os
from pathlib import Path
import sqlite3
import pandas as pd

from infra.DataGenerator import DataGenerator
from infra.config.schemas import validate_config, validate_questions_config


def test_generate_records_creates_csv_and_table(tmp_path, monkeypatch):
    base_dir = Path(__file__).resolve().parent.parent
    yaml_path = base_dir / "infra" / "config" / "config.yml"

    # Use temp output directory
    out_dir = tmp_path / "output"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Monkeypatch base_dir to temp for outputs, but keep config path
    dg = DataGenerator(
        yaml_config=yaml_path,
        num_records=10,
        base_dir=tmp_path,
        table_name="test_attempts",
    )

    dg.generate_records()
    dg.write_to_csv()
    dg.save_to_sqlite()

    csv_path = out_dir / "generated_data.csv"
    assert csv_path.exists(), "CSV should be generated"

    df = pd.read_csv(csv_path)
    expected_cols = {
        "user_id",
        "question_id",
        "difficulty",
        "category",
        "attempt_number",
        "is_correct",
        "time_ms",
        "hints_used",
        "uses_ollama",
        "client",
    }
    assert expected_cols.issubset(df.columns), "CSV should contain expected columns"
    assert len(df) == 10, "Should generate requested number of records"

    # Check SQLite table exists
    db_path = out_dir / "generated_data.db"
    assert db_path.exists(), "DB file should be created"
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.execute("SELECT COUNT(*) FROM test_attempts")
        count = cur.fetchone()[0]
        assert count == 10, "Table should contain generated rows"
    finally:
        conn.close()


def test_validate_num_records():
    dg = DataGenerator()
    # Valid
    dg._validate_num_records(1)
    dg._validate_num_records(10000000)
    dg._validate_num_records(1000)
    # Invalid
    try:
        dg._validate_num_records(0)
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    try:
        dg._validate_num_records(10000001)
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    try:
        dg._validate_num_records(-1)
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    try:
        dg._validate_num_records("100")
        assert False, "Should raise ValueError"
    except ValueError:
        pass


def test_validate_seed():
    dg = DataGenerator()
    # Valid
    dg._validate_seed(None)
    dg._validate_seed(0)
    dg._validate_seed(42)
    # Invalid
    try:
        dg._validate_seed(-1)
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    try:
        dg._validate_seed("42")
        assert False, "Should raise ValueError"
    except ValueError:
        pass


def test_validate_config():
    dg = DataGenerator()
    # Valid config (simplified)
    valid_config = {
        "data_generation": {"num_records": 1000, "seed": 42, "table_name": "test"},
        "fields": [
            {"name": "id", "type": "int", "values": {"min": 1, "max": 10}},
            {"name": "name", "type": "str", "values": ["a", "b"]},
            {"name": "active", "type": "bool", "values": [True, False]}
        ]
    }
    dg._validate_config(valid_config)
    # Invalid: missing data_generation
    invalid_config1 = {"fields": []}
    try:
        dg._validate_config(invalid_config1)
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    # Invalid: missing fields
    invalid_config2 = {"data_generation": {}}
    try:
        dg._validate_config(invalid_config2)
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    # Invalid: empty fields
    invalid_config3 = {"data_generation": {}, "fields": []}
    try:
        dg._validate_config(invalid_config3)
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    # Invalid: field missing keys
    invalid_config4 = {"data_generation": {}, "fields": [{"name": "id"}]}
    try:
        dg._validate_config(invalid_config4)
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    # Invalid: wrong type
    invalid_config5 = {"data_generation": {}, "fields": [{"name": "id", "type": "float", "values": {}}]}
    try:
        dg._validate_config(invalid_config5)
        assert False, "Should raise ValueError"
    except ValueError:
        pass


def test_invalid_config_raises_error(tmp_path):
    # Test that invalid config raises error during init
    invalid_config = tmp_path / "invalid.yml"
    with open(invalid_config, 'w') as f:
        f.write("invalid: yaml\n")
    try:
        DataGenerator(yaml_config=invalid_config, base_dir=tmp_path)
        assert False, "Should raise ValueError"
    except ValueError:
        pass


def test_validate_config_schema():
    # Valid config
    valid_config = {
        "data_generation": {"num_records": 1000, "seed": 42, "table_name": "test"},
        "fields": [
            {"name": "id", "type": "int", "values": {"min": 1, "max": 10}},
            {"name": "name", "type": "str", "values": ["a", "b"]},
            {"name": "active", "type": "bool", "values": [True, False]}
        ]
    }
    validate_config(valid_config)  # Should not raise
    # Invalid: num_records too large
    invalid_config = valid_config.copy()
    invalid_config["data_generation"]["num_records"] = 20000000
    try:
        validate_config(invalid_config)
        assert False, "Should raise ValueError"
    except ValueError:
        pass


def test_validate_questions_config_schema():
    # Valid questions config
    valid_questions = {
        "questions": [
            {
                "name": "test_question",
                "difficulty": "BEGINNER",
                "time_limit_seconds": 300,
                "hints_available": 5,
                "tags": ["test"],
                "active": True,
                "description": "Test",
                "prerequisite_questions": [],
                "sql_features": ["SELECT"],
                "learning_objectives": ["Learn"]
            }
        ]
    }
    validate_questions_config(valid_questions)  # Should not raise
    # Invalid: wrong difficulty
    invalid_questions = valid_questions.copy()
    invalid_questions["questions"][0]["difficulty"] = "INVALID"
    try:
        validate_questions_config(invalid_questions)
        assert False, "Should raise ValueError"
    except ValueError:
        pass
