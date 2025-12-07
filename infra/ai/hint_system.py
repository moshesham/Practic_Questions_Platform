"""
AI-Powered Progressive Hint System

This module provides an intelligent hint system that adapts to difficulty level
and tracks hint usage for scoring adjustments.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

from infra.ai.llama_client import BaseLLMClient, get_llm_client
from infra.difficulty import DifficultyLevel, DifficultyManager


logger = logging.getLogger(__name__)


class HintLevel(Enum):
    """Progressive hint specificity levels."""
    SUBTLE = 1      # Very indirect hint
    MODERATE = 2    # Points in right direction
    EXPLICIT = 3    # Nearly gives answer


@dataclass
class Hint:
    """
    Individual hint with metadata.
    
    Attributes:
        level: Hint specificity level
        content: The actual hint text
        penalty_points: Points deducted for using this hint
        timestamp: When hint was generated
        question_name: Question this hint is for
    """
    level: HintLevel
    content: str
    penalty_points: int
    timestamp: datetime = field(default_factory=datetime.now)
    question_name: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert hint to dictionary for storage."""
        return {
            'level': self.level.name,
            'content': self.content,
            'penalty_points': self.penalty_points,
            'timestamp': self.timestamp.isoformat(),
            'question_name': self.question_name
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Hint':
        """Create hint from dictionary."""
        return cls(
            level=HintLevel[data['level']],
            content=data['content'],
            penalty_points=data['penalty_points'],
            timestamp=datetime.fromisoformat(data['timestamp']),
            question_name=data.get('question_name', '')
        )


class ProgressiveHintSystem:
    """
    Intelligent hint system that adapts to difficulty and tracks usage.
    
    Features:
    - Progressive hints that become more specific
    - Difficulty-adjusted hint counts
    - Scoring penalties for hint usage
    - AI-generated contextual hints
    - Hint history tracking
    """
    
    def __init__(
        self,
        llm_client: Optional[BaseLLMClient] = None,
        difficulty_level: DifficultyLevel = DifficultyLevel.BEGINNER,
        question_name: str = ""
    ):
        """
        Initialize hint system.
        
        Args:
            llm_client: LLM client for generating hints (creates default if None)
            difficulty_level: Difficulty level of the question
            question_name: Name of the question
        """
        self.llm_client = llm_client or get_llm_client()
        self.difficulty_level = difficulty_level
        self.question_name = question_name
        self.hints_used: List[Hint] = []
        self.difficulty_manager = DifficultyManager()
        
        # Get difficulty configuration
        self.difficulty_config = self.difficulty_manager.get_config(difficulty_level)
        
        logger.info(
            f"Initialized hint system for {difficulty_level.name} "
            f"(max hints: {self.difficulty_config.hint_count})"
        )
    
    def get_next_hint(
        self,
        question: str,
        user_query: Optional[str] = None,
        error_message: Optional[str] = None
    ) -> Hint:
        """
        Generate next progressive hint.
        
        Args:
            question: The SQL question/problem description
            user_query: User's current SQL attempt (optional)
            error_message: Any error from user's attempt (optional)
            
        Returns:
            Next hint in progression
            
        Raises:
            ValueError: If no more hints available
        """
        # Check if hints exhausted
        hints_remaining = self.get_hints_remaining()
        if hints_remaining <= 0:
            raise ValueError(
                f"No hints remaining. Maximum {self.difficulty_config.hint_count} "
                f"hints allowed for {self.difficulty_level.name} level."
            )
        
        # Determine hint level based on number already used
        hint_number = len(self.hints_used) + 1
        hint_level = self._determine_hint_level(hint_number)
        
        # Generate hint using AI
        try:
            hint_content = self._generate_hint_content(
                question, user_query, error_message, hint_level
            )
        except Exception as e:
            logger.error(f"Failed to generate hint: {e}")
            # Fallback to generic hint
            hint_content = self._get_fallback_hint(hint_level)
        
        # Calculate penalty
        penalty = self.difficulty_config.hint_penalty_points
        
        # Create hint object
        hint = Hint(
            level=hint_level,
            content=hint_content,
            penalty_points=penalty,
            question_name=self.question_name
        )
        
        # Track usage
        self.hints_used.append(hint)
        
        logger.info(
            f"Generated hint #{hint_number} (level: {hint_level.name}, "
            f"penalty: {penalty} points)"
        )
        
        return hint
    
    def _determine_hint_level(self, hint_number: int) -> HintLevel:
        """
        Determine appropriate hint level based on progression.
        
        Args:
            hint_number: Which hint in sequence (1-indexed)
            
        Returns:
            Appropriate hint level
        """
        max_hints = self.difficulty_config.hint_count
        
        if hint_number == 1:
            return HintLevel.SUBTLE
        elif hint_number >= max_hints:
            return HintLevel.EXPLICIT
        else:
            return HintLevel.MODERATE
    
    def _generate_hint_content(
        self,
        question: str,
        user_query: Optional[str],
        error_message: Optional[str],
        hint_level: HintLevel
    ) -> str:
        """
        Generate hint content using AI.
        
        Args:
            question: SQL question
            user_query: User's attempt
            error_message: Any error message
            hint_level: Level of hint to generate
            
        Returns:
            Generated hint content
        """
        # If there's an error, focus on that
        if error_message and user_query:
            return self.llm_client.analyze_error(
                user_query, error_message, question
            )
        
        # Otherwise, generate contextual hint
        return self.llm_client.generate_hint(
            question,
            user_query,
            self.difficulty_level.name,
            hint_level.value
        )
    
    def _get_fallback_hint(self, hint_level: HintLevel) -> str:
        """
        Get fallback hint if AI generation fails.
        
        Args:
            hint_level: Level of hint needed
            
        Returns:
            Generic fallback hint
        """
        fallbacks = {
            HintLevel.SUBTLE: (
                "Think about which SQL clauses you need to solve this problem. "
                "Review the question carefully for keywords."
            ),
            HintLevel.MODERATE: (
                "Consider the structure: SELECT [columns] FROM [table] "
                "WHERE [condition]. Which parts do you need?"
            ),
            HintLevel.EXPLICIT: (
                "Break down the problem step by step: "
                "1) Identify the table(s), "
                "2) Determine which columns, "
                "3) Apply any filters or conditions."
            )
        }
        return fallbacks.get(hint_level, fallbacks[HintLevel.SUBTLE])
    
    def get_hints_remaining(self) -> int:
        """
        Get number of hints still available.
        
        Returns:
            Number of hints remaining
        """
        return self.difficulty_config.hint_count - len(self.hints_used)
    
    def calculate_total_penalty(self) -> int:
        """
        Calculate total score penalty for all hints used.
        
        Returns:
            Total penalty points
        """
        return sum(hint.penalty_points for hint in self.hints_used)
    
    def get_hint_summary(self) -> Dict[str, Any]:
        """
        Get summary of hint usage.
        
        Returns:
            Dictionary with hint statistics
        """
        return {
            'total_hints_used': len(self.hints_used),
            'hints_remaining': self.get_hints_remaining(),
            'total_penalty': self.calculate_total_penalty(),
            'difficulty_level': self.difficulty_level.name,
            'max_hints': self.difficulty_config.hint_count,
            'hints': [hint.to_dict() for hint in self.hints_used]
        }
    
    def reset(self) -> None:
        """Reset hint usage (for new attempt)."""
        self.hints_used = []
        logger.info("Hint system reset")


class HintManager:
    """
    Manages hint systems for multiple questions.
    
    Tracks hint usage across user's session and maintains history.
    """
    
    def __init__(self, llm_client: Optional[BaseLLMClient] = None):
        """
        Initialize hint manager.
        
        Args:
            llm_client: Shared LLM client for all hint systems
        """
        self.llm_client = llm_client or get_llm_client()
        self.hint_systems: Dict[str, ProgressiveHintSystem] = {}
        self.global_hints_used = 0
        
        logger.info("Initialized HintManager")
    
    def get_hint_system(
        self,
        question_name: str,
        difficulty_level: DifficultyLevel
    ) -> ProgressiveHintSystem:
        """
        Get or create hint system for a question.
        
        Args:
            question_name: Unique question identifier
            difficulty_level: Question difficulty
            
        Returns:
            Hint system for the question
        """
        if question_name not in self.hint_systems:
            self.hint_systems[question_name] = ProgressiveHintSystem(
                llm_client=self.llm_client,
                difficulty_level=difficulty_level,
                question_name=question_name
            )
        
        return self.hint_systems[question_name]
    
    def request_hint(
        self,
        question_name: str,
        question_text: str,
        difficulty_level: DifficultyLevel,
        user_query: Optional[str] = None,
        error_message: Optional[str] = None
    ) -> Hint:
        """
        Request a hint for a question.
        
        Args:
            question_name: Question identifier
            question_text: Full question description
            difficulty_level: Question difficulty
            user_query: User's current attempt
            error_message: Any error message
            
        Returns:
            Generated hint
            
        Raises:
            ValueError: If no hints remaining
        """
        hint_system = self.get_hint_system(question_name, difficulty_level)
        hint = hint_system.get_next_hint(question_text, user_query, error_message)
        
        self.global_hints_used += 1
        
        return hint
    
    def get_question_summary(self, question_name: str) -> Optional[Dict[str, Any]]:
        """
        Get hint summary for specific question.
        
        Args:
            question_name: Question identifier
            
        Returns:
            Hint summary or None if question not found
        """
        if question_name in self.hint_systems:
            return self.hint_systems[question_name].get_hint_summary()
        return None
    
    def get_global_summary(self) -> Dict[str, Any]:
        """
        Get summary of all hint usage.
        
        Returns:
            Global hint statistics
        """
        total_penalty = sum(
            system.calculate_total_penalty()
            for system in self.hint_systems.values()
        )
        
        return {
            'total_hints_used': self.global_hints_used,
            'total_penalty': total_penalty,
            'questions_with_hints': len(self.hint_systems),
            'per_question': {
                name: system.get_hint_summary()
                for name, system in self.hint_systems.items()
            }
        }
    
    def reset_question(self, question_name: str) -> None:
        """
        Reset hints for a specific question.
        
        Args:
            question_name: Question to reset
        """
        if question_name in self.hint_systems:
            self.hint_systems[question_name].reset()
            logger.info(f"Reset hints for question: {question_name}")
    
    def reset_all(self) -> None:
        """Reset all hint systems."""
        self.hint_systems.clear()
        self.global_hints_used = 0
        logger.info("Reset all hint systems")


if __name__ == "__main__":
    # Demo usage
    print("=" * 60)
    print("AI-Powered Hint System Demo")
    print("=" * 60)
    
    # Create hint manager
    manager = HintManager()
    
    # Sample question
    question_name = "sql_basic_select"
    question_text = "Write a query to select first_name and last_name from employees table"
    difficulty = DifficultyLevel.BEGINNER
    
    print(f"\nQuestion: {question_text}")
    print(f"Difficulty: {difficulty.name}\n")
    
    # Request hints progressively
    for i in range(3):
        try:
            hint = manager.request_hint(
                question_name,
                question_text,
                difficulty
            )
            
            print(f"Hint #{i+1} ({hint.level.name}):")
            print(f"  {hint.content}")
            print(f"  Penalty: {hint.penalty_points} points\n")
        except ValueError as e:
            print(f"Error: {e}\n")
            break
    
    # Show summary
    summary = manager.get_question_summary(question_name)
    print("\nHint Usage Summary:")
    print(f"  Hints used: {summary['total_hints_used']}/{summary['max_hints']}")
    print(f"  Total penalty: {summary['total_penalty']} points")
    print(f"  Hints remaining: {summary['hints_remaining']}")
    
    print("\n" + "=" * 60)
