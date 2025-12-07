"""
Tests for difficulty level system
"""

import pytest
from infra.difficulty import (
    DifficultyLevel,
    DifficultyConfig,
    DifficultyManager,
    DIFFICULTY_CONFIGS,
    get_difficulty_config
)


class TestDifficultyLevel:
    """Tests for DifficultyLevel enum."""
    
    def test_difficulty_levels_exist(self):
        """Test all difficulty levels are defined."""
        assert DifficultyLevel.BEGINNER
        assert DifficultyLevel.INTERMEDIATE
        assert DifficultyLevel.ADVANCED
        assert DifficultyLevel.EXPERT
    
    def test_from_string_valid(self):
        """Test converting valid strings to difficulty levels."""
        assert DifficultyLevel.from_string('beginner') == DifficultyLevel.BEGINNER
        assert DifficultyLevel.from_string('INTERMEDIATE') == DifficultyLevel.INTERMEDIATE
        assert DifficultyLevel.from_string('Advanced') == DifficultyLevel.ADVANCED
        assert DifficultyLevel.from_string('EXPERT') == DifficultyLevel.EXPERT
    
    def test_from_string_invalid(self):
        """Test converting invalid string raises error."""
        with pytest.raises(ValueError):
            DifficultyLevel.from_string('invalid')
    
    def test_string_representation(self):
        """Test string representation of difficulty levels."""
        assert str(DifficultyLevel.BEGINNER) == 'Beginner'
        assert str(DifficultyLevel.INTERMEDIATE) == 'Intermediate'


class TestDifficultyConfig:
    """Tests for DifficultyConfig dataclass."""
    
    def test_create_valid_config(self):
        """Test creating valid difficulty config."""
        config = DifficultyConfig(
            level=DifficultyLevel.BEGINNER,
            time_limit_seconds=300,
            hint_count=5,
            allowed_sql_features=['SELECT', 'FROM'],
            scoring_multiplier=1.0
        )
        
        assert config.level == DifficultyLevel.BEGINNER
        assert config.time_limit_seconds == 300
        assert config.hint_count == 5
        assert len(config.allowed_sql_features) == 2
        assert config.scoring_multiplier == 1.0
    
    def test_invalid_time_limit(self):
        """Test that negative time limit raises error."""
        with pytest.raises(ValueError):
            DifficultyConfig(
                level=DifficultyLevel.BEGINNER,
                time_limit_seconds=-1,
                hint_count=5,
                allowed_sql_features=['SELECT'],
                scoring_multiplier=1.0
            )
    
    def test_invalid_hint_count(self):
        """Test that negative hint count raises error."""
        with pytest.raises(ValueError):
            DifficultyConfig(
                level=DifficultyLevel.BEGINNER,
                time_limit_seconds=300,
                hint_count=-1,
                allowed_sql_features=['SELECT'],
                scoring_multiplier=1.0
            )
    
    def test_invalid_scoring_multiplier(self):
        """Test that zero or negative multiplier raises error."""
        with pytest.raises(ValueError):
            DifficultyConfig(
                level=DifficultyLevel.BEGINNER,
                time_limit_seconds=300,
                hint_count=5,
                allowed_sql_features=['SELECT'],
                scoring_multiplier=0
            )


class TestPredefinedConfigs:
    """Tests for predefined difficulty configurations."""
    
    def test_all_levels_have_configs(self):
        """Test that all difficulty levels have predefined configs."""
        assert DifficultyLevel.BEGINNER in DIFFICULTY_CONFIGS
        assert DifficultyLevel.INTERMEDIATE in DIFFICULTY_CONFIGS
        assert DifficultyLevel.ADVANCED in DIFFICULTY_CONFIGS
        assert DifficultyLevel.EXPERT in DIFFICULTY_CONFIGS
    
    def test_beginner_config(self):
        """Test beginner configuration."""
        config = DIFFICULTY_CONFIGS[DifficultyLevel.BEGINNER]
        
        assert config.level == DifficultyLevel.BEGINNER
        assert config.time_limit_seconds == 300
        assert config.hint_count == 5
        assert config.prerequisite_level is None
        assert 'SELECT' in config.allowed_sql_features
    
    def test_intermediate_prerequisites(self):
        """Test intermediate level has beginner prerequisite."""
        config = DIFFICULTY_CONFIGS[DifficultyLevel.INTERMEDIATE]
        
        assert config.prerequisite_level == DifficultyLevel.BEGINNER
        assert config.scoring_multiplier > 1.0
    
    def test_difficulty_progression(self):
        """Test that difficulty increases progressively."""
        beginner = DIFFICULTY_CONFIGS[DifficultyLevel.BEGINNER]
        intermediate = DIFFICULTY_CONFIGS[DifficultyLevel.INTERMEDIATE]
        advanced = DIFFICULTY_CONFIGS[DifficultyLevel.ADVANCED]
        expert = DIFFICULTY_CONFIGS[DifficultyLevel.EXPERT]
        
        # Time limits increase
        assert beginner.time_limit_seconds < intermediate.time_limit_seconds
        assert intermediate.time_limit_seconds < advanced.time_limit_seconds
        assert advanced.time_limit_seconds < expert.time_limit_seconds
        
        # Hint counts decrease
        assert beginner.hint_count > intermediate.hint_count
        assert intermediate.hint_count > advanced.hint_count
        assert advanced.hint_count > expert.hint_count
        
        # Scoring multipliers increase
        assert beginner.scoring_multiplier < intermediate.scoring_multiplier
        assert intermediate.scoring_multiplier < advanced.scoring_multiplier
        assert advanced.scoring_multiplier < expert.scoring_multiplier


class TestDifficultyManager:
    """Tests for DifficultyManager class."""
    
    @pytest.fixture
    def manager(self):
        """Create a difficulty manager for testing."""
        return DifficultyManager()
    
    def test_get_config(self, manager):
        """Test getting config for a level."""
        config = manager.get_config(DifficultyLevel.BEGINNER)
        assert config.level == DifficultyLevel.BEGINNER
    
    def test_get_config_invalid(self, manager):
        """Test getting config for invalid level raises error."""
        # This shouldn't happen with enum, but test the error handling
        manager.configs = {}
        with pytest.raises(KeyError):
            manager.get_config(DifficultyLevel.BEGINNER)
    
    def test_validate_progression_beginner(self, manager):
        """Test that beginner level has no prerequisites."""
        assert manager.validate_progression(
            DifficultyLevel.BEGINNER,
            set()
        )
    
    def test_validate_progression_intermediate_pass(self, manager):
        """Test intermediate unlocked after completing beginner."""
        assert manager.validate_progression(
            DifficultyLevel.INTERMEDIATE,
            {DifficultyLevel.BEGINNER}
        )
    
    def test_validate_progression_intermediate_fail(self, manager):
        """Test intermediate locked without beginner."""
        assert not manager.validate_progression(
            DifficultyLevel.INTERMEDIATE,
            set()
        )
    
    def test_validate_progression_advanced(self, manager):
        """Test advanced level progression."""
        assert manager.validate_progression(
            DifficultyLevel.ADVANCED,
            {DifficultyLevel.BEGINNER, DifficultyLevel.INTERMEDIATE}
        )
        
        assert not manager.validate_progression(
            DifficultyLevel.ADVANCED,
            {DifficultyLevel.BEGINNER}
        )
    
    def test_get_allowed_features_beginner(self, manager):
        """Test getting allowed features for beginner."""
        features = manager.get_allowed_features(DifficultyLevel.BEGINNER)
        
        assert 'SELECT' in features
        assert 'FROM' in features
        assert 'WHERE' in features
    
    def test_get_allowed_features_cumulative(self, manager):
        """Test that higher levels include lower level features."""
        beginner_features = set(manager.get_allowed_features(DifficultyLevel.BEGINNER))
        intermediate_features = set(manager.get_allowed_features(DifficultyLevel.INTERMEDIATE))
        
        # Intermediate should include all beginner features
        assert beginner_features.issubset(intermediate_features)
    
    def test_calculate_score_correct(self, manager):
        """Test score calculation for correct answer."""
        score = manager.calculate_score(
            level=DifficultyLevel.BEGINNER,
            time_taken=150,  # Under 180 second threshold for bonus
            hints_used=0,
            is_correct=True
        )
        
        # Base score (100 * 1.0) + time bonus (50) - hints (0) = 150
        assert score == 150
    
    def test_calculate_score_incorrect(self, manager):
        """Test that incorrect answers get zero score."""
        score = manager.calculate_score(
            level=DifficultyLevel.BEGINNER,
            time_taken=100,
            hints_used=0,
            is_correct=False
        )
        
        assert score == 0
    
    def test_calculate_score_with_hints(self, manager):
        """Test score calculation with hints used."""
        score = manager.calculate_score(
            level=DifficultyLevel.BEGINNER,
            time_taken=100,
            hints_used=3,
            is_correct=True
        )
        
        # Base (100) + time bonus (50) - hints (3*5=15) = 135
        assert score == 135
    
    def test_calculate_score_slow_completion(self, manager):
        """Test score without time bonus for slow completion."""
        score = manager.calculate_score(
            level=DifficultyLevel.BEGINNER,
            time_taken=250,  # Over bonus threshold
            hints_used=0,
            is_correct=True
        )
        
        # Base (100) + no time bonus = 100
        assert score == 100
    
    def test_calculate_score_intermediate(self, manager):
        """Test score calculation for intermediate level."""
        score = manager.calculate_score(
            level=DifficultyLevel.INTERMEDIATE,
            time_taken=300,
            hints_used=1,
            is_correct=True
        )
        
        # Base (100 * 2.0 = 200) + time bonus (50) - hints (1*10=10) = 240
        assert score == 240
    
    def test_get_next_level(self, manager):
        """Test getting next level in progression."""
        assert manager.get_next_level(DifficultyLevel.BEGINNER) == DifficultyLevel.INTERMEDIATE
        assert manager.get_next_level(DifficultyLevel.INTERMEDIATE) == DifficultyLevel.ADVANCED
        assert manager.get_next_level(DifficultyLevel.ADVANCED) == DifficultyLevel.EXPERT
        assert manager.get_next_level(DifficultyLevel.EXPERT) is None
    
    def test_get_difficulty_summary(self, manager):
        """Test getting difficulty summary."""
        summary = manager.get_difficulty_summary()
        
        assert 'BEGINNER' in summary
        assert 'INTERMEDIATE' in summary
        assert 'ADVANCED' in summary
        assert 'EXPERT' in summary
        assert 'Time Limit' in summary
        assert 'Hints Available' in summary


class TestConvenienceFunctions:
    """Tests for module-level convenience functions."""
    
    def test_get_difficulty_config(self):
        """Test get_difficulty_config convenience function."""
        config = get_difficulty_config(DifficultyLevel.BEGINNER)
        assert config.level == DifficultyLevel.BEGINNER
