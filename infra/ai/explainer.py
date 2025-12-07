"""
AI-Powered SQL Query Explanation Engine

This module provides intelligent SQL query explanations with step-by-step
execution flow, clause-by-clause breakdown, and performance insights.
"""

import re
import sqlite3
import functools
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import logging

from infra.ai.llama_client import BaseLLMClient, get_llm_client


logger = logging.getLogger(__name__)


@functools.total_ordering
class ExplanationLevel(Enum):
    """Explanation detail levels."""
    BASIC = 1       # Simple overview
    DETAILED = 2    # Clause-by-clause breakdown
    EXPERT = 3      # Includes execution plan and optimizations
    
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


@dataclass
class ClauseExplanation:
    """
    Explanation for a single SQL clause.
    
    Attributes:
        clause_type: Type of clause (SELECT, FROM, WHERE, etc.)
        content: The actual clause text
        explanation: Human-readable explanation
        execution_order: Order in which this clause executes (1-indexed)
    """
    clause_type: str
    content: str
    explanation: str
    execution_order: int
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'clause_type': self.clause_type,
            'content': self.content,
            'explanation': self.explanation,
            'execution_order': self.execution_order
        }


@dataclass
class QueryExplanation:
    """
    Complete query explanation with multiple perspectives.
    
    Attributes:
        query: Original SQL query
        summary: High-level summary
        clauses: List of clause-by-clause explanations
        execution_flow: Step-by-step execution description
        performance_notes: Performance considerations
        optimization_suggestions: Potential improvements
        explain_plan: Database execution plan (if available)
    """
    query: str
    summary: str
    clauses: List[ClauseExplanation] = field(default_factory=list)
    execution_flow: List[str] = field(default_factory=list)
    performance_notes: List[str] = field(default_factory=list)
    optimization_suggestions: List[str] = field(default_factory=list)
    explain_plan: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'query': self.query,
            'summary': self.summary,
            'clauses': [clause.to_dict() for clause in self.clauses],
            'execution_flow': self.execution_flow,
            'performance_notes': self.performance_notes,
            'optimization_suggestions': self.optimization_suggestions,
            'explain_plan': self.explain_plan
        }
    
    def format_readable(self) -> str:
        """Format as human-readable text."""
        lines = [
            "=" * 70,
            "SQL Query Explanation",
            "=" * 70,
            "",
            "QUERY:",
            self.query,
            "",
            "SUMMARY:",
            self.summary,
            "",
        ]
        
        if self.clauses:
            lines.extend([
                "CLAUSE BREAKDOWN:",
                "-" * 70
            ])
            for clause in sorted(self.clauses, key=lambda c: c.execution_order):
                lines.extend([
                    f"{clause.execution_order}. {clause.clause_type}: {clause.content}",
                    f"   → {clause.explanation}",
                    ""
                ])
        
        if self.execution_flow:
            lines.extend([
                "EXECUTION FLOW:",
                "-" * 70
            ])
            for i, step in enumerate(self.execution_flow, 1):
                lines.append(f"{i}. {step}")
            lines.append("")
        
        if self.performance_notes:
            lines.extend([
                "PERFORMANCE NOTES:",
                "-" * 70
            ])
            for note in self.performance_notes:
                lines.append(f"• {note}")
            lines.append("")
        
        if self.optimization_suggestions:
            lines.extend([
                "OPTIMIZATION SUGGESTIONS:",
                "-" * 70
            ])
            for suggestion in self.optimization_suggestions:
                lines.append(f"• {suggestion}")
            lines.append("")
        
        if self.explain_plan:
            lines.extend([
                "EXECUTION PLAN:",
                "-" * 70,
                self.explain_plan,
                ""
            ])
        
        lines.append("=" * 70)
        
        return "\n".join(lines)


class SQLExplainer:
    """
    AI-powered SQL query explanation engine.
    
    Features:
    - Automatic clause parsing and explanation
    - Execution flow visualization
    - Performance analysis
    - Optimization suggestions
    - Database execution plan integration
    """
    
    # SQL clause patterns
    CLAUSE_PATTERNS = {
        'SELECT': r'SELECT\s+(.+?)(?=FROM|$)',
        'FROM': r'FROM\s+(.+?)(?=WHERE|GROUP BY|HAVING|ORDER BY|LIMIT|JOIN|$)',
        'WHERE': r'WHERE\s+(.+?)(?=GROUP BY|HAVING|ORDER BY|LIMIT|$)',
        'JOIN': r'((?:INNER|LEFT|RIGHT|FULL|CROSS)?\s*JOIN\s+.+?(?=WHERE|GROUP BY|HAVING|ORDER BY|LIMIT|JOIN|$))',
        'GROUP BY': r'GROUP BY\s+(.+?)(?=HAVING|ORDER BY|LIMIT|$)',
        'HAVING': r'HAVING\s+(.+?)(?=ORDER BY|LIMIT|$)',
        'ORDER BY': r'ORDER BY\s+(.+?)(?=LIMIT|$)',
        'LIMIT': r'LIMIT\s+(\d+)',
    }
    
    # Standard execution order (FROM first, SELECT last in logical order)
    EXECUTION_ORDER = [
        'FROM', 'JOIN', 'WHERE', 'GROUP BY', 'HAVING', 'SELECT', 'ORDER BY', 'LIMIT'
    ]
    
    def __init__(
        self,
        llm_client: Optional[BaseLLMClient] = None,
        db_path: Optional[str] = None
    ):
        """
        Initialize SQL explainer.
        
        Args:
            llm_client: LLM client for AI-generated explanations
            db_path: Path to SQLite database for EXPLAIN QUERY PLAN
        """
        self.llm_client = llm_client or get_llm_client()
        self.db_path = db_path
        
        logger.info("Initialized SQLExplainer")
    
    def explain_query(
        self,
        query: str,
        level: ExplanationLevel = ExplanationLevel.DETAILED,
        include_plan: bool = False
    ) -> QueryExplanation:
        """
        Generate comprehensive query explanation.
        
        Args:
            query: SQL query to explain
            level: Detail level for explanation
            include_plan: Whether to include database execution plan
            
        Returns:
            Complete query explanation
        """
        logger.info(f"Explaining query at level: {level.name}")
        
        # Normalize query
        normalized_query = self._normalize_query(query)
        
        # Get AI-generated summary and explanation
        ai_explanation = self._get_ai_explanation(normalized_query)
        
        # Parse clauses
        clauses = self._parse_clauses(normalized_query)
        
        # Generate execution flow
        execution_flow = self._generate_execution_flow(clauses)
        
        # Get performance notes
        performance_notes = self._analyze_performance(normalized_query, clauses)
        
        # Get optimization suggestions
        optimization_suggestions = []
        if level >= ExplanationLevel.DETAILED:
            optimization_suggestions = self._get_optimization_suggestions(
                normalized_query
            )
        
        # Get execution plan if requested
        explain_plan = None
        if include_plan and self.db_path:
            explain_plan = self._get_explain_plan(normalized_query)
        
        return QueryExplanation(
            query=query,
            summary=ai_explanation,
            clauses=clauses,
            execution_flow=execution_flow,
            performance_notes=performance_notes,
            optimization_suggestions=optimization_suggestions,
            explain_plan=explain_plan
        )
    
    def _normalize_query(self, query: str) -> str:
        """
        Normalize query for parsing.
        
        Args:
            query: Raw SQL query
            
        Returns:
            Normalized query
        """
        # Remove extra whitespace
        normalized = ' '.join(query.split())
        
        # Ensure uppercase keywords for parsing
        keywords = [
            'SELECT', 'FROM', 'WHERE', 'JOIN', 'INNER', 'LEFT', 'RIGHT',
            'FULL', 'CROSS', 'ON', 'GROUP BY', 'HAVING', 'ORDER BY',
            'LIMIT', 'OFFSET', 'UNION', 'EXCEPT', 'INTERSECT'
        ]
        
        for keyword in keywords:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + keyword + r'\b'
            normalized = re.sub(
                pattern, keyword, normalized, flags=re.IGNORECASE
            )
        
        return normalized
    
    def _get_ai_explanation(self, query: str) -> str:
        """
        Get AI-generated explanation.
        
        Args:
            query: SQL query
            
        Returns:
            AI-generated explanation text
        """
        try:
            return self.llm_client.explain_query(query)
        except Exception as e:
            logger.error(f"Failed to get AI explanation: {e}")
            return (
                f"This query retrieves data from a database. "
                f"Please review the clause breakdown below for details."
            )
    
    def _parse_clauses(self, query: str) -> List[ClauseExplanation]:
        """
        Parse query into individual clauses.
        
        Args:
            query: Normalized SQL query
            
        Returns:
            List of clause explanations
        """
        clauses = []
        
        for clause_type, pattern in self.CLAUSE_PATTERNS.items():
            matches = re.findall(pattern, query, re.IGNORECASE | re.DOTALL)
            
            for match in matches:
                # Get execution order
                try:
                    execution_order = self.EXECUTION_ORDER.index(clause_type) + 1
                except ValueError:
                    execution_order = 99  # Unknown clauses go last
                
                # Generate explanation for this clause
                explanation = self._explain_clause(clause_type, match.strip())
                
                clauses.append(ClauseExplanation(
                    clause_type=clause_type,
                    content=match.strip(),
                    explanation=explanation,
                    execution_order=execution_order
                ))
        
        return clauses
    
    def _explain_clause(self, clause_type: str, content: str) -> str:
        """
        Generate explanation for a specific clause.
        
        Args:
            clause_type: Type of clause (SELECT, WHERE, etc.)
            content: Clause content
            
        Returns:
            Human-readable explanation
        """
        explanations = {
            'SELECT': f"Specifies which columns to retrieve: {content}",
            'FROM': f"Identifies the source table(s): {content}",
            'WHERE': f"Filters rows based on condition: {content}",
            'JOIN': f"Combines rows from multiple tables: {content}",
            'GROUP BY': f"Groups rows by: {content}",
            'HAVING': f"Filters groups based on: {content}",
            'ORDER BY': f"Sorts results by: {content}",
            'LIMIT': f"Limits output to {content} rows",
        }
        
        return explanations.get(
            clause_type,
            f"{clause_type} clause: {content}"
        )
    
    def _generate_execution_flow(
        self, clauses: List[ClauseExplanation]
    ) -> List[str]:
        """
        Generate step-by-step execution flow.
        
        Args:
            clauses: Parsed clauses
            
        Returns:
            List of execution steps
        """
        flow = []
        
        # Sort by execution order
        sorted_clauses = sorted(clauses, key=lambda c: c.execution_order)
        
        for clause in sorted_clauses:
            step = self._clause_to_execution_step(clause)
            if step:
                flow.append(step)
        
        return flow
    
    def _clause_to_execution_step(self, clause: ClauseExplanation) -> Optional[str]:
        """
        Convert clause to execution step description.
        
        Args:
            clause: Clause explanation
            
        Returns:
            Execution step description
        """
        steps = {
            'FROM': "Database identifies and loads the source table(s)",
            'JOIN': "Combines rows from joined tables based on join conditions",
            'WHERE': "Filters individual rows based on specified conditions",
            'GROUP BY': "Groups rows with matching values into summary rows",
            'HAVING': "Filters grouped results based on aggregate conditions",
            'SELECT': "Selects and computes the specified columns",
            'ORDER BY': "Sorts the result set according to specified criteria",
            'LIMIT': "Restricts output to specified number of rows",
        }
        
        return steps.get(clause.clause_type)
    
    def _analyze_performance(
        self, query: str, clauses: List[ClauseExplanation]
    ) -> List[str]:
        """
        Analyze query for performance considerations.
        
        Args:
            query: SQL query
            clauses: Parsed clauses
            
        Returns:
            List of performance notes
        """
        notes = []
        
        # Check for SELECT *
        if re.search(r'SELECT\s+\*', query, re.IGNORECASE):
            notes.append(
                "Using SELECT * retrieves all columns, which may impact "
                "performance. Consider selecting only needed columns."
            )
        
        # Check for missing WHERE on non-aggregate queries
        has_where = any(c.clause_type == 'WHERE' for c in clauses)
        has_group = any(c.clause_type == 'GROUP BY' for c in clauses)
        if not has_where and not has_group:
            notes.append(
                "No WHERE clause found. Query will scan all rows, "
                "which may be slow on large tables."
            )
        
        # Check for complex WHERE with OR
        where_clauses = [c for c in clauses if c.clause_type == 'WHERE']
        if where_clauses and 'OR' in where_clauses[0].content.upper():
            notes.append(
                "WHERE clause contains OR condition, which may prevent "
                "index usage. Consider restructuring if possible."
            )
        
        # Check for ORDER BY without LIMIT
        has_order = any(c.clause_type == 'ORDER BY' for c in clauses)
        has_limit = any(c.clause_type == 'LIMIT' for c in clauses)
        if has_order and not has_limit:
            notes.append(
                "ORDER BY without LIMIT sorts entire result set, "
                "which can be expensive on large datasets."
            )
        
        return notes
    
    def _get_optimization_suggestions(self, query: str) -> List[str]:
        """
        Get AI-generated optimization suggestions.
        
        Args:
            query: SQL query
            
        Returns:
            List of optimization suggestions
        """
        try:
            # Get dummy explain plan for optimization analysis
            suggestions_text = self.llm_client.suggest_optimization(
                query, "No execution plan available"
            )
            
            # Split into individual suggestions
            suggestions = [
                s.strip() for s in suggestions_text.split('\n')
                if s.strip() and not s.strip().startswith('#')
            ]
            
            return suggestions[:5]  # Limit to top 5 suggestions
            
        except Exception as e:
            logger.error(f"Failed to get optimization suggestions: {e}")
            return []
    
    def _get_explain_plan(self, query: str) -> Optional[str]:
        """
        Get database execution plan.
        
        Args:
            query: SQL query
            
        Returns:
            Execution plan text or None if unavailable
        """
        if not self.db_path:
            return None
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get query plan
            cursor.execute(f"EXPLAIN QUERY PLAN {query}")
            plan_rows = cursor.fetchall()
            
            # Format plan
            plan_lines = [
                f"{row[0]:2d} | {row[1]:2d} | {row[2]:2d} | {row[3]}"
                for row in plan_rows
            ]
            
            conn.close()
            
            return "\n".join(plan_lines)
            
        except Exception as e:
            logger.error(f"Failed to get execution plan: {e}")
            return None


if __name__ == "__main__":
    # Demo usage
    print("=" * 70)
    print("SQL Query Explanation Engine Demo")
    print("=" * 70)
    
    # Sample queries
    queries = [
        # Basic SELECT
        """
        SELECT first_name, last_name, salary
        FROM employees
        WHERE salary > 50000
        ORDER BY salary DESC
        LIMIT 10
        """,
        
        # JOIN query
        """
        SELECT e.first_name, d.department_name
        FROM employees e
        INNER JOIN departments d ON e.department_id = d.id
        WHERE d.department_name = 'Engineering'
        """,
        
        # Aggregate query
        """
        SELECT department_id, COUNT(*) as emp_count, AVG(salary) as avg_salary
        FROM employees
        GROUP BY department_id
        HAVING COUNT(*) > 5
        ORDER BY avg_salary DESC
        """
    ]
    
    explainer = SQLExplainer()
    
    for i, query in enumerate(queries, 1):
        print(f"\n\nExample {i}:")
        print("-" * 70)
        
        explanation = explainer.explain_query(
            query,
            level=ExplanationLevel.DETAILED
        )
        
        print(explanation.format_readable())
    
    print("\n" + "=" * 70)
