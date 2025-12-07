# infra/user.py
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
import uuid


class User:
    def __init__(self, base_dir: Optional[Union[Path, str]] = None, username: Optional[str] = None) -> None:
        # Use the calling script's directory as base if not provided
        self.base_dir = base_dir or Path(__file__).resolve().parent.parent

        # Create users directory
        self.users_dir = self.base_dir / 'users'
        self.users_dir.mkdir(parents=True, exist_ok=True)

        # Generate or set user ID
        self.username = username or str(uuid.uuid4())
        self.user_file = self.users_dir / f"{self.username}_progress.json"

        # Initialize user progress
        self.progress = self.load_progress()

    def load_progress(self) -> Dict[str, Any]:
        if self.user_file.exists():
            with open(self.user_file, 'r') as f:
                return json.load(f)
        return {
            'completed_questions': [],
            'completed_levels': [],  # Track completed difficulty levels
            'attempts': {},
            'current_question': None,
            'total_score': 0,
            'statistics': {
                'total_attempts': 0,
                'correct_attempts': 0,
                'total_hints_used': 0,
                'total_time_seconds': 0
            }
        }

    def save_progress(self) -> None:
        with open(self.user_file, 'w') as f:
            json.dump(self.progress, f, indent=4)

    def start_question(self, question_name: str) -> None:
        self.progress['current_question'] = question_name
        self.save_progress()

    def record_solution_attempt(self, solution_path: Union[Path, str], is_correct: bool) -> None:
        if not self.progress['current_question']:
            raise ValueError("No active question")

        # Initialize attempts for current question if not exists
        if self.progress['current_question'] not in self.progress['attempts']:
            self.progress['attempts'][self.progress['current_question']] = []

        # Record attempt
        attempt = {
            'solution_path': str(solution_path),
            'is_correct': is_correct,
            'timestamp': str(datetime.now())
        }
        self.progress['attempts'][self.progress['current_question']].append(attempt)

        # Update statistics
        self.progress['statistics']['total_attempts'] += 1
        if is_correct:
            self.progress['statistics']['correct_attempts'] += 1
            
            # Mark as completed if correct (avoid duplicates)
            if self.progress['current_question'] not in self.progress['completed_questions']:
                self.progress['completed_questions'].append(self.progress['current_question'])

        self.save_progress()
    
    def update_score(self, points: int) -> None:
        """
        Update user's total score.
        
        Args:
            points: Points to add to total score
        """
        self.progress['total_score'] = self.progress.get('total_score', 0) + points
        self.save_progress()
    
    def mark_level_completed(self, difficulty_level: str) -> None:
        """
        Mark a difficulty level as completed.
        
        Args:
            difficulty_level: Name of the difficulty level (BEGINNER, INTERMEDIATE, etc.)
        """
        if 'completed_levels' not in self.progress:
            self.progress['completed_levels'] = []
        
        if difficulty_level not in self.progress['completed_levels']:
            self.progress['completed_levels'].append(difficulty_level)
            self.save_progress()
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get user statistics.
        
        Returns:
            Dictionary containing user statistics
        """
        stats = self.progress.get('statistics', {})
        total = stats.get('total_attempts', 0)
        correct = stats.get('correct_attempts', 0)
        
        return {
            'total_score': self.progress.get('total_score', 0),
            'completed_questions': len(self.progress.get('completed_questions', [])),
            'completed_levels': self.progress.get('completed_levels', []),
            'total_attempts': total,
            'correct_attempts': correct,
            'accuracy_rate': (correct / total * 100) if total > 0 else 0,
            'total_hints_used': stats.get('total_hints_used', 0),
            'total_time_seconds': stats.get('total_time_seconds', 0)
        }

    def get_available_questions(self, questions_dir: Union[Path, str]) -> List[str]:
        """
        Retrieve available questions based on configuration
        """
        questions_dir = Path(questions_dir)
        return [q.name for q in questions_dir.iterdir() if q.is_dir()]