from pathlib import Path
import sys

# Add project root to Python path
project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root))

from infra.DataGenerator import DataGenerator
from infra.user import User

def main():
    # Generate initial data
    data_gen = DataGenerator(yaml_config='config/config.yml')
    data_gen.generate_records()
    data_gen.write_to_csv()
    data_gen.save_to_sqlite()

    # Demonstrate user creation and tracking
    user = User(username='student1')
    available_questions = user.get_available_questions('Questions')
    print("Available Questions:", available_questions)

if __name__ == "__main__":
    main()