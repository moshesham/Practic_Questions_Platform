"""
JSON schemas for validating YAML configuration files.
"""

from jsonschema import validate, ValidationError

# Schema for config.yml
CONFIG_SCHEMA = {
    "type": "object",
    "properties": {
        "data_generation": {
            "type": "object",
            "properties": {
                "num_records": {"type": "integer", "minimum": 1, "maximum": 10000000},
                "seed": {"type": "integer", "minimum": 0},
                "table_name": {"type": "string"}
            },
            "required": ["num_records", "seed", "table_name"]
        },
        "fields": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "type": {"type": "string", "enum": ["int", "str", "bool"]},
                    "values": {
                        "oneOf": [
                            # For int type
                            {
                                "type": "object",
                                "properties": {
                                    "min": {"type": "integer"},
                                    "max": {"type": "integer"}
                                },
                                "required": ["min", "max"]
                            },
                            # For str type
                            {"type": "array", "items": {"type": "string"}},
                            # For bool type
                            {"type": "array", "items": {"type": "boolean"}}
                        ]
                    }
                },
                "required": ["name", "type", "values"]
            },
            "minItems": 1
        }
    },
    "required": ["data_generation", "fields"]
}

# Schema for questions_config.yml
QUESTIONS_CONFIG_SCHEMA = {
    "type": "object",
    "properties": {
        "questions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "difficulty": {"type": "string", "enum": ["BEGINNER", "INTERMEDIATE", "ADVANCED", "EXPERT"]},
                    "time_limit_seconds": {"type": "integer", "minimum": 1},
                    "hints_available": {"type": "integer", "minimum": 0},
                    "tags": {"type": "array", "items": {"type": "string"}},
                    "active": {"type": "boolean"},
                    "description": {"type": "string"},
                    "prerequisite_questions": {"type": "array", "items": {"type": "string"}},
                    "sql_features": {"type": "array", "items": {"type": "string"}},
                    "learning_objectives": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["name", "difficulty", "time_limit_seconds", "hints_available", "tags", "active", "description", "prerequisite_questions", "sql_features", "learning_objectives"]
            },
            "minItems": 1
        }
    },
    "required": ["questions"]
}


def validate_config(config: dict) -> None:
    """Validate config.yml against schema."""
    try:
        validate(instance=config, schema=CONFIG_SCHEMA)
    except ValidationError as e:
        raise ValueError(f"Invalid config.yml: {e.message}") from e


def validate_questions_config(config: dict) -> None:
    """Validate questions_config.yml against schema."""
    try:
        validate(instance=config, schema=QUESTIONS_CONFIG_SCHEMA)
    except ValidationError as e:
        raise ValueError(f"Invalid questions_config.yml: {e.message}") from e