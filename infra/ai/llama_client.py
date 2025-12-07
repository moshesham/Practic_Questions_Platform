"""
Local Llama Client for SQL Practice Platform

This module provides integration with local Llama models for intelligent
SQL assistance including hints, explanations, and error analysis.

Supports multiple backends:
- Ollama (API-based, recommended)
- llama-cpp-python (Python bindings)
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, Optional, List
from enum import Enum
import json
import logging
import requests
from pathlib import Path


logger = logging.getLogger(__name__)


class LLMBackend(Enum):
    """Supported LLM backends."""
    OLLAMA = "ollama"
    LLAMA_CPP = "llama_cpp"
    MOCK = "mock"  # For testing


@dataclass
class LlamaConfig:
    """
    Configuration for Llama model client.
    
    Attributes:
        backend: Backend to use (ollama, llama_cpp, mock)
        model_name: Name of the model (e.g., 'llama3.2:3b', 'codellama:7b')
        base_url: Base URL for API-based backends (Ollama)
        model_path: Path to local model file (for llama-cpp)
        context_length: Maximum context length
        temperature: Sampling temperature (0.0-1.0)
        max_tokens: Maximum tokens to generate
        top_p: Nucleus sampling parameter
        timeout: Request timeout in seconds
    """
    backend: LLMBackend = LLMBackend.OLLAMA
    model_name: str = "llama3.2:3b"
    base_url: str = "http://localhost:11434"
    model_path: Optional[Path] = None
    context_length: int = 4096
    temperature: float = 0.7
    max_tokens: int = 512
    top_p: float = 0.9
    timeout: int = 60
    
    def __post_init__(self):
        """Validate configuration."""
        if self.backend == LLMBackend.LLAMA_CPP and not self.model_path:
            raise ValueError("model_path required for llama_cpp backend")
        
        if self.temperature < 0 or self.temperature > 1:
            raise ValueError("temperature must be between 0 and 1")
        
        if self.top_p < 0 or self.top_p > 1:
            raise ValueError("top_p must be between 0 and 1")


class BaseLLMClient(ABC):
    """
    Abstract base class for LLM clients.
    
    All LLM backends must implement these methods to provide
    consistent AI-powered assistance across the platform.
    """
    
    @abstractmethod
    def generate_hint(
        self,
        question: str,
        user_query: Optional[str],
        difficulty: str,
        hint_level: int = 1
    ) -> str:
        """
        Generate a contextual hint for SQL question.
        
        Args:
            question: The SQL question/problem description
            user_query: User's current SQL attempt (optional)
            difficulty: Difficulty level (BEGINNER, INTERMEDIATE, etc.)
            hint_level: Progressive hint level (1=subtle, 3=explicit)
            
        Returns:
            Generated hint as string
        """
        pass
    
    @abstractmethod
    def explain_query(self, sql_query: str) -> str:
        """
        Explain SQL query in plain English.
        
        Args:
            sql_query: SQL query to explain
            
        Returns:
            Plain English explanation
        """
        pass
    
    @abstractmethod
    def analyze_error(
        self,
        user_query: str,
        error_message: str,
        question_context: Optional[str] = None
    ) -> str:
        """
        Analyze SQL error and provide guidance.
        
        Args:
            user_query: User's SQL query that caused error
            error_message: The error message from database
            question_context: Optional context about what query should do
            
        Returns:
            Analysis and suggestions for fixing the error
        """
        pass
    
    @abstractmethod
    def suggest_optimization(
        self,
        sql_query: str,
        explain_plan: Optional[str] = None
    ) -> str:
        """
        Suggest query optimizations.
        
        Args:
            sql_query: SQL query to optimize
            explain_plan: Optional EXPLAIN output
            
        Returns:
            Optimization suggestions
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if LLM backend is available.
        
        Returns:
            True if backend is available and ready
        """
        pass


class OllamaClient(BaseLLMClient):
    """
    Ollama-based LLM client.
    
    Connects to local Ollama server for LLM inference.
    Recommended backend for ease of use and performance.
    """
    
    def __init__(self, config: LlamaConfig):
        """
        Initialize Ollama client.
        
        Args:
            config: Llama configuration
        """
        self.config = config
        self.api_url = f"{config.base_url}/api/generate"
        self.chat_url = f"{config.base_url}/api/chat"
        
        logger.info(f"Initialized Ollama client: {config.model_name}")
    
    def is_available(self) -> bool:
        """Check if Ollama server is running."""
        try:
            response = requests.get(
                f"{self.config.base_url}/api/tags",
                timeout=5
            )
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            logger.warning(f"Ollama not available: {e}")
            return False
    
    def _generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Generate text using Ollama API.
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt for context
            
        Returns:
            Generated text
            
        Raises:
            RuntimeError: If Ollama request fails
        """
        try:
            payload = {
                "model": self.config.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": self.config.temperature,
                    "top_p": self.config.top_p,
                    "num_predict": self.config.max_tokens
                }
            }
            
            if system_prompt:
                payload["system"] = system_prompt
            
            response = requests.post(
                self.api_url,
                json=payload,
                timeout=self.config.timeout
            )
            response.raise_for_status()
            
            result = response.json()
            return result.get("response", "").strip()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama request failed: {e}")
            raise RuntimeError(f"Failed to generate response: {e}")
    
    def generate_hint(
        self,
        question: str,
        user_query: Optional[str],
        difficulty: str,
        hint_level: int = 1
    ) -> str:
        """Generate contextual hint using Ollama."""
        
        # Adjust hint specificity based on level
        hint_instructions = {
            1: "Give a very subtle hint that points in the right direction without revealing the solution.",
            2: "Give a moderate hint that explains the concept needed but not the exact SQL.",
            3: "Give an explicit hint that shows the SQL structure but requires the user to fill in specifics."
        }
        
        system_prompt = f"""You are a helpful SQL tutor for {difficulty} level students.
{hint_instructions.get(hint_level, hint_instructions[1])}
Keep hints concise (2-3 sentences maximum).
Never provide complete solutions."""
        
        user_prompt = f"""Question: {question}

"""
        
        if user_query:
            user_prompt += f"Student's current attempt:\n{user_query}\n\n"
        
        user_prompt += f"Provide hint #{hint_level}:"
        
        return self._generate(user_prompt, system_prompt)
    
    def explain_query(self, sql_query: str) -> str:
        """Explain SQL query in plain English."""
        
        system_prompt = """You are a SQL expert who explains queries clearly.
Break down the query into logical steps.
Use plain English that beginners can understand.
Keep explanations concise but complete."""
        
        user_prompt = f"""Explain this SQL query in plain English:

```sql
{sql_query}
```

Provide:
1. What the query does (high-level)
2. Step-by-step breakdown of each clause
3. What results it returns"""
        
        return self._generate(user_prompt, system_prompt)
    
    def analyze_error(
        self,
        user_query: str,
        error_message: str,
        question_context: Optional[str] = None
    ) -> str:
        """Analyze SQL error and provide guidance."""
        
        system_prompt = """You are a SQL debugging assistant.
Analyze errors clearly and suggest specific fixes.
Be encouraging and educational.
Keep responses concise (3-4 sentences)."""
        
        user_prompt = f"""SQL Query:
```sql
{user_query}
```

Error: {error_message}

"""
        
        if question_context:
            user_prompt += f"Goal: {question_context}\n\n"
        
        user_prompt += """Provide:
1. What caused the error
2. How to fix it
3. One tip to avoid this in future"""
        
        return self._generate(user_prompt, system_prompt)
    
    def suggest_optimization(
        self,
        sql_query: str,
        explain_plan: Optional[str] = None
    ) -> str:
        """Suggest query optimizations."""
        
        system_prompt = """You are a SQL performance expert.
Suggest practical optimizations.
Focus on beginner-friendly improvements.
Explain why each suggestion helps."""
        
        user_prompt = f"""Analyze this SQL query for optimization:

```sql
{sql_query}
```

"""
        
        if explain_plan:
            user_prompt += f"Execution plan:\n{explain_plan}\n\n"
        
        user_prompt += """Suggest:
1. Potential performance issues
2. Specific improvements
3. Best practices to follow"""
        
        return self._generate(user_prompt, system_prompt)


class MockLLMClient(BaseLLMClient):
    """
    Mock LLM client for testing.
    
    Returns predefined responses without making actual API calls.
    Useful for unit tests and development without Ollama.
    """
    
    def __init__(self, config: Optional[LlamaConfig] = None):
        """Initialize mock client."""
        self.config = config or LlamaConfig(backend=LLMBackend.MOCK)
        logger.info("Initialized Mock LLM client")
    
    def is_available(self) -> bool:
        """Mock is always available."""
        return True
    
    def generate_hint(
        self,
        question: str,
        user_query: Optional[str],
        difficulty: str,
        hint_level: int = 1
    ) -> str:
        """Return mock hint."""
        hints = {
            1: "Consider which SQL clause would help filter the data you need.",
            2: "Try using a WHERE clause to filter rows based on a condition.",
            3: "Use: SELECT columns FROM table WHERE condition;"
        }
        return hints.get(hint_level, hints[1])
    
    def explain_query(self, sql_query: str) -> str:
        """Return mock explanation."""
        return f"""This query retrieves data from a database table.

1. SELECT: Specifies which columns to retrieve
2. FROM: Indicates the table to query
3. WHERE: Filters rows based on conditions (if present)
4. Results: Returns matching rows with selected columns"""
    
    def analyze_error(
        self,
        user_query: str,
        error_message: str,
        question_context: Optional[str] = None
    ) -> str:
        """Return mock error analysis."""
        return """The error suggests a syntax issue in your query.

Common causes:
- Missing or misplaced keywords
- Incorrect column/table names
- Missing quotation marks for strings

Tip: Check SQL syntax carefully and verify table/column names."""
    
    def suggest_optimization(
        self,
        sql_query: str,
        explain_plan: Optional[str] = None
    ) -> str:
        """Return mock optimization suggestions."""
        return """Optimization suggestions:

1. Consider adding indexes on frequently queried columns
2. Use specific column names instead of SELECT *
3. Ensure WHERE clauses use indexed columns when possible

These changes can significantly improve query performance."""
    

class LLMClientFactory:
    """Factory for creating appropriate LLM client based on configuration."""
    
    @staticmethod
    def create_client(config: LlamaConfig) -> BaseLLMClient:
        """
        Create LLM client based on configuration.
        
        Args:
            config: Llama configuration
            
        Returns:
            Appropriate LLM client instance
            
        Raises:
            ValueError: If backend not supported
        """
        if config.backend == LLMBackend.OLLAMA:
            return OllamaClient(config)
        elif config.backend == LLMBackend.MOCK:
            return MockLLMClient(config)
        elif config.backend == LLMBackend.LLAMA_CPP:
            # Placeholder for future llama-cpp-python implementation
            raise NotImplementedError("llama-cpp backend not yet implemented")
        else:
            raise ValueError(f"Unsupported backend: {config.backend}")
    
    @staticmethod
    def create_default_client() -> BaseLLMClient:
        """
        Create client with default configuration.
        
        Attempts to use Ollama, falls back to Mock if unavailable.
        
        Returns:
            LLM client instance
        """
        try:
            config = LlamaConfig(backend=LLMBackend.OLLAMA)
            client = OllamaClient(config)
            
            if client.is_available():
                logger.info("Using Ollama backend")
                return client
            else:
                logger.warning("Ollama not available, using Mock backend")
                return MockLLMClient()
        except Exception as e:
            logger.error(f"Failed to create Ollama client: {e}")
            logger.info("Falling back to Mock backend")
            return MockLLMClient()


# Convenience function for quick client creation
def get_llm_client(
    backend: str = "ollama",
    model_name: str = "llama3.2:3b",
    **kwargs
) -> BaseLLMClient:
    """
    Get LLM client with simplified interface.
    
    Args:
        backend: Backend name ('ollama', 'mock')
        model_name: Model to use
        **kwargs: Additional configuration options
        
    Returns:
        LLM client instance
        
    Example:
        >>> client = get_llm_client()
        >>> hint = client.generate_hint("SELECT all users", None, "BEGINNER")
    """
    backend_enum = LLMBackend(backend.lower())
    config = LlamaConfig(backend=backend_enum, model_name=model_name, **kwargs)
    return LLMClientFactory.create_client(config)


if __name__ == "__main__":
    # Demo usage
    print("=" * 60)
    print("Local Llama Client Demo")
    print("=" * 60)
    
    # Try to create client (will fall back to mock if Ollama unavailable)
    client = LLMClientFactory.create_default_client()
    
    print(f"\nBackend: {client.__class__.__name__}")
    print(f"Available: {client.is_available()}\n")
    
    # Demo hint generation
    question = "Write a query to select all employees from the employees table"
    print(f"Question: {question}\n")
    
    hint = client.generate_hint(question, None, "BEGINNER", hint_level=1)
    print(f"Hint: {hint}\n")
    
    # Demo query explanation
    query = "SELECT first_name, last_name FROM employees WHERE salary > 50000"
    print(f"Query: {query}\n")
    
    explanation = client.explain_query(query)
    print(f"Explanation:\n{explanation}\n")
    
    print("=" * 60)
