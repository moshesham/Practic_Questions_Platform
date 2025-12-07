import sqlite3
from pathlib import Path
import pandas as pd
import pytest

from infra.AnswerValidator import AnswerValidator, SecurityError
from infra.exceptions import FileIOError, DatabaseError, ValidationError


def build_temp_db(tmp_path: Path) -> Path:
    db_path = tmp_path / "test.db"
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE employees (
            employee_id INTEGER PRIMARY KEY,
            department TEXT,
            salary INTEGER
        );
        """
    )
    cur.executemany(
        "INSERT INTO employees (employee_id, department, salary) VALUES (?, ?, ?);",
        [
            (1, "Sales", 100),
            (2, "Engineering", 200),
        ],
    )
    conn.commit()
    conn.close()
    return db_path


def test_execute_query_safe(tmp_path: Path, monkeypatch):
    db_path = build_temp_db(tmp_path)
    sql_path = tmp_path / "example.sql"
    sql_path.write_text(
        "SELECT employee_id, department, salary FROM employees WHERE department = 'Sales';"
    )

    validator = AnswerValidator(base_dir=tmp_path, question_name=None, answer_path=sql_path)
    validator.db_path = db_path

    validator.load_sql()
    validator.execute_query()

    assert isinstance(validator.answer_df, pd.DataFrame)
    assert len(validator.answer_df) == 1


def test_execute_query_forbidden_keyword(tmp_path: Path):
    db_path = build_temp_db(tmp_path)
    sql_path = tmp_path / "bad.sql"
    sql_path.write_text("DELETE FROM employees;")

    validator = AnswerValidator(base_dir=tmp_path, question_name=None, answer_path=sql_path)
    validator.db_path = db_path

    validator.load_sql()
    with pytest.raises(SecurityError):
        validator.execute_query()


def test_execute_query_non_select(tmp_path: Path):
    db_path = build_temp_db(tmp_path)
    sql_path = tmp_path / "update.sql"
    sql_path.write_text("UPDATE employees SET salary = 0;")

    validator = AnswerValidator(base_dir=tmp_path, question_name=None, answer_path=sql_path)
    validator.db_path = db_path

    validator.load_sql()
    with pytest.raises(SecurityError):
        validator.execute_query()


def test_load_sql_file_not_found(tmp_path: Path):
    sql_path = tmp_path / "nonexistent.sql"
    validator = AnswerValidator(base_dir=tmp_path, question_name=None, answer_path=sql_path)
    with pytest.raises(FileIOError):
        validator.load_sql()


def test_execute_query_invalid_sql(tmp_path: Path):
    db_path = build_temp_db(tmp_path)
    sql_path = tmp_path / "invalid.sql"
    sql_path.write_text("SELECT invalid_column FROM employees;")

    validator = AnswerValidator(base_dir=tmp_path, question_name=None, answer_path=sql_path)
    validator.db_path = db_path

    validator.load_sql()
    with pytest.raises(DatabaseError):
        validator.execute_query()


def test_validate_answer_solution_file_not_found(tmp_path: Path):
    db_path = build_temp_db(tmp_path)
    sql_path = tmp_path / "example.sql"
    sql_path.write_text("SELECT * FROM employees;")

    validator = AnswerValidator(base_dir=tmp_path, question_name=None, answer_path=sql_path)
    validator.db_path = db_path

    validator.load_sql()
    validator.execute_query()

    with pytest.raises(FileIOError):
        validator.validate_answer(tmp_path / "nonexistent.csv")


def test_validate_answer_column_mismatch(tmp_path: Path):
    db_path = build_temp_db(tmp_path)
    sql_path = tmp_path / "example.sql"
    sql_path.write_text("SELECT * FROM employees;")
    solution_path = tmp_path / "solution.csv"
    # Create solution with different columns
    pd.DataFrame({"wrong_col": [1, 2]}).to_csv(solution_path, index=False)

    validator = AnswerValidator(base_dir=tmp_path, question_name=None, answer_path=sql_path)
    validator.db_path = db_path

    validator.load_sql()
    validator.execute_query()

    with pytest.raises(ValidationError):
        validator.validate_answer(solution_path)
