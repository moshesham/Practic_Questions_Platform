---
name: AI Agent Content Creation Task
about: Template for delegating SQL question and content creation tasks to AI agents
title: '[AI-CONTENT] '
labels: 'ai-agent-task, content'
assignees: ''
---

## Content Task

**Task ID:** TASK-XXX
**Content Type:** SQL Questions | Documentation | Examples
**Difficulty Level:** Beginner | Intermediate | Advanced | Expert
**Estimated Time:** X hours

---

## Description

<!-- Describe the content to be created -->

---

## Content Specifications

### SQL Questions (if applicable)

**Number of questions to create:** X

**Topics to cover:**
- [ ] Topic 1
- [ ] Topic 2
- [ ] Topic 3

**Each question must include:**
1. `question.txt` - Problem description
2. `example_solution.sql` - Reference SQL solution
3. `solutions/solution_df.csv` - Expected output data
4. `metadata.yml` - Question metadata

---

## Question Template

```yaml
# metadata.yml structure
difficulty: BEGINNER | INTERMEDIATE | ADVANCED | EXPERT
time_limit_seconds: 300
hints_available: 5
tags:
  - sql
  - topic_tag
prerequisite_questions: []
sql_features:
  - SELECT
  - WHERE
learning_objectives:
  - Objective 1
  - Objective 2
```

---

## Quality Requirements

- [ ] Questions have clear, unambiguous descriptions
- [ ] Solutions are correct and optimized
- [ ] Expected outputs are accurate
- [ ] Metadata is complete
- [ ] Progressive difficulty within level
- [ ] Real-world relevance where possible

---

## Database Schema Reference

<!-- Provide schema context for question creation -->

```sql
-- Available tables and columns
CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    department_id INTEGER,
    salary DECIMAL(10,2)
);

-- Add other relevant tables
```

---

## Sample Question Format

### Question File (`question.txt`)
```
[Question Title]

Write a SQL query to:
1. [Requirement 1]
2. [Requirement 2]
3. [Requirement 3]

Expected output columns:
- column1
- column2

Constraints:
- [Any specific constraints]

Hints:
- [Optional starter hint]
```

### Solution File (`example_solution.sql`)
```sql
-- Clear, well-commented solution
SELECT column1, column2
FROM table_name
WHERE condition
ORDER BY column1;
```

---

## AI Agent Instructions

1. **Review** the database schema and existing questions
2. **Create** questions following the template structure
3. **Ensure** progressive difficulty within the level
4. **Validate** solutions against the test database
5. **Write** clear, educational problem descriptions
6. **Include** learning objectives in metadata
7. **Test** all solutions produce correct output

---

## Acceptance Criteria

- [ ] All specified questions created
- [ ] Complete folder structure for each question
- [ ] Solutions validated and correct
- [ ] Metadata complete and accurate
- [ ] Questions follow difficulty guidelines
- [ ] Educational value is clear

---

## Notes

<!-- Additional context for content creation -->
