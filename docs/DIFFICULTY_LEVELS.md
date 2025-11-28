# SQL Difficulty Levels Specification

This document defines the difficulty level system for the SQL Practice Questions Platform, providing clear criteria for question classification and progression requirements.

## Table of Contents

1. [Overview](#overview)
2. [Difficulty Level Definitions](#difficulty-level-definitions)
3. [SQL Feature Matrix](#sql-feature-matrix)
4. [Question Requirements](#question-requirements)
5. [Scoring System](#scoring-system)
6. [Progression Rules](#progression-rules)
7. [Implementation Guide](#implementation-guide)

---

## Overview

The platform supports four difficulty levels, each with distinct SQL concepts, time limits, and scoring criteria.

```
┌─────────────┐    ┌──────────────────┐    ┌────────────┐    ┌────────┐
│  BEGINNER   │ -> │  INTERMEDIATE    │ -> │  ADVANCED  │ -> │ EXPERT │
│   Level 1   │    │     Level 2      │    │  Level 3   │    │Level 4 │
└─────────────┘    └──────────────────┘    └────────────┘    └────────┘
     ↓                     ↓                     ↓                ↓
 Basic SELECT         JOINs &            Window Functions    Complex
 WHERE, ORDER BY    Aggregations              CTEs           Analytics
```

---

## Difficulty Level Definitions

### Level 1: BEGINNER

**Target Audience:** First-time SQL learners, no prior database experience

**Learning Objectives:**
- Understand table structure and data types
- Write basic SELECT statements
- Filter data with WHERE clause
- Sort results with ORDER BY
- Limit result sets

**Typical Question Format:**
```sql
-- Simple, single-table queries
SELECT column1, column2
FROM single_table
WHERE simple_condition
ORDER BY column1
LIMIT n;
```

**Configuration:**
```yaml
difficulty: BEGINNER
time_limit_seconds: 300      # 5 minutes
hints_available: 5
score_multiplier: 1.0
ai_hint_level: explicit      # More helpful hints
```

---

### Level 2: INTERMEDIATE

**Target Audience:** Learners comfortable with basic SQL, ready for multi-table queries

**Learning Objectives:**
- Understand table relationships
- Write various types of JOINs
- Use aggregate functions
- Apply GROUP BY and HAVING
- Write subqueries

**Typical Question Format:**
```sql
-- Multi-table queries with aggregations
SELECT t1.column, COUNT(*), AVG(t2.value)
FROM table1 t1
INNER JOIN table2 t2 ON t1.id = t2.fk_id
WHERE condition
GROUP BY t1.column
HAVING COUNT(*) > n;
```

**Configuration:**
```yaml
difficulty: INTERMEDIATE
time_limit_seconds: 600      # 10 minutes
hints_available: 3
score_multiplier: 1.5
ai_hint_level: moderate
prerequisite_completion: 70%  # of BEGINNER
```

---

### Level 3: ADVANCED

**Target Audience:** Experienced SQL users ready for analytical functions

**Learning Objectives:**
- Master window functions (ROW_NUMBER, RANK, LAG, LEAD)
- Write Common Table Expressions (CTEs)
- Combine multiple advanced concepts
- Understand query optimization basics

**Typical Question Format:**
```sql
-- Window functions and CTEs
WITH ranked_data AS (
    SELECT 
        column1,
        column2,
        ROW_NUMBER() OVER (PARTITION BY column1 ORDER BY column2) as rn
    FROM table
)
SELECT *
FROM ranked_data
WHERE rn <= 3;
```

**Configuration:**
```yaml
difficulty: ADVANCED
time_limit_seconds: 900      # 15 minutes
hints_available: 2
score_multiplier: 2.0
ai_hint_level: subtle
prerequisite_completion: 80%  # of INTERMEDIATE
```

---

### Level 4: EXPERT

**Target Audience:** SQL professionals seeking mastery-level challenges

**Learning Objectives:**
- Write recursive CTEs
- Complex analytical scenarios
- Query optimization and performance
- Real-world problem-solving

**Typical Question Format:**
```sql
-- Recursive CTEs and complex analytics
WITH RECURSIVE hierarchy AS (
    SELECT id, parent_id, name, 1 as level
    FROM org_chart
    WHERE parent_id IS NULL
    
    UNION ALL
    
    SELECT o.id, o.parent_id, o.name, h.level + 1
    FROM org_chart o
    INNER JOIN hierarchy h ON o.parent_id = h.id
)
SELECT * FROM hierarchy;
```

**Configuration:**
```yaml
difficulty: EXPERT
time_limit_seconds: 1200     # 20 minutes
hints_available: 1
score_multiplier: 3.0
ai_hint_level: minimal
prerequisite_completion: 90%  # of ADVANCED
```

---

## SQL Feature Matrix

### Features by Difficulty Level

| SQL Feature | BEGINNER | INTERMEDIATE | ADVANCED | EXPERT |
|-------------|:--------:|:------------:|:--------:|:------:|
| **SELECT** |
| SELECT * | ✓ | ✓ | ✓ | ✓ |
| SELECT columns | ✓ | ✓ | ✓ | ✓ |
| Column aliases | ✓ | ✓ | ✓ | ✓ |
| DISTINCT | ✓ | ✓ | ✓ | ✓ |
| **FILTERING** |
| WHERE (basic) | ✓ | ✓ | ✓ | ✓ |
| AND/OR | ✓ | ✓ | ✓ | ✓ |
| IN/NOT IN | ✓ | ✓ | ✓ | ✓ |
| BETWEEN | ✓ | ✓ | ✓ | ✓ |
| LIKE | ✓ | ✓ | ✓ | ✓ |
| IS NULL/NOT NULL | ✓ | ✓ | ✓ | ✓ |
| **ORDERING** |
| ORDER BY | ✓ | ✓ | ✓ | ✓ |
| ASC/DESC | ✓ | ✓ | ✓ | ✓ |
| LIMIT/OFFSET | ✓ | ✓ | ✓ | ✓ |
| **JOINS** |
| INNER JOIN | | ✓ | ✓ | ✓ |
| LEFT JOIN | | ✓ | ✓ | ✓ |
| RIGHT JOIN | | ✓ | ✓ | ✓ |
| FULL OUTER JOIN | | ✓ | ✓ | ✓ |
| CROSS JOIN | | ✓ | ✓ | ✓ |
| Self JOIN | | ✓ | ✓ | ✓ |
| Multiple JOINs | | ✓ | ✓ | ✓ |
| **AGGREGATIONS** |
| COUNT | ✓ | ✓ | ✓ | ✓ |
| SUM | | ✓ | ✓ | ✓ |
| AVG | | ✓ | ✓ | ✓ |
| MIN/MAX | | ✓ | ✓ | ✓ |
| GROUP BY | | ✓ | ✓ | ✓ |
| HAVING | | ✓ | ✓ | ✓ |
| **SUBQUERIES** |
| WHERE subquery | | ✓ | ✓ | ✓ |
| FROM subquery | | ✓ | ✓ | ✓ |
| Correlated | | | ✓ | ✓ |
| EXISTS/NOT EXISTS | | ✓ | ✓ | ✓ |
| **CTEs** |
| Basic WITH | | | ✓ | ✓ |
| Multiple CTEs | | | ✓ | ✓ |
| Recursive CTE | | | | ✓ |
| **WINDOW FUNCTIONS** |
| ROW_NUMBER | | | ✓ | ✓ |
| RANK/DENSE_RANK | | | ✓ | ✓ |
| LEAD/LAG | | | ✓ | ✓ |
| FIRST_VALUE/LAST_VALUE | | | ✓ | ✓ |
| Running totals | | | ✓ | ✓ |
| PARTITION BY | | | ✓ | ✓ |
| Frame clause | | | | ✓ |
| **ADVANCED** |
| CASE expressions | | ✓ | ✓ | ✓ |
| COALESCE/NULLIF | | ✓ | ✓ | ✓ |
| Date functions | | ✓ | ✓ | ✓ |
| String functions | | ✓ | ✓ | ✓ |
| UNION/INTERSECT/EXCEPT | | ✓ | ✓ | ✓ |
| Query optimization | | | | ✓ |

---

## Question Requirements

### BEGINNER Questions (10 minimum)

```yaml
# Question template
questions:
  - name: beginner_select_all
    difficulty: BEGINNER
    tags: [select, beginner]
    time_limit_seconds: 300
    hints_available: 5
    sql_features:
      - SELECT
    learning_objectives:
      - "Understand the basic SELECT * syntax"
      - "Know how to retrieve all columns from a table"
    
  - name: beginner_select_columns
    difficulty: BEGINNER
    tags: [select, columns, beginner]
    sql_features:
      - SELECT
    learning_objectives:
      - "Select specific columns from a table"
      - "Understand column order in SELECT"
```

**Required Question Types:**
1. SELECT * (all columns)
2. SELECT specific columns
3. WHERE with equals
4. WHERE with comparison operators
5. WHERE with LIKE pattern
6. ORDER BY single column
7. ORDER BY multiple columns
8. LIMIT results
9. DISTINCT values
10. Simple COUNT(*)

---

### INTERMEDIATE Questions (15 minimum)

```yaml
questions:
  - name: intermediate_inner_join
    difficulty: INTERMEDIATE
    tags: [join, inner-join, intermediate]
    time_limit_seconds: 600
    hints_available: 3
    prerequisite_questions:
      - beginner_select_columns
      - beginner_where_equals
    sql_features:
      - SELECT
      - INNER JOIN
      - WHERE
    learning_objectives:
      - "Combine data from two related tables"
      - "Understand foreign key relationships"
```

**Required Question Types:**

*JOINs (5):*
1. Basic INNER JOIN
2. LEFT JOIN with NULL handling
3. Multiple table JOIN (3+ tables)
4. Self JOIN
5. CROSS JOIN

*Aggregations (5):*
6. GROUP BY with COUNT
7. GROUP BY with SUM
8. GROUP BY with AVG
9. HAVING clause filtering
10. Multiple aggregate functions

*Subqueries (5):*
11. Subquery in WHERE clause
12. Subquery in FROM clause (derived table)
13. Correlated subquery
14. EXISTS clause
15. IN with subquery

---

### ADVANCED Questions (10 minimum)

```yaml
questions:
  - name: advanced_row_number
    difficulty: ADVANCED
    tags: [window-function, row-number, advanced]
    time_limit_seconds: 900
    hints_available: 2
    prerequisite_questions:
      - intermediate_group_by_count
      - intermediate_inner_join
    sql_features:
      - SELECT
      - ROW_NUMBER
      - OVER
      - PARTITION BY
    learning_objectives:
      - "Assign sequential numbers to rows"
      - "Partition data for window functions"
```

**Required Question Types:**

*Window Functions (5):*
1. ROW_NUMBER() OVER()
2. RANK() vs DENSE_RANK()
3. LEAD() and LAG()
4. Running totals with SUM() OVER()
5. PARTITION BY clause

*CTEs (5):*
6. Basic WITH clause
7. Multiple CTEs in sequence
8. Basic recursive CTE (simple hierarchy)
9. CTE with window functions
10. CTE for complex aggregations

---

### EXPERT Questions (5 minimum)

```yaml
questions:
  - name: expert_recursive_hierarchy
    difficulty: EXPERT
    tags: [recursive-cte, hierarchy, expert]
    time_limit_seconds: 1200
    hints_available: 1
    prerequisite_questions:
      - advanced_basic_cte
      - advanced_row_number
    sql_features:
      - WITH RECURSIVE
      - UNION ALL
    learning_objectives:
      - "Traverse hierarchical data structures"
      - "Understand recursive query termination"
```

**Required Question Types:**
1. Recursive CTE for hierarchies
2. Complex analytical scenario (multi-step analysis)
3. Query optimization challenge
4. Real-world data modeling problem
5. Combined advanced features

---

## Scoring System

### Base Scoring Formula

```python
def calculate_score(
    difficulty: DifficultyLevel,
    time_taken: int,
    hints_used: int,
    is_correct: bool
) -> int:
    """Calculate question score based on multiple factors."""
    if not is_correct:
        return 0
    
    # Base points by difficulty
    base_points = {
        DifficultyLevel.BEGINNER: 100,
        DifficultyLevel.INTERMEDIATE: 150,
        DifficultyLevel.ADVANCED: 200,
        DifficultyLevel.EXPERT: 300
    }
    
    # Time limits by difficulty
    time_limits = {
        DifficultyLevel.BEGINNER: 300,
        DifficultyLevel.INTERMEDIATE: 600,
        DifficultyLevel.ADVANCED: 900,
        DifficultyLevel.EXPERT: 1200
    }
    
    # Hint penalties by difficulty
    hint_penalties = {
        DifficultyLevel.BEGINNER: 5,
        DifficultyLevel.INTERMEDIATE: 10,
        DifficultyLevel.ADVANCED: 20,
        DifficultyLevel.EXPERT: 40
    }
    
    score = base_points[difficulty]
    
    # Time bonus (up to 50% bonus for quick solutions)
    time_limit = time_limits[difficulty]
    if time_taken < time_limit:
        time_bonus = (time_limit - time_taken) / time_limit * 0.5
        score += int(base_points[difficulty] * time_bonus)
    
    # Hint penalty
    hint_penalty = hints_used * hint_penalties[difficulty]
    score -= hint_penalty
    
    return max(score, 10)  # Minimum 10 points for correct answer
```

### Score Breakdown Table

| Difficulty | Base Points | Max Bonus | Min Points | Time Limit |
|------------|-------------|-----------|------------|------------|
| BEGINNER | 100 | 50 | 10 | 5 min |
| INTERMEDIATE | 150 | 75 | 10 | 10 min |
| ADVANCED | 200 | 100 | 10 | 15 min |
| EXPERT | 300 | 150 | 10 | 20 min |

---

## Progression Rules

### Unlocking Next Level

```python
def can_unlock_level(
    user_progress: dict,
    target_level: DifficultyLevel
) -> bool:
    """Determine if user can unlock the next difficulty level."""
    
    requirements = {
        DifficultyLevel.INTERMEDIATE: {
            'previous_level': DifficultyLevel.BEGINNER,
            'min_completion': 0.70,  # 70% of beginner questions
            'min_score': 500
        },
        DifficultyLevel.ADVANCED: {
            'previous_level': DifficultyLevel.INTERMEDIATE,
            'min_completion': 0.80,  # 80% of intermediate questions
            'min_score': 1500
        },
        DifficultyLevel.EXPERT: {
            'previous_level': DifficultyLevel.ADVANCED,
            'min_completion': 0.90,  # 90% of advanced questions
            'min_score': 3000
        }
    }
    
    if target_level not in requirements:
        return True  # Beginner is always unlocked
    
    req = requirements[target_level]
    prev_level = req['previous_level']
    
    # Check completion percentage
    completion = calculate_completion(user_progress, prev_level)
    if completion < req['min_completion']:
        return False
    
    # Check minimum score
    total_score = calculate_total_score(user_progress, prev_level)
    if total_score < req['min_score']:
        return False
    
    return True
```

### Progression Summary

```
BEGINNER -> INTERMEDIATE:
  ✓ Complete 70% of BEGINNER questions
  ✓ Achieve minimum 500 points in BEGINNER

INTERMEDIATE -> ADVANCED:
  ✓ Complete 80% of INTERMEDIATE questions
  ✓ Achieve minimum 1500 points in INTERMEDIATE

ADVANCED -> EXPERT:
  ✓ Complete 90% of ADVANCED questions
  ✓ Achieve minimum 3000 points in ADVANCED
```

---

## Implementation Guide

### Data Models

```python
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class DifficultyLevel(Enum):
    """SQL question difficulty levels."""
    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3
    EXPERT = 4


@dataclass
class DifficultyConfig:
    """Configuration for a difficulty level."""
    level: DifficultyLevel
    time_limit_seconds: int
    max_hints: int
    base_points: int
    hint_penalty_per_use: int
    ai_hint_level: str
    prerequisite_completion: float = 0.0
    
    @classmethod
    def from_level(cls, level: DifficultyLevel) -> 'DifficultyConfig':
        """Factory method for difficulty configurations."""
        configs = {
            DifficultyLevel.BEGINNER: cls(
                level=level,
                time_limit_seconds=300,
                max_hints=5,
                base_points=100,
                hint_penalty_per_use=5,
                ai_hint_level='explicit'
            ),
            DifficultyLevel.INTERMEDIATE: cls(
                level=level,
                time_limit_seconds=600,
                max_hints=3,
                base_points=150,
                hint_penalty_per_use=10,
                ai_hint_level='moderate',
                prerequisite_completion=0.70
            ),
            DifficultyLevel.ADVANCED: cls(
                level=level,
                time_limit_seconds=900,
                max_hints=2,
                base_points=200,
                hint_penalty_per_use=20,
                ai_hint_level='subtle',
                prerequisite_completion=0.80
            ),
            DifficultyLevel.EXPERT: cls(
                level=level,
                time_limit_seconds=1200,
                max_hints=1,
                base_points=300,
                hint_penalty_per_use=40,
                ai_hint_level='minimal',
                prerequisite_completion=0.90
            )
        }
        return configs[level]


@dataclass
class Question:
    """A SQL practice question."""
    name: str
    difficulty: DifficultyLevel
    tags: List[str]
    sql_features: List[str]
    learning_objectives: List[str]
    question_text: str
    expected_solution: str
    prerequisite_questions: List[str] = field(default_factory=list)
    
    def get_config(self) -> DifficultyConfig:
        """Get difficulty configuration for this question."""
        return DifficultyConfig.from_level(self.difficulty)
```

### Updated Configuration Schema

```yaml
# config/questions_config.yml

questions:
  # Beginner questions
  - name: sql_basic_select
    difficulty: BEGINNER
    time_limit_seconds: 300
    hints_available: 5
    tags:
      - select
      - beginner
    sql_features:
      - SELECT
      - WHERE
      - ORDER BY
    learning_objectives:
      - "Write basic SELECT statements"
      - "Filter data with WHERE clause"
    active: true
    
  # Intermediate questions
  - name: sql_join_operations
    difficulty: INTERMEDIATE
    time_limit_seconds: 600
    hints_available: 3
    tags:
      - join
      - intermediate
    sql_features:
      - SELECT
      - INNER JOIN
      - LEFT JOIN
    learning_objectives:
      - "Combine data from multiple tables"
      - "Understand JOIN types"
    prerequisite_questions:
      - sql_basic_select
    active: true

# Difficulty level settings
difficulty_levels:
  BEGINNER:
    time_limit: 300
    max_hints: 5
    base_points: 100
    unlock_requirements: null
    
  INTERMEDIATE:
    time_limit: 600
    max_hints: 3
    base_points: 150
    unlock_requirements:
      previous_level: BEGINNER
      min_completion: 0.70
      min_score: 500
      
  ADVANCED:
    time_limit: 900
    max_hints: 2
    base_points: 200
    unlock_requirements:
      previous_level: INTERMEDIATE
      min_completion: 0.80
      min_score: 1500
      
  EXPERT:
    time_limit: 1200
    max_hints: 1
    base_points: 300
    unlock_requirements:
      previous_level: ADVANCED
      min_completion: 0.90
      min_score: 3000
```

---

## Summary

This specification provides a complete framework for implementing a multi-level SQL practice system with:

- Clear difficulty level definitions
- SQL feature progression path
- Comprehensive scoring system
- Fair progression requirements
- Detailed implementation guidance

AI agents implementing this system should follow the code examples and configuration schemas provided to ensure consistency across the platform.

---

*Last Updated: November 2024*
