import streamlit as st
from infra.DataGenerator import DataGenerator
from infra.AnswerValidator import AnswerValidator
from infra.user import User
import pandas as pd
import yaml
from pathlib import Path

st.set_page_config(page_title="SQL Practice Platform", layout="wide")
st.title("SQL Practice Platform")

# Load questions config
def load_questions():
    with open("infra/config/questions_config.yml", "r") as f:
        return yaml.safe_load(f)["questions"]

questions = load_questions()
question_names = [q["name"] for q in questions if q["active"]]

selected_question = st.selectbox("Select a question:", question_names)

st.write("### Question Details")
for q in questions:
    if q["name"] == selected_question:
        st.write(f"**Difficulty:** {q['difficulty']}")
        st.write(f"**Description:** {q['description']}")
        st.write(f"**Tags:** {', '.join(q['tags'])}")
        break

st.write("---")

st.write("### Enter your SQL answer below:")
user_sql = st.text_area("SQL Query", height=200)

if st.button("Submit Answer"):
    # Generate data if not present
    data_gen = DataGenerator(yaml_config="infra/config/config.yml")
    data_gen.generate_records()
    data_gen.write_to_csv()
    data_gen.save_to_sqlite()

    validator = AnswerValidator(question_name=selected_question)
    validator.query = user_sql
    try:
        validator.execute_query()
        result_df = validator.answer_df
        st.write("#### Query Result:")
        st.dataframe(result_df)
        # Validate against solution
        is_correct = validator.validate_answer()
        if is_correct:
            st.success("Your answer is correct!")
        else:
            st.error("Your answer is incorrect. Please try again.")
    except Exception as e:
        st.error(f"Error: {e}")
