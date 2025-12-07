import os
from pathlib import Path
import sqlite3
import pandas as pd

from infra.DataGenerator import DataGenerator


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
