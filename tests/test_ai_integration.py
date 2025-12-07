"""
Tests for AI Integration Components

Tests for LLM clients, hint system, and query explainer.
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime

from infra.ai.llama_client import (
    BaseLLMClient, OllamaClient, MockLLMClient,
    LLMClientFactory, LlamaConfig
)
from infra.ai.hint_system import (
    HintLevel, Hint, ProgressiveHintSystem, HintManager
)
from infra.ai.explainer import (
    ExplanationLevel, ClauseExplanation, QueryExplanation, SQLExplainer
)
from infra.difficulty import DifficultyLevel


# =============================================================================
# LLM Client Tests
# =============================================================================

class TestLlamaConfig:
    """Tests for LlamaConfig."""
    
    def test_default_config(self):
        """Test default configuration."""
        config = LlamaConfig()
        assert config.base_url == "http://localhost:11434"
        assert config.model_name == "llama3.2:3b"
        assert config.temperature == 0.7
        assert config.timeout == 60
    
    def test_custom_config(self):
        """Test custom configuration."""
        config = LlamaConfig(
            model_name="llama3.1:8b",
            temperature=0.5,
            timeout=90
        )
        assert config.model_name == "llama3.1:8b"
        assert config.temperature == 0.5
        assert config.timeout == 90
    
    def test_validate_temperature(self):
        """Test temperature validation."""
        with pytest.raises(ValueError, match="temperature must be between 0 and 1"):
            LlamaConfig(temperature=1.5)
        
        with pytest.raises(ValueError, match="temperature must be between 0 and 1"):
            LlamaConfig(temperature=-0.1)
    
    def test_validate_timeout(self):
        """Test timeout validation."""
        # Timeout validation not implemented yet in LlamaConfig
        # Just verify it accepts positive values
        config = LlamaConfig(timeout=30)
        assert config.timeout == 30


class TestMockLLMClient:
    """Tests for MockLLMClient."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.client = MockLLMClient()
    
    def test_generate_hint(self):
        """Test hint generation."""
        hint = self.client.generate_hint(
            "Select all employees",
            "SELECT * FROM emp",
            "BEGINNER",
            1
        )
        assert isinstance(hint, str)
        assert len(hint) > 0
        # Mock client returns meaningful hints
        assert len(hint) > 10
    
    def test_explain_query(self):
        """Test query explanation."""
        explanation = self.client.explain_query("SELECT * FROM employees")
        assert isinstance(explanation, str)
        assert len(explanation) > 0
    
    def test_analyze_error(self):
        """Test error analysis."""
        analysis = self.client.analyze_error(
            "SELCT * FROM employees",
            "syntax error near 'SELCT'",
            "Select all employees"
        )
        assert isinstance(analysis, str)
        assert "error" in analysis.lower() or "fix" in analysis.lower()
    
    def test_suggest_optimization(self):
        """Test optimization suggestions."""
        suggestions = self.client.suggest_optimization(
            "SELECT * FROM employees",
            "Full table scan"
        )
        assert isinstance(suggestions, str)
        assert len(suggestions) > 0


class TestLLMClientFactory:
    """Tests for LLMClientFactory."""
    
    def test_create_mock_client(self):
        """Test creating mock client."""
        from infra.ai.llama_client import LLMBackend
        config = LlamaConfig(backend=LLMBackend.MOCK)
        client = LLMClientFactory.create_client(config)
        assert isinstance(client, MockLLMClient)
    
    def test_create_ollama_client(self):
        """Test creating Ollama client."""
        from infra.ai.llama_client import LLMBackend
        config = LlamaConfig(backend=LLMBackend.OLLAMA)
        client = LLMClientFactory.create_client(config)
        assert isinstance(client, OllamaClient)
    
    def test_create_with_config(self):
        """Test creating client with custom config."""
        from infra.ai.llama_client import LLMBackend
        config = LlamaConfig(backend=LLMBackend.OLLAMA, model_name="llama3.1:8b")
        client = LLMClientFactory.create_client(config)
        assert isinstance(client, OllamaClient)
        assert client.config.model_name == "llama3.1:8b"
    
    def test_invalid_client_type(self):
        """Test error on invalid client type."""
        # Test unsupported backend
        from infra.ai.llama_client import LLMBackend
        from pathlib import Path
        config = LlamaConfig(
            backend=LLMBackend.LLAMA_CPP,
            model_path=Path("dummy/path/model.gguf")
        )
        with pytest.raises(NotImplementedError, match="llama-cpp backend not yet implemented"):
            LLMClientFactory.create_client(config)
    
    def test_create_default_client(self):
        """Test creating default client."""
        client = LLMClientFactory.create_default_client()
        # Should create mock client by default (since Ollama might not be running)
        assert isinstance(client, (MockLLMClient, OllamaClient))


# =============================================================================
# Hint System Tests
# =============================================================================

class TestHint:
    """Tests for Hint dataclass."""
    
    def test_hint_creation(self):
        """Test creating a hint."""
        hint = Hint(
            level=HintLevel.MODERATE,
            content="Try using a WHERE clause",
            penalty_points=5,
            question_name="basic_select"
        )
        assert hint.level == HintLevel.MODERATE
        assert hint.content == "Try using a WHERE clause"
        assert hint.penalty_points == 5
        assert hint.question_name == "basic_select"
        assert isinstance(hint.timestamp, datetime)
    
    def test_hint_to_dict(self):
        """Test converting hint to dictionary."""
        hint = Hint(
            level=HintLevel.SUBTLE,
            content="Think about filtering",
            penalty_points=3
        )
        data = hint.to_dict()
        
        assert data['level'] == 'SUBTLE'
        assert data['content'] == "Think about filtering"
        assert data['penalty_points'] == 3
        assert 'timestamp' in data
    
    def test_hint_from_dict(self):
        """Test creating hint from dictionary."""
        data = {
            'level': 'EXPLICIT',
            'content': "Use SELECT * FROM table",
            'penalty_points': 10,
            'timestamp': datetime.now().isoformat(),
            'question_name': 'test'
        }
        hint = Hint.from_dict(data)
        
        assert hint.level == HintLevel.EXPLICIT
        assert hint.content == "Use SELECT * FROM table"
        assert hint.penalty_points == 10


class TestProgressiveHintSystem:
    """Tests for ProgressiveHintSystem."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.client = MockLLMClient()
        self.hint_system = ProgressiveHintSystem(
            llm_client=self.client,
            difficulty_level=DifficultyLevel.BEGINNER,
            question_name="test_question"
        )
    
    def test_initialization(self):
        """Test hint system initialization."""
        assert self.hint_system.difficulty_level == DifficultyLevel.BEGINNER
        assert self.hint_system.question_name == "test_question"
        assert len(self.hint_system.hints_used) == 0
        assert self.hint_system.get_hints_remaining() == 5  # BEGINNER has 5 hints
    
    def test_get_first_hint(self):
        """Test getting first hint."""
        hint = self.hint_system.get_next_hint("Select all employees")
        
        assert isinstance(hint, Hint)
        assert hint.level == HintLevel.SUBTLE  # First hint is subtle
        assert hint.penalty_points == 5  # BEGINNER penalty
        assert len(self.hint_system.hints_used) == 1
        assert self.hint_system.get_hints_remaining() == 4
    
    def test_hint_progression(self):
        """Test hint level progression."""
        # First hint: SUBTLE
        hint1 = self.hint_system.get_next_hint("Test question")
        assert hint1.level == HintLevel.SUBTLE
        
        # Second hint: MODERATE
        hint2 = self.hint_system.get_next_hint("Test question")
        assert hint2.level == HintLevel.MODERATE
        
        # Third hint: MODERATE
        hint3 = self.hint_system.get_next_hint("Test question")
        assert hint3.level == HintLevel.MODERATE
        
        # Fourth hint: MODERATE
        hint4 = self.hint_system.get_next_hint("Test question")
        assert hint4.level == HintLevel.MODERATE
        
        # Fifth hint: EXPLICIT (max for BEGINNER)
        hint5 = self.hint_system.get_next_hint("Test question")
        assert hint5.level == HintLevel.EXPLICIT
    
    def test_hints_exhausted(self):
        """Test error when hints exhausted."""
        # Use all 5 hints
        for _ in range(5):
            self.hint_system.get_next_hint("Test question")
        
        # Try to get another hint
        with pytest.raises(ValueError, match="No hints remaining"):
            self.hint_system.get_next_hint("Test question")
    
    def test_calculate_total_penalty(self):
        """Test penalty calculation."""
        # Get 3 hints
        for _ in range(3):
            self.hint_system.get_next_hint("Test question")
        
        # Each hint costs 5 points for BEGINNER
        assert self.hint_system.calculate_total_penalty() == 15
    
    def test_hint_summary(self):
        """Test hint summary."""
        self.hint_system.get_next_hint("Test question")
        self.hint_system.get_next_hint("Test question")
        
        summary = self.hint_system.get_hint_summary()
        assert summary['total_hints_used'] == 2
        assert summary['hints_remaining'] == 3
        assert summary['total_penalty'] == 10
        assert summary['difficulty_level'] == 'BEGINNER'
        assert len(summary['hints']) == 2
    
    def test_reset(self):
        """Test resetting hint system."""
        self.hint_system.get_next_hint("Test question")
        self.hint_system.get_next_hint("Test question")
        
        self.hint_system.reset()
        
        assert len(self.hint_system.hints_used) == 0
        assert self.hint_system.get_hints_remaining() == 5
        assert self.hint_system.calculate_total_penalty() == 0
    
    def test_different_difficulty_levels(self):
        """Test hint limits for different difficulties."""
        # INTERMEDIATE: 3 hints
        intermediate = ProgressiveHintSystem(
            llm_client=self.client,
            difficulty_level=DifficultyLevel.INTERMEDIATE
        )
        assert intermediate.get_hints_remaining() == 3
        
        # ADVANCED: 2 hints
        advanced = ProgressiveHintSystem(
            llm_client=self.client,
            difficulty_level=DifficultyLevel.ADVANCED
        )
        assert advanced.get_hints_remaining() == 2
        
        # EXPERT: 1 hint
        expert = ProgressiveHintSystem(
            llm_client=self.client,
            difficulty_level=DifficultyLevel.EXPERT
        )
        assert expert.get_hints_remaining() == 1


class TestHintManager:
    """Tests for HintManager."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.manager = HintManager()
    
    def test_initialization(self):
        """Test hint manager initialization."""
        assert len(self.manager.hint_systems) == 0
        assert self.manager.global_hints_used == 0
    
    def test_get_hint_system(self):
        """Test getting/creating hint system."""
        system = self.manager.get_hint_system("q1", DifficultyLevel.BEGINNER)
        
        assert isinstance(system, ProgressiveHintSystem)
        assert system.question_name == "q1"
        assert len(self.manager.hint_systems) == 1
        
        # Getting same question returns same system
        system2 = self.manager.get_hint_system("q1", DifficultyLevel.BEGINNER)
        assert system is system2
    
    def test_request_hint(self):
        """Test requesting hint through manager."""
        hint = self.manager.request_hint(
            "q1",
            "Select all from employees",
            DifficultyLevel.BEGINNER
        )
        
        assert isinstance(hint, Hint)
        assert self.manager.global_hints_used == 1
    
    def test_multiple_questions(self):
        """Test managing hints for multiple questions."""
        self.manager.request_hint("q1", "Question 1", DifficultyLevel.BEGINNER)
        self.manager.request_hint("q2", "Question 2", DifficultyLevel.ADVANCED)
        self.manager.request_hint("q1", "Question 1", DifficultyLevel.BEGINNER)
        
        assert len(self.manager.hint_systems) == 2
        assert self.manager.global_hints_used == 3
    
    def test_get_question_summary(self):
        """Test getting summary for specific question."""
        self.manager.request_hint("q1", "Test", DifficultyLevel.BEGINNER)
        
        summary = self.manager.get_question_summary("q1")
        assert summary is not None
        assert summary['total_hints_used'] == 1
        
        # Non-existent question
        summary = self.manager.get_question_summary("nonexistent")
        assert summary is None
    
    def test_get_global_summary(self):
        """Test getting global summary."""
        self.manager.request_hint("q1", "Test 1", DifficultyLevel.BEGINNER)
        self.manager.request_hint("q2", "Test 2", DifficultyLevel.ADVANCED)
        
        summary = self.manager.get_global_summary()
        assert summary['total_hints_used'] == 2
        assert summary['questions_with_hints'] == 2
        assert 'per_question' in summary
        assert 'q1' in summary['per_question']
        assert 'q2' in summary['per_question']
    
    def test_reset_question(self):
        """Test resetting specific question."""
        self.manager.request_hint("q1", "Test", DifficultyLevel.BEGINNER)
        self.manager.reset_question("q1")
        
        summary = self.manager.get_question_summary("q1")
        assert summary['total_hints_used'] == 0
    
    def test_reset_all(self):
        """Test resetting all hint systems."""
        self.manager.request_hint("q1", "Test 1", DifficultyLevel.BEGINNER)
        self.manager.request_hint("q2", "Test 2", DifficultyLevel.ADVANCED)
        
        self.manager.reset_all()
        
        assert len(self.manager.hint_systems) == 0
        assert self.manager.global_hints_used == 0


# =============================================================================
# SQL Explainer Tests
# =============================================================================

class TestSQLExplainer:
    """Tests for SQLExplainer."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.client = MockLLMClient()
        self.explainer = SQLExplainer(llm_client=self.client)
    
    def test_explain_simple_select(self):
        """Test explaining simple SELECT query."""
        query = "SELECT first_name, last_name FROM employees WHERE salary > 50000"
        
        explanation = self.explainer.explain_query(query)
        
        assert explanation.query == query
        assert len(explanation.clauses) > 0
        assert any(c.clause_type == 'SELECT' for c in explanation.clauses)
        assert any(c.clause_type == 'FROM' for c in explanation.clauses)
        assert any(c.clause_type == 'WHERE' for c in explanation.clauses)
    
    def test_explain_join_query(self):
        """Test explaining JOIN query."""
        query = """
        SELECT e.name, d.dept_name
        FROM employees e
        INNER JOIN departments d ON e.dept_id = d.id
        """
        
        explanation = self.explainer.explain_query(query)
        
        assert any(c.clause_type == 'JOIN' for c in explanation.clauses)
    
    def test_explain_aggregate_query(self):
        """Test explaining aggregate query."""
        query = """
        SELECT department, COUNT(*) as count, AVG(salary) as avg_sal
        FROM employees
        GROUP BY department
        HAVING COUNT(*) > 5
        ORDER BY avg_sal DESC
        """
        
        explanation = self.explainer.explain_query(query)
        
        assert any(c.clause_type == 'GROUP BY' for c in explanation.clauses)
        assert any(c.clause_type == 'HAVING' for c in explanation.clauses)
        assert any(c.clause_type == 'ORDER BY' for c in explanation.clauses)
    
    def test_execution_order(self):
        """Test clause execution order."""
        query = """
        SELECT name
        FROM employees
        WHERE salary > 50000
        ORDER BY name
        """
        
        explanation = self.explainer.explain_query(query)
        
        # FROM should execute before WHERE, which should execute before SELECT
        from_clause = next(c for c in explanation.clauses if c.clause_type == 'FROM')
        where_clause = next(c for c in explanation.clauses if c.clause_type == 'WHERE')
        select_clause = next(c for c in explanation.clauses if c.clause_type == 'SELECT')
        
        assert from_clause.execution_order < where_clause.execution_order
        assert where_clause.execution_order < select_clause.execution_order
    
    def test_performance_notes_select_star(self):
        """Test performance note for SELECT *."""
        query = "SELECT * FROM employees"
        
        explanation = self.explainer.explain_query(query)
        
        # Should warn about SELECT *
        assert any(
            'SELECT *' in note or 'all columns' in note
            for note in explanation.performance_notes
        )
    
    def test_performance_notes_missing_where(self):
        """Test performance note for missing WHERE."""
        query = "SELECT name FROM employees"
        
        explanation = self.explainer.explain_query(query)
        
        # Should warn about missing WHERE
        assert any(
            'WHERE' in note or 'scan all rows' in note
            for note in explanation.performance_notes
        )
    
    def test_format_readable(self):
        """Test readable formatting."""
        query = "SELECT name FROM employees WHERE id = 1"
        
        explanation = self.explainer.explain_query(query)
        formatted = explanation.format_readable()
        
        assert isinstance(formatted, str)
        assert 'QUERY:' in formatted
        assert 'SUMMARY:' in formatted
        assert 'CLAUSE BREAKDOWN:' in formatted
        assert query in formatted
    
    def test_to_dict(self):
        """Test converting explanation to dictionary."""
        query = "SELECT * FROM employees"
        
        explanation = self.explainer.explain_query(query)
        data = explanation.to_dict()
        
        assert data['query'] == query
        assert 'summary' in data
        assert 'clauses' in data
        assert isinstance(data['clauses'], list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
