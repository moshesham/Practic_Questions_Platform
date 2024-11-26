# infra/user.py
import json
from pathlib import Path
import uuid


class User:
    def __init__(self, base_dir=None, username=None):
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

    def load_progress(self):
        if self.user_file.exists():
            with open(self.user_file, 'r') as f:
                return json.load(f)
        return {
            'completed_questions': [],
            'attempts': {},
            'current_question': None
        }

    def save_progress(self):
        with open(self.user_file, 'w') as f:
            json.dump(self.progress, f, indent=4)

    def start_question(self, question_name):
        self.progress['current_question'] = question_name
        self.save_progress()

    def record_solution_attempt(self, solution_path, is_correct):
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

        # Mark as completed if correct
        if is_correct:
            self.progress['completed_questions'].append(self.progress['current_question'])

        self.save_progress()

    def get_available_questions(self, questions_dir):
        """
        Retrieve available questions based on configuration
        """
        questions_dir = Path(questions_dir)
        return [q.name for q in questions_dir.iterdir() if q.is_dir()]