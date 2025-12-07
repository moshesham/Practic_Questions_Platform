"""
Tests for User management system
"""

import pytest
import json
from pathlib import Path
from infra.user import User


class TestUser:
    """Tests for User class."""
    
    @pytest.fixture
    def temp_user_dir(self, tmp_path):
        """Create temporary user directory."""
        return tmp_path / "users"
    
    @pytest.fixture
    def user(self, temp_user_dir):
        """Create a test user."""
        return User(base_dir=temp_user_dir.parent, username="test_user")
    
    def test_user_creation(self, user):
        """Test user is created with default progress."""
        assert user.username == "test_user"
        assert user.progress['completed_questions'] == []
        assert user.progress['completed_levels'] == []
        assert user.progress['total_score'] == 0
        assert 'statistics' in user.progress
    
    def test_user_file_creation(self, user):
        """Test that user file is created after saving progress."""
        # File is created lazily when progress is saved
        user.save_progress()
        assert user.user_file.exists()
    
    def test_start_question(self, user):
        """Test starting a question."""
        user.start_question("sql_basic_select")
        assert user.progress['current_question'] == "sql_basic_select"
    
    def test_record_correct_attempt(self, user):
        """Test recording a correct solution attempt."""
        user.start_question("sql_basic_select")
        user.record_solution_attempt("path/to/solution.sql", is_correct=True)
        
        assert "sql_basic_select" in user.progress['completed_questions']
        assert user.progress['statistics']['total_attempts'] == 1
        assert user.progress['statistics']['correct_attempts'] == 1
        assert len(user.progress['attempts']['sql_basic_select']) == 1
    
    def test_record_incorrect_attempt(self, user):
        """Test recording an incorrect solution attempt."""
        user.start_question("sql_basic_select")
        user.record_solution_attempt("path/to/solution.sql", is_correct=False)
        
        assert "sql_basic_select" not in user.progress['completed_questions']
        assert user.progress['statistics']['total_attempts'] == 1
        assert user.progress['statistics']['correct_attempts'] == 0
    
    def test_record_attempt_without_active_question(self, user):
        """Test that recording attempt without active question raises error."""
        with pytest.raises(ValueError):
            user.record_solution_attempt("path/to/solution.sql", is_correct=True)
    
    def test_multiple_attempts_same_question(self, user):
        """Test multiple attempts on same question."""
        user.start_question("sql_basic_select")
        user.record_solution_attempt("attempt1.sql", is_correct=False)
        user.record_solution_attempt("attempt2.sql", is_correct=False)
        user.record_solution_attempt("attempt3.sql", is_correct=True)
        
        assert len(user.progress['attempts']['sql_basic_select']) == 3
        assert user.progress['statistics']['total_attempts'] == 3
        assert user.progress['statistics']['correct_attempts'] == 1
        # Should only appear once in completed questions
        assert user.progress['completed_questions'].count('sql_basic_select') == 1
    
    def test_update_score(self, user):
        """Test updating user score."""
        user.update_score(100)
        assert user.progress['total_score'] == 100
        
        user.update_score(50)
        assert user.progress['total_score'] == 150
        
        user.update_score(-25)
        assert user.progress['total_score'] == 125
    
    def test_mark_level_completed(self, user):
        """Test marking difficulty level as completed."""
        user.mark_level_completed('BEGINNER')
        assert 'BEGINNER' in user.progress['completed_levels']
        
        # Should not add duplicates
        user.mark_level_completed('BEGINNER')
        assert user.progress['completed_levels'].count('BEGINNER') == 1
    
    def test_get_statistics(self, user):
        """Test getting user statistics."""
        user.start_question("q1")
        user.record_solution_attempt("sol1.sql", is_correct=True)
        user.update_score(100)
        user.mark_level_completed('BEGINNER')
        
        stats = user.get_statistics()
        
        assert stats['total_score'] == 100
        assert stats['completed_questions'] == 1
        assert stats['completed_levels'] == ['BEGINNER']
        assert stats['total_attempts'] == 1
        assert stats['correct_attempts'] == 1
        assert stats['accuracy_rate'] == 100.0
    
    def test_accuracy_rate_calculation(self, user):
        """Test accuracy rate is calculated correctly."""
        user.start_question("q1")
        user.record_solution_attempt("sol1.sql", is_correct=False)
        user.record_solution_attempt("sol2.sql", is_correct=True)
        
        user.start_question("q2")
        user.record_solution_attempt("sol3.sql", is_correct=False)
        
        stats = user.get_statistics()
        
        assert stats['total_attempts'] == 3
        assert stats['correct_attempts'] == 1
        assert abs(stats['accuracy_rate'] - 33.33) < 0.1
    
    def test_accuracy_rate_no_attempts(self, user):
        """Test accuracy rate is 0 when no attempts."""
        stats = user.get_statistics()
        assert stats['accuracy_rate'] == 0
    
    def test_save_and_load_progress(self, temp_user_dir):
        """Test that progress is saved and can be loaded."""
        user1 = User(base_dir=temp_user_dir.parent, username="persistent_user")
        user1.start_question("sql_basic_select")
        user1.record_solution_attempt("sol.sql", is_correct=True)
        user1.update_score(150)
        user1.mark_level_completed('BEGINNER')
        
        # Create new user instance with same username
        user2 = User(base_dir=temp_user_dir.parent, username="persistent_user")
        
        # Progress should be loaded from file
        assert user2.progress['current_question'] == "sql_basic_select"
        assert user2.progress['total_score'] == 150
        assert 'BEGINNER' in user2.progress['completed_levels']
        assert 'sql_basic_select' in user2.progress['completed_questions']
    
    def test_get_available_questions(self, user, tmp_path):
        """Test getting available questions."""
        # Create mock questions directory
        questions_dir = tmp_path / "Questions"
        questions_dir.mkdir()
        
        (questions_dir / "q1").mkdir()
        (questions_dir / "q2").mkdir()
        (questions_dir / "q3").mkdir()
        
        available = user.get_available_questions(questions_dir)
        
        assert len(available) == 3
        assert "q1" in available
        assert "q2" in available
        assert "q3" in available
    
    def test_user_progress_file_format(self, user):
        """Test that user progress file is valid JSON."""
        user.start_question("test_q")
        user.record_solution_attempt("sol.sql", is_correct=True)
        user.update_score(100)
        
        # Read the file and verify it's valid JSON
        with open(user.user_file, 'r') as f:
            data = json.load(f)
        
        assert 'completed_questions' in data
        assert 'attempts' in data
        assert 'current_question' in data
        assert 'total_score' in data
        assert 'statistics' in data
        assert 'completed_levels' in data
