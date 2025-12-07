import sqlite3
from pathlib import Path
import pandas as pd

from infra.DataGenerator import DataGenerator
from infra.AnswerValidator import AnswerValidator


def write_config(tmp_path: Path) -> Path:
    config_dir = tmp_path / "infra" / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    cfg = config_dir / "config.yml"
    cfg.write_text(
        """
        data_generation:
          num_records: 5
          seed: 1
          table_name: employees

        fields:
          - name: employee_id
            type: int
            values:
              min: 1
              max: 5
          - name: department
            type: str
            values: [Sales, Engineering]
          - name: salary
            type: int
            values:
              min: 100
              max: 200
        """
    )
    return cfg


def prepare_question(tmp_path: Path, db_path: Path) -> None:
    q_dir = tmp_path / "Questions" / "sql_basic_select"
    (q_dir / "solutions").mkdir(parents=True, exist_ok=True)

    sql_file = q_dir / "example_solution.sql"
    sql_file.write_text(
        """
        SELECT employee_id, department, salary
        FROM employees
        WHERE department = 'Sales'
        ORDER BY salary DESC
        LIMIT 3;
        """
    )

    # Build expected solution using the generated DB
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(sql_file.read_text(), conn)
    conn.close()
    solution_path = q_dir / "solutions" / "solution_df.csv"
    df.to_csv(solution_path, index=False)


def test_end_to_end_generation_and_validation(tmp_path: Path):
    cfg_path = write_config(tmp_path)
    generator = DataGenerator(yaml_config=cfg_path, base_dir=tmp_path)
    generator.generate_records()
    generator.write_to_csv()
    generator.save_to_sqlite()

    prepare_question(tmp_path, generator.db_path)

    validator = AnswerValidator(base_dir=tmp_path, question_name="sql_basic_select")
    validator.load_sql()
    validator.execute_query()
    assert validator.validate_answer() is True
