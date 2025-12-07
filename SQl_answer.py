from pathlib import Path
import sys
import yaml

# Add project root to Python path
project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root))

from infra.DataGenerator import DataGenerator
from infra.user import User
from infra.AnswerValidator import AnswerValidator
from infra.logging_config import LoggerManager

def main():
    # Generate initial data
    data_gen = DataGenerator(yaml_config='infra/config/config.yml')
    data_gen.generate_records()
    data_gen.write_to_csv()
    data_gen.save_to_sqlite()

    # Load questions configuration
    with open('infra/config/questions_config.yml', 'r') as f:
        questions_config = yaml.safe_load(f)

    # Demonstrate user creation and tracking
    user = User(username='student1')
    
    # Get available questions
    available_questions = user.get_available_questions('Questions')
    print("Available Questions:", available_questions)

    # Evaluate SQL answers for all active questions
    for question_config in questions_config['questions']:
        if question_config['active']:
            question_name = question_config['name']
            
            # Mark the question as active for this user session
            user.start_question(question_name)
            
            # Set up logging for this question
            logger_manager = LoggerManager(question_name=question_name)
            logger = logger_manager.create_logger("sql_evaluation")
            
            try:
                # Initialize AnswerValidator for the specific question
                validator = AnswerValidator( base_dir=project_root, question_name=question_name)

                # Log question details
                logger.info(f"Evaluating question: {question_name}")
                logger.info(f"Difficulty: {question_config['difficulty']}")
                logger.info(f"Tags: {', '.join(question_config['tags'])}")

                # Load and execute SQL query
                validator.load_sql()
                validator.execute_query()

                # Validate answer
                try:
                    is_correct = validator.validate_answer()
                    
                    # Record user's attempt
                    user.record_solution_attempt(validator.solution_df_path, is_correct)
                    
                    logger.info(f"Question {question_name} evaluation complete")
                    
                    # Print additional details
                    if is_correct:
                        logger.info("Solution is correct!")
                    else:
                        logger.warning("Solution needs improvement")
                
                except Exception as validate_error:
                    logger.error(f"Validation error for {question_name}: {validate_error}")
                    user.record_solution_attempt(validator.solution_df_path, False)

            except Exception as e:
                logger.info(f"No Active Evaluating question {question_name}: {e}")

if __name__ == "__main__":
    main()
    # # Basic usage
    # validator = AnswerValidator(question_name='sql_basic_select')
    # validator.load_sql()
    # validator.execute_query()
    # is_correct = validator.validate_answer()

    # # Print additional details
    # if is_correct:
    #     print("Solution is correct!")
    # else:
    #     print("Solution needs improvement")


    # # With custom solution file
    # validator = AnswerValidator(question_name='sql_basic_select')
    # validator.load_sql()
    # validator.execute_query()
    # is_correct = validator.validate_answer(solution_file='/path/to/custom/solution.csv')