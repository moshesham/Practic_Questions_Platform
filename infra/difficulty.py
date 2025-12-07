"""
Difficulty Level System for SQL Practice Questions Platform

This module provides a comprehensive difficulty level system with configurations
for different SQL practice levels: BEGINNER, INTERMEDIATE, ADVANCED, and EXPERT.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set


class DifficultyLevel(Enum):
    """Enumeration of SQL question difficulty levels."""
    
    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3
    EXPERT = 4
    
    @classmethod
    def from_string(cls, level_str: str) -> 'DifficultyLevel':
        """
        Convert string to DifficultyLevel enum.
        
        Args:
            level_str: String representation (case-insensitive)
            
        Returns:
            DifficultyLevel enum value
            
        Raises:
            ValueError: If invalid level string
        """
        level_map = {
            'beginner': cls.BEGINNER,
            'intermediate': cls.INTERMEDIATE,
            'advanced': cls.ADVANCED,
            'expert': cls.EXPERT
        }
        
        normalized = level_str.lower().strip()
        if normalized not in level_map:
            raise ValueError(
                f"Invalid difficulty level: {level_str}. "
                f"Must be one of: {list(level_map.keys())}"
            )
        
        return level_map[normalized]
    
    def __str__(self) -> str:
        """Return string representation of difficulty level."""
        return self.name.capitalize()


@dataclass
class DifficultyConfig:
    """
    Configuration for a specific difficulty level.
    
    Attributes:
        level: The difficulty level
        time_limit_seconds: Maximum time allowed for the question (in seconds)
        hint_count: Maximum number of hints available
        allowed_sql_features: List of SQL features/keywords allowed at this level
        scoring_multiplier: Score multiplier for correct answers (higher = more points)
        prerequisite_level: Required difficulty level to unlock (None for BEGINNER)
        hint_penalty_points: Points deducted per hint used
        time_bonus_threshold: If completed under this time, get bonus points
    """
    
    level: DifficultyLevel
    time_limit_seconds: int
    hint_count: int
    allowed_sql_features: List[str]
    scoring_multiplier: float
    prerequisite_level: Optional[DifficultyLevel] = None
    hint_penalty_points: int = 5
    time_bonus_threshold: Optional[int] = None
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        if self.time_limit_seconds <= 0:
            raise ValueError("time_limit_seconds must be positive")
        if self.hint_count < 0:
            raise ValueError("hint_count cannot be negative")
        if self.scoring_multiplier <= 0:
            raise ValueError("scoring_multiplier must be positive")


# Predefined difficulty configurations
DIFFICULTY_CONFIGS: Dict[DifficultyLevel, DifficultyConfig] = {
    DifficultyLevel.BEGINNER: DifficultyConfig(
        level=DifficultyLevel.BEGINNER,
        time_limit_seconds=300,  # 5 minutes
        hint_count=5,
        allowed_sql_features=[
            'SELECT', 'FROM', 'WHERE', 'ORDER BY', 'LIMIT',
            'DISTINCT', 'AND', 'OR', 'NOT', 'LIKE', 'IN',
            'BETWEEN', 'IS NULL', 'IS NOT NULL'
        ],
        scoring_multiplier=1.0,
        prerequisite_level=None,
        hint_penalty_points=5,
        time_bonus_threshold=180  # 3 minutes
    ),
    
    DifficultyLevel.INTERMEDIATE: DifficultyConfig(
        level=DifficultyLevel.INTERMEDIATE,
        time_limit_seconds=600,  # 10 minutes
        hint_count=3,
        allowed_sql_features=[
            # All BEGINNER features plus:
            'JOIN', 'INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN', 'FULL JOIN',
            'GROUP BY', 'HAVING', 'COUNT', 'SUM', 'AVG', 'MIN', 'MAX',
            'SUBQUERY', 'EXISTS', 'ANY', 'ALL', 'UNION', 'INTERSECT', 'EXCEPT',
            'CASE', 'WHEN', 'THEN', 'ELSE', 'END'
        ],
        scoring_multiplier=2.0,
        prerequisite_level=DifficultyLevel.BEGINNER,
        hint_penalty_points=10,
        time_bonus_threshold=360  # 6 minutes
    ),
    
    DifficultyLevel.ADVANCED: DifficultyConfig(
        level=DifficultyLevel.ADVANCED,
        time_limit_seconds=900,  # 15 minutes
        hint_count=2,
        allowed_sql_features=[
            # All INTERMEDIATE features plus:
            'WINDOW FUNCTIONS', 'ROW_NUMBER', 'RANK', 'DENSE_RANK',
            'NTILE', 'LAG', 'LEAD', 'FIRST_VALUE', 'LAST_VALUE',
            'OVER', 'PARTITION BY', 'CTE', 'WITH', 'RECURSIVE',
            'COALESCE', 'NULLIF', 'CAST', 'CONVERT',
            'STRING_AGG', 'ARRAY_AGG'
        ],
        scoring_multiplier=3.0,
        prerequisite_level=DifficultyLevel.INTERMEDIATE,
        hint_penalty_points=15,
        time_bonus_threshold=540  # 9 minutes
    ),
    
    DifficultyLevel.EXPERT: DifficultyConfig(
        level=DifficultyLevel.EXPERT,
        time_limit_seconds=1800,  # 30 minutes
        hint_count=1,
        allowed_sql_features=[
            # All ADVANCED features plus:
            'RECURSIVE CTE', 'LATERAL JOIN', 'CROSS APPLY', 'OUTER APPLY',
            'PIVOT', 'UNPIVOT', 'MATERIALIZED', 'PERFORMANCE OPTIMIZATION',
            'INDEX HINTS', 'QUERY PLANS', 'ADVANCED ANALYTICS'
        ],
        scoring_multiplier=5.0,
        prerequisite_level=DifficultyLevel.ADVANCED,
        hint_penalty_points=25,
        time_bonus_threshold=900  # 15 minutes
    )
}


class DifficultyManager:
    """
    Manager for difficulty level operations and validations.
    """
    
    def __init__(self):
        """Initialize the difficulty manager with predefined configs."""
        self.configs = DIFFICULTY_CONFIGS
    
    def get_config(self, level: DifficultyLevel) -> DifficultyConfig:
        """
        Get configuration for a specific difficulty level.
        
        Args:
            level: The difficulty level
            
        Returns:
            DifficultyConfig for the level
            
        Raises:
            KeyError: If level not found
        """
        if level not in self.configs:
            raise KeyError(f"No configuration found for level: {level}")
        return self.configs[level]
    
    def validate_progression(
        self,
        current_level: DifficultyLevel,
        completed_levels: Set[DifficultyLevel]
    ) -> bool:
        """
        Check if user can access a difficulty level based on prerequisites.
        
        Args:
            current_level: Level user wants to access
            completed_levels: Set of levels user has completed
            
        Returns:
            True if user meets prerequisites, False otherwise
        """
        config = self.get_config(current_level)
        
        # BEGINNER has no prerequisites
        if config.prerequisite_level is None:
            return True
        
        # Check if prerequisite level is completed
        return config.prerequisite_level in completed_levels
    
    def get_allowed_features(self, level: DifficultyLevel) -> List[str]:
        """
        Get list of allowed SQL features for a difficulty level.
        
        Args:
            level: The difficulty level
            
        Returns:
            List of allowed SQL features/keywords
        """
        config = self.get_config(level)
        
        # For higher levels, include all lower level features
        all_features = set(config.allowed_sql_features)
        
        if level == DifficultyLevel.INTERMEDIATE:
            all_features.update(
                self.get_config(DifficultyLevel.BEGINNER).allowed_sql_features
            )
        elif level == DifficultyLevel.ADVANCED:
            all_features.update(
                self.get_config(DifficultyLevel.BEGINNER).allowed_sql_features
            )
            all_features.update(
                self.get_config(DifficultyLevel.INTERMEDIATE).allowed_sql_features
            )
        elif level == DifficultyLevel.EXPERT:
            all_features.update(
                self.get_config(DifficultyLevel.BEGINNER).allowed_sql_features
            )
            all_features.update(
                self.get_config(DifficultyLevel.INTERMEDIATE).allowed_sql_features
            )
            all_features.update(
                self.get_config(DifficultyLevel.ADVANCED).allowed_sql_features
            )
        
        return sorted(list(all_features))
    
    def calculate_score(
        self,
        level: DifficultyLevel,
        time_taken: int,
        hints_used: int,
        is_correct: bool
    ) -> int:
        """
        Calculate score for a question attempt.
        
        Args:
            level: Difficulty level of the question
            time_taken: Time taken in seconds
            hints_used: Number of hints used
            is_correct: Whether answer was correct
            
        Returns:
            Calculated score (0 if incorrect)
        """
        if not is_correct:
            return 0
        
        config = self.get_config(level)
        
        # Base score
        base_score = 100 * config.scoring_multiplier
        
        # Deduct hint penalties
        hint_penalty = hints_used * config.hint_penalty_points
        
        # Time bonus
        time_bonus = 0
        if (config.time_bonus_threshold and 
            time_taken <= config.time_bonus_threshold):
            time_bonus = 50
        
        # Calculate final score
        final_score = base_score - hint_penalty + time_bonus
        
        return max(0, int(final_score))  # Ensure non-negative
    
    def get_next_level(self, current_level: DifficultyLevel) -> Optional[DifficultyLevel]:
        """
        Get the next difficulty level in progression.
        
        Args:
            current_level: Current difficulty level
            
        Returns:
            Next difficulty level or None if at max level
        """
        level_order = [
            DifficultyLevel.BEGINNER,
            DifficultyLevel.INTERMEDIATE,
            DifficultyLevel.ADVANCED,
            DifficultyLevel.EXPERT
        ]
        
        try:
            current_index = level_order.index(current_level)
            if current_index < len(level_order) - 1:
                return level_order[current_index + 1]
        except ValueError:
            pass
        
        return None
    
    def get_difficulty_summary(self) -> str:
        """
        Get a formatted summary of all difficulty levels.
        
        Returns:
            Formatted string with difficulty level information
        """
        summary = ["=" * 60]
        summary.append("SQL PRACTICE DIFFICULTY LEVELS")
        summary.append("=" * 60)
        
        for level in [DifficultyLevel.BEGINNER, DifficultyLevel.INTERMEDIATE,
                      DifficultyLevel.ADVANCED, DifficultyLevel.EXPERT]:
            config = self.get_config(level)
            summary.append(f"\n{level.name}:")
            summary.append(f"  Time Limit: {config.time_limit_seconds}s")
            summary.append(f"  Hints Available: {config.hint_count}")
            summary.append(f"  Score Multiplier: {config.scoring_multiplier}x")
            summary.append(f"  Prerequisite: {config.prerequisite_level.name if config.prerequisite_level else 'None'}")
        
        summary.append("=" * 60)
        return "\n".join(summary)


# Convenience function for quick access
def get_difficulty_config(level: DifficultyLevel) -> DifficultyConfig:
    """
    Get difficulty configuration for a level.
    
    Args:
        level: The difficulty level
        
    Returns:
        DifficultyConfig for the level
    """
    return DIFFICULTY_CONFIGS[level]


if __name__ == "__main__":
    # Demo usage
    manager = DifficultyManager()
    print(manager.get_difficulty_summary())
    
    # Example score calculation
    print("\nExample Score Calculation:")
    score = manager.calculate_score(
        level=DifficultyLevel.INTERMEDIATE,
        time_taken=300,
        hints_used=1,
        is_correct=True
    )
    print(f"Score: {score}")
