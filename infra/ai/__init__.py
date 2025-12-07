"""
AI Integration Package for SQL Practice Platform

This package provides AI-powered assistance using local Llama models.
"""

from infra.ai.llama_client import (
    BaseLLMClient,
    OllamaClient,
    MockLLMClient,
    LLMClientFactory,
    LlamaConfig,
    get_llm_client
)
from infra.ai.hint_system import (
    HintLevel,
    Hint,
    ProgressiveHintSystem,
    HintManager
)
from infra.ai.explainer import (
    ExplanationLevel,
    ClauseExplanation,
    QueryExplanation,
    SQLExplainer
)

__version__ = "1.0.0"

__all__ = [
    # LLM Clients
    'BaseLLMClient',
    'OllamaClient',
    'MockLLMClient',
    'LLMClientFactory',
    'LlamaConfig',
    'get_llm_client',
    
    # Hint System
    'HintLevel',
    'Hint',
    'ProgressiveHintSystem',
    'HintManager',
    
    # Query Explainer
    'ExplanationLevel',
    'ClauseExplanation',
    'QueryExplanation',
    'SQLExplainer',
]

