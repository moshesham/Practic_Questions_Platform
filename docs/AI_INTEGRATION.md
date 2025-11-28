# Local Llama AI Integration Specifications

This document provides detailed specifications for integrating local Llama AI models into the SQL Practice Questions Platform.

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Supported Backends](#supported-backends)
4. [Installation Guide](#installation-guide)
5. [Configuration](#configuration)
6. [API Reference](#api-reference)
7. [Use Cases](#use-cases)
8. [Best Practices](#best-practices)

---

## Overview

The platform integrates local Llama AI models to provide:

- **Intelligent Hints**: Context-aware hints that adapt to difficulty level
- **Query Explanations**: Natural language explanations of SQL queries
- **Error Analysis**: AI-powered debugging assistance
- **Solution Feedback**: Personalized feedback on user solutions
- **Query Optimization Suggestions**: Performance improvement recommendations

### Benefits of Local AI

- **Privacy**: User data never leaves the local machine
- **No API Costs**: No per-request charges
- **Offline Capability**: Works without internet connection
- **Customization**: Fine-tune models for SQL-specific tasks

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    SQL Practice Platform                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │  Hint System │    │  Explainer   │    │Error Analyzer│  │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘  │
│         │                    │                    │          │
│         └────────────────────┼────────────────────┘          │
│                              │                               │
│                    ┌─────────▼─────────┐                    │
│                    │   LLM Client      │                    │
│                    │   (Abstract)      │                    │
│                    └─────────┬─────────┘                    │
│                              │                               │
├──────────────────────────────┼───────────────────────────────┤
│                              │                               │
│  ┌───────────────┐   ┌──────▼──────┐   ┌───────────────┐   │
│  │ Ollama Client │   │ llama-cpp   │   │  Custom API   │   │
│  │   (HTTP)      │   │   Client    │   │    Client     │   │
│  └───────┬───────┘   └──────┬──────┘   └───────┬───────┘   │
│          │                   │                   │           │
└──────────┼───────────────────┼───────────────────┼───────────┘
           │                   │                   │
           ▼                   ▼                   ▼
    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
    │   Ollama    │    │  llama.cpp  │    │ Custom LLM  │
    │   Server    │    │   Binary    │    │   Server    │
    └─────────────┘    └─────────────┘    └─────────────┘
```

---

## Supported Backends

### 1. Ollama (Recommended)

Ollama provides the easiest setup for running Llama models locally.

**Pros:**
- Simple installation and management
- REST API for easy integration
- Automatic model downloading
- Good performance on consumer hardware

**Supported Models:**
- `llama3.2:1b` - Smallest, fastest
- `llama3.2:3b` - Good balance
- `llama3.1:8b` - Best quality for local use
- `codellama:7b` - Optimized for code
- `sqlcoder:7b` - Specialized for SQL

### 2. llama-cpp-python

Python bindings for llama.cpp, offering maximum control.

**Pros:**
- Direct Python integration
- Fine-grained control over inference
- Supports GGUF model format
- GPU acceleration support

**Cons:**
- More complex setup
- Requires model file management

### 3. Custom API Server

For advanced deployments with custom infrastructure.

**Pros:**
- Maximum flexibility
- Can use any LLM backend
- Custom optimizations possible

---

## Installation Guide

### Ollama Setup (Recommended)

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull recommended models
ollama pull llama3.2:3b      # General use
ollama pull codellama:7b     # Code-focused
ollama pull sqlcoder:7b      # SQL-specialized

# Start Ollama server (runs on port 11434)
ollama serve

# Verify installation
curl http://localhost:11434/api/tags
```

### llama-cpp-python Setup

```bash
# Install with CUDA support (for NVIDIA GPUs)
CMAKE_ARGS="-DLLAMA_CUDA=on" pip install llama-cpp-python

# Install CPU-only version
pip install llama-cpp-python

# Download model (example: Llama 3.2 3B)
wget https://huggingface.co/lmstudio-community/Llama-3.2-3B-Instruct-GGUF/resolve/main/Llama-3.2-3B-Instruct-Q4_K_M.gguf

# Move to models directory
mkdir -p models
mv Llama-3.2-3B-Instruct-Q4_K_M.gguf models/
```

### Platform Configuration

Add to `requirements.txt`:

```
# AI Integration Dependencies
requests>=2.28.0           # For Ollama API
llama-cpp-python>=0.2.0    # For direct llama.cpp integration
httpx>=0.24.0              # Async HTTP client
```

---

## Configuration

### Configuration File

Create `config/ai_config.yml`:

```yaml
# AI Integration Configuration

ai:
  # Enable/disable AI features
  enabled: true
  
  # Primary backend: ollama, llama_cpp, or custom
  backend: ollama
  
  # Ollama configuration
  ollama:
    base_url: http://localhost:11434
    default_model: llama3.2:3b
    timeout_seconds: 60
    
    # Model-specific settings
    models:
      hints:
        name: llama3.2:3b
        temperature: 0.7
        max_tokens: 256
      explanations:
        name: codellama:7b
        temperature: 0.3
        max_tokens: 512
      error_analysis:
        name: sqlcoder:7b
        temperature: 0.5
        max_tokens: 256
  
  # llama-cpp-python configuration
  llama_cpp:
    model_path: models/Llama-3.2-3B-Instruct-Q4_K_M.gguf
    n_ctx: 4096
    n_threads: 4
    n_gpu_layers: 0  # Set to 35 for GPU
    
  # Custom backend configuration
  custom:
    base_url: http://localhost:8000
    api_key_env: CUSTOM_LLM_API_KEY

# Hint system configuration
hints:
  # Maximum hints per difficulty level
  max_hints:
    BEGINNER: 5
    INTERMEDIATE: 3
    ADVANCED: 2
    EXPERT: 1
  
  # Score penalty per hint level
  penalties:
    SUBTLE: 5
    MODERATE: 10
    EXPLICIT: 20

# Prompt templates
prompts:
  hint_system: |
    You are a SQL tutor helping students learn SQL.
    Provide hints without giving away the complete solution.
    Adjust hint specificity based on difficulty: {difficulty}
    
  explanation_system: |
    You are an expert SQL instructor.
    Explain the following SQL query in clear, educational terms.
    Focus on helping the student understand each component.
    
  error_analysis_system: |
    You are a SQL debugging assistant.
    Analyze the error and provide clear guidance on how to fix it.
    Do not provide the complete solution.
```

### Environment Variables

```bash
# .env file
OLLAMA_BASE_URL=http://localhost:11434
LLAMA_MODEL_PATH=/path/to/model.gguf
CUSTOM_LLM_API_KEY=your-api-key-here

# Optional: GPU configuration
CUDA_VISIBLE_DEVICES=0
```

---

## API Reference

### Abstract LLM Client

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum


class LLMBackend(Enum):
    """Supported LLM backends."""
    OLLAMA = "ollama"
    LLAMA_CPP = "llama_cpp"
    CUSTOM = "custom"


@dataclass
class LLMConfig:
    """Configuration for LLM client."""
    backend: LLMBackend
    model_name: str
    temperature: float = 0.7
    max_tokens: int = 512
    top_p: float = 0.9
    context_length: int = 4096
    
    # Backend-specific config
    ollama_base_url: str = "http://localhost:11434"
    llama_cpp_model_path: Optional[str] = None
    custom_base_url: Optional[str] = None
    custom_api_key: Optional[str] = None


class BaseLLMClient(ABC):
    """Abstract base class for LLM clients."""
    
    @abstractmethod
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """Generate text completion.
        
        Args:
            prompt: User prompt
            system_prompt: System instructions
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text response
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if LLM backend is available."""
        pass
    
    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about loaded model."""
        pass
```

### Ollama Client Implementation

```python
import requests
from typing import Optional, Dict, Any


class OllamaClient(BaseLLMClient):
    """Client for Ollama LLM server."""
    
    def __init__(self, config: LLMConfig):
        self.config = config
        self.base_url = config.ollama_base_url
        self.model = config.model_name
        
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """Generate completion using Ollama API."""
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature or self.config.temperature,
                "num_predict": max_tokens or self.config.max_tokens,
                "top_p": self.config.top_p,
            }
        }
        
        if system_prompt:
            payload["system"] = system_prompt
            
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        
        return response.json()["response"]
    
    def is_available(self) -> bool:
        """Check if Ollama server is running."""
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=5
            )
            return response.status_code == 200
        except requests.RequestException:
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about loaded model."""
        response = requests.get(
            f"{self.base_url}/api/show",
            json={"name": self.model},
            timeout=10
        )
        return response.json()
```

### Hint System API

```python
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional


class HintLevel(Enum):
    """Hint specificity levels."""
    SUBTLE = 1      # Very indirect hint
    MODERATE = 2    # Points in right direction
    EXPLICIT = 3    # Nearly gives answer


@dataclass
class Hint:
    """A single hint with metadata."""
    level: HintLevel
    content: str
    penalty_points: int


class ProgressiveHintSystem:
    """Provides AI-powered progressive hints."""
    
    def __init__(
        self,
        llm_client: BaseLLMClient,
        difficulty: str,
        max_hints: int = 3
    ):
        self.llm_client = llm_client
        self.difficulty = difficulty
        self.max_hints = max_hints
        self.hints_used: List[Hint] = []
        
    def get_next_hint(
        self,
        question: str,
        user_query: Optional[str] = None,
        error_message: Optional[str] = None
    ) -> Hint:
        """Generate the next progressive hint.
        
        Args:
            question: The SQL question being solved
            user_query: User's current query attempt
            error_message: Any error from query execution
            
        Returns:
            Hint object with content and metadata
            
        Raises:
            HintLimitExceededError: If max hints reached
        """
        if len(self.hints_used) >= self.max_hints:
            raise HintLimitExceededError(
                f"Maximum hints ({self.max_hints}) exceeded"
            )
        
        # Determine hint level based on hints already used
        hint_number = len(self.hints_used) + 1
        hint_level = self._determine_hint_level(hint_number)
        
        # Generate hint using LLM
        prompt = self._create_hint_prompt(
            question, user_query, error_message, hint_level
        )
        
        hint_content = self.llm_client.generate(
            prompt=prompt,
            system_prompt=HINT_SYSTEM_PROMPT,
            temperature=0.7,
            max_tokens=256
        )
        
        hint = Hint(
            level=hint_level,
            content=hint_content,
            penalty_points=self._get_penalty(hint_level)
        )
        
        self.hints_used.append(hint)
        return hint
    
    def calculate_total_penalty(self) -> int:
        """Calculate total score penalty from hints used."""
        return sum(h.penalty_points for h in self.hints_used)
```

### Query Explainer API

```python
from typing import List, Dict


class SQLExplainer:
    """AI-powered SQL query explanation system."""
    
    def __init__(self, llm_client: BaseLLMClient):
        self.llm_client = llm_client
    
    def explain_step_by_step(self, query: str) -> List[str]:
        """Break down query into logical execution steps.
        
        Args:
            query: SQL query to explain
            
        Returns:
            List of step-by-step explanations
        """
        prompt = f"""
        Break down the following SQL query into logical steps:
        
        ```sql
        {query}
        ```
        
        Explain each step in the order the database would process it.
        Format as a numbered list.
        """
        
        response = self.llm_client.generate(
            prompt=prompt,
            system_prompt=EXPLANATION_SYSTEM_PROMPT,
            temperature=0.3,
            max_tokens=512
        )
        
        return self._parse_steps(response)
    
    def explain_for_beginner(self, query: str) -> str:
        """Provide beginner-friendly explanation.
        
        Uses simple language and analogies to explain
        the query concept.
        """
        prompt = f"""
        Explain this SQL query to a complete beginner:
        
        ```sql
        {query}
        ```
        
        Use simple language, analogies, and avoid jargon.
        Explain what the query does in plain English.
        """
        
        return self.llm_client.generate(
            prompt=prompt,
            system_prompt=BEGINNER_EXPLANATION_PROMPT,
            temperature=0.5,
            max_tokens=400
        )
    
    def compare_queries(
        self,
        user_query: str,
        reference_query: str
    ) -> str:
        """Compare user's query with reference solution.
        
        Highlights differences and suggests improvements
        without giving away the complete answer.
        """
        prompt = f"""
        Compare these two SQL queries:
        
        User's Query:
        ```sql
        {user_query}
        ```
        
        Reference Approach:
        ```sql
        {reference_query}
        ```
        
        Explain the key differences and suggest improvements
        for the user's approach without revealing the exact solution.
        """
        
        return self.llm_client.generate(
            prompt=prompt,
            temperature=0.5,
            max_tokens=400
        )
```

---

## Use Cases

### 1. Progressive Hint Generation

```python
# Example usage in answer validation flow
from infra.ai import ProgressiveHintSystem, OllamaClient, LLMConfig

# Initialize client
config = LLMConfig(
    backend=LLMBackend.OLLAMA,
    model_name="llama3.2:3b"
)
client = OllamaClient(config)

# Create hint system for intermediate question
hint_system = ProgressiveHintSystem(
    llm_client=client,
    difficulty="INTERMEDIATE",
    max_hints=3
)

# User requests first hint
hint1 = hint_system.get_next_hint(
    question="Find employees earning above average salary",
    user_query="SELECT * FROM employees WHERE salary > ???"
)
print(f"Hint 1 ({hint1.level.name}): {hint1.content}")
# Output: "Consider using a subquery to calculate the average..."

# User requests second hint after more attempts
hint2 = hint_system.get_next_hint(
    question="Find employees earning above average salary",
    user_query="SELECT * FROM employees WHERE salary > (SELECT ???)"
)
print(f"Hint 2 ({hint2.level.name}): {hint2.content}")
# Output: "Use AVG(salary) in your subquery to get the average..."
```

### 2. Error Analysis

```python
# When user's query produces an error
error_analyzer = ErrorAnalyzer(client)

error_message = "no such column: salaries"
user_query = "SELECT * FROM employees WHERE salaries > 50000"

analysis = error_analyzer.analyze(
    user_query=user_query,
    error_message=error_message,
    table_schema=EMPLOYEES_SCHEMA
)

print(analysis)
# Output: "The error indicates you're referencing a column 
# 'salaries' that doesn't exist. Check the table schema - 
# the correct column name might be 'salary' (singular)."
```

### 3. Query Explanation for Learning

```python
explainer = SQLExplainer(client)

complex_query = """
SELECT d.department_name, COUNT(e.employee_id) as emp_count
FROM departments d
LEFT JOIN employees e ON d.department_id = e.department_id
GROUP BY d.department_name
HAVING COUNT(e.employee_id) > 5
ORDER BY emp_count DESC;
"""

# Step-by-step for advanced users
steps = explainer.explain_step_by_step(complex_query)
for i, step in enumerate(steps, 1):
    print(f"{i}. {step}")

# Simple explanation for beginners
simple = explainer.explain_for_beginner(complex_query)
print(simple)
# Output: "This query is like asking: 'For each department,
# count how many employees work there, but only show me
# departments with more than 5 employees, and sort them
# from most to least employees.'"
```

---

## Best Practices

### 1. Model Selection

| Use Case | Recommended Model | Reason |
|----------|-------------------|--------|
| Quick hints | llama3.2:1b | Fast response |
| Detailed explanations | llama3.2:3b | Good balance |
| Code/SQL tasks | codellama:7b | Code-optimized |
| SQL-specific | sqlcoder:7b | Best for SQL |

### 2. Prompt Engineering

```python
# Use clear, structured prompts
HINT_PROMPT = """
You are helping a student learn SQL at the {difficulty} level.

Question they're trying to solve:
{question}

Their current attempt:
```sql
{user_query}
```

Provide a {hint_level} hint that:
1. Guides them in the right direction
2. Does NOT reveal the complete solution
3. Is appropriate for their skill level
4. Encourages learning through discovery

Hint:
"""
```

### 3. Error Handling

```python
def safe_generate_hint(
    hint_system: ProgressiveHintSystem,
    question: str,
    user_query: str
) -> Optional[str]:
    """Generate hint with fallback handling."""
    try:
        hint = hint_system.get_next_hint(question, user_query)
        return hint.content
    except LLMUnavailableError:
        # Fallback to static hints
        return get_static_hint(question, len(hint_system.hints_used))
    except HintLimitExceededError:
        return "You've used all available hints for this question."
    except Exception as e:
        logger.error(f"Hint generation failed: {e}")
        return "Unable to generate hint. Please try again."
```

### 4. Caching Responses

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_explanation_cached(query_hash: str, query: str) -> str:
    """Cache explanations to avoid redundant API calls."""
    return explainer.explain_step_by_step(query)
```

### 5. Monitoring and Logging

```python
import time
import logging

logger = logging.getLogger(__name__)

def monitored_generate(client: BaseLLMClient, prompt: str) -> str:
    """Generate with monitoring."""
    start_time = time.time()
    
    try:
        response = client.generate(prompt)
        elapsed = time.time() - start_time
        
        logger.info(
            "LLM generation completed",
            extra={
                "elapsed_seconds": elapsed,
                "prompt_length": len(prompt),
                "response_length": len(response),
                "model": client.config.model_name
            }
        )
        
        return response
    except Exception as e:
        logger.error(f"LLM generation failed: {e}")
        raise
```

---

## Troubleshooting

### Ollama Connection Issues

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Check logs
journalctl -u ollama -f

# Restart Ollama
systemctl restart ollama
```

### Model Loading Issues

```bash
# List available models
ollama list

# Pull model if missing
ollama pull llama3.2:3b

# Check model details
ollama show llama3.2:3b
```

### Performance Issues

- Use smaller models for quick tasks
- Enable GPU acceleration if available
- Consider batch processing for multiple hints
- Implement response caching

---

*Last Updated: November 2024*
