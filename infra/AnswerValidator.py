import pandas as pd
import sqlite3
from pathlib import Path
from typing import Optional, Union
import logging
import difflib

from .exceptions import FileIOError, DatabaseError, ValidationError, SecurityError

class AnswerValidator:
    def __init__(
        self,
        answer_path: Optional[Union[Path, str]] = None,
        base_dir: Optional[Union[Path, str]] = None,
        question_name: Optional[str] = None
    ) -> None:
        """
        Initialize AnswerValidator with flexible path resolution
        
        Args:
            answer_path (Path or str, optional): Direct path to SQL solution file
            base_dir (Path or str, optional): Base directory of the project
            question_name (str, optional): Name of the specific question
        """
        # Resolve base directory
        self.base_dir = Path(base_dir or Path(__file__).resolve().parent.parent)
        
        # Initialize logging
        self.logger = logging.getLogger(__name__)
        
        # Output and questions directories
        self.output_dir = self.base_dir / 'output'
        self.questions_dir = self.base_dir / 'Questions'
        
        # Set paths based on question name or direct path
        if question_name:
            # If question name is provided, construct paths accordingly
            self.question_path = self.questions_dir / question_name
            
            # Find SQL solution file in the question directory
            self.db_filename = next(self.question_path.glob('example_solution.sql'), None)
            
            # Find solution DataFrame in the solutions subdirectory
            self.solution_df_path = self.question_path / 'solutions' / 'solution_df.csv'
            
            # Database path
            self.db_path = self.output_dir / 'generated_data.db'
        elif answer_path:
            # If direct path is provided, use it
            self.db_filename = Path(answer_path)
            self.solution_df_path = None
            self.db_path = self.output_dir / 'generated_data.db'
        else:
            raise ValueError("Either question_name or answer_path must be provided")
        
        # # Validate file existence
        # if not self.db_filename or not self.db_filename.exists():
        #     raise FileNotFoundError(f"SQL solution file not found: {self.db_filename}")
        
        # SQL query placeholder
        self.query = None
        self.answer_df = None

    def load_sql(self) -> None:
        """
        Load SQL query from the solution file
        
        Raises:
            FileIOError: If the SQL file cannot be read.
        """
        try:
            with open(self.db_filename, 'r') as file:
                print(self.db_filename)
                self.query = file.read().strip()
            
            self.logger.info(f"SQL query loaded from {self.db_filename}")
        except (IOError, OSError) as e:
            raise FileIOError(f"Failed to read SQL file '{self.db_filename}': {e}") from e

    def _validate_query_safety(self, query: str) -> None:
        """Validate query for forbidden operations and ensure it is read-only.

        Only allows queries starting with SELECT or WITH and blocks write/DDL verbs.

        Raises:
            SecurityError: If the query is unsafe to execute.
        """

        if not query:
            raise SecurityError("Query is empty")

        normalized = query.strip().upper()

        if not (normalized.startswith("SELECT") or normalized.startswith("WITH")):
            raise SecurityError("Only read-only SELECT queries are allowed")

        forbidden_keywords = [
            "DROP",
            "DELETE",
            "UPDATE",
            "INSERT",
            "ALTER",
            "CREATE",
            "TRUNCATE",
            "EXEC",
            "PRAGMA",
        ]

        for keyword in forbidden_keywords:
            if keyword in normalized:
                raise SecurityError(f"Query contains forbidden operation: {keyword}")

    def execute_query(self) -> None:
        """
        Execute the loaded SQL query against the generated database
        
        Raises:
            SecurityError: If the query is unsafe.
            DatabaseError: If database connection or execution fails.
        """
        try:
            self._validate_query_safety(self.query)
            # Establish database connection
            conn = sqlite3.connect(self.db_path)
            
            # Execute query and load results into DataFrame
            self.answer_df = pd.read_sql_query(self.query, conn, index_col=None)
            
            # Close connection
            conn.close()
            
            self.logger.info(f"Query executed successfully. Rows returned: {len(self.answer_df)}")
        except sqlite3.Error as e:
            raise DatabaseError(f"Database error executing query: {e}") from e
        except pd.errors.DatabaseError as e:
            raise DatabaseError(f"Pandas database error: {e}") from e

    def validate_answer(self, solution_file: Optional[Union[Path, str]] = None) -> bool:
        """
        Validate the answer by comparing with expected solution
        
        Args:
            solution_file (Path or str, optional): Path to solution DataFrame
        
        Returns:
            bool: True if solution matches, False otherwise
            
        Raises:
            FileIOError: If solution file cannot be read.
            ValidationError: If DataFrame structures don't match.
        """
        # Use predefined solution path if no specific file is provided
        solution_file = solution_file or self.solution_df_path
        
        if not solution_file or not Path(solution_file).exists():
            raise FileIOError(f"Solution DataFrame file not found: {solution_file}")
        
        try:
            # Load expected solution
            solution_df = pd.read_csv(solution_file, index_col=None)
            
            # Validate DataFrame structure
            self._validate_dataframe_structure(self.answer_df, solution_df)
            
            # Compare DataFrames
            is_match = self._compare_dataframes(self.answer_df, solution_df)
            
            return is_match
        
        except pd.errors.EmptyDataError as e:
            raise FileIOError(f"Solution file is empty or invalid: {solution_file}") from e
        except pd.errors.ParserError as e:
            raise FileIOError(f"Failed to parse solution CSV file '{solution_file}': {e}") from e

    def _validate_dataframe_structure(self, df1, df2):
        """
        Validate DataFrame structure (columns and types)
        
        Args:
            df1 (pd.DataFrame): Generated answer DataFrame
            df2 (pd.DataFrame): Expected solution DataFrame
            
        Raises:
            ValidationError: If DataFrame structures don't match.
        """
        # Check column names
        if list(df1.columns) != list(df2.columns):
            column_diff = list(set(df1.columns) ^ set(df2.columns))
            raise ValidationError(f"Column mismatch: {column_diff}")
        
        # Optional: Check data types (can be customized)
        for col in df1.columns:
            if df1[col].dtype != df2[col].dtype:
                self.logger.warning(f"Data type mismatch in column {col}")

    def _compare_dataframes(self, df1, df2):
        """
        Compare two DataFrames with detailed logging
        
        Args:
            df1 (pd.DataFrame): Generated answer DataFrame
            df2 (pd.DataFrame): Expected solution DataFrame
        
        Returns:
            bool: True if DataFrames match, False otherwise
        """
        # First, check row count
        if len(df1) != len(df2):
            self.logger.error(f"Row count mismatch: {len(df1)} vs {len(df2)}")
            return False
        
        # Sort both DataFrames to ensure consistent comparison
        df1_sorted = df1.sort_values(by=list(df1.columns)).reset_index(drop=True)
        df2_sorted = df2.sort_values(by=list(df2.columns)).reset_index(drop=True)
        
        # Compare entire DataFrame
        if not df1_sorted.equals(df2_sorted):
            # Detailed difference logging
            diff_df = pd.DataFrame({
                'Matches': (df1_sorted == df2_sorted).all(axis=1)
            })
            
            mismatched_rows = df1_sorted[~diff_df['Matches']]
            self.logger.error(f"Mismatched rows: {len(mismatched_rows)}")
            
            # Optional: Log first few mismatched rows
            if len(mismatched_rows) > 0:
                self.logger.error("Sample mismatched rows:\n" + str(mismatched_rows.head()))
            
            return False
        
        return True

    def generate_detailed_report(self, df1, df2):
        """
        Generate a detailed difference report
        
        Args:
            df1 (pd.DataFrame): Generated answer DataFrame
            df2 (pd.DataFrame): Expected solution DataFrame
        
        Returns:
            str: Detailed difference report
        """
        report = []
        
        # Compare column names
        diff_columns = list(set(df1.columns) ^ set(df2.columns))
        if diff_columns:
            report.append(f"Column differences: {diff_columns}")
        
        # Compare row count
        if len(df1) != len(df2):
            report.append(f"Row count mismatch: {len(df1)} vs {len(df2)}")
        
        # Compare values
        for column in df1.columns:
            column_diff = (df1[column] != df2[column]).sum()
            if column_diff > 0:
                report.append(f"Column '{column}' has {column_diff} different values")
        
        return "\n".join(report)