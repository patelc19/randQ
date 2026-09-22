import random
import time

import streamlit as st

from randq.selector import rand_draw, rand_draw_no_repeat

st.title("Random Question Picker")

if "names" not in st.session_state:
    st.session_state.names = []
if "questions" not in st.session_state:
    st.session_state.questions = []
if "used_names" not in st.session_state:
    st.session_state.used_names = set()
if "used_questions" not in st.session_state:
    st.session_state.used_questions = set()
if "current_pick" not in st.session_state:
    st.session_state.current_pick = None


def add_name():
    if st.session_state.new_name.strip():
        st.session_state.names.append(st.session_state.new_name.strip())
        st.session_state.new_name = ""


def add_question():
    if st.session_state.new_question.strip():
        st.session_state.questions.append(st.session_state.new_question.strip())
        st.session_state.new_question = ""


col1, col2 = st.columns(2)

with col1:
    st.subheader("Names")
    st.text_input("Add a name", key="new_name")
    st.button("Add name", on_click=add_name)

with col2:
    st.subheader("Questions")
    st.text_input("Add a question", key="new_question")
    st.button("Add question", on_click=add_question)

col1, col2 = st.columns(2)
with col1:
    st.write(st.session_state.names)
with col2:
    st.write(st.session_state.questions)

no_repeats = st.checkbox("No repeats within this session")

names = st.session_state.names
questions = st.session_state.questions
# exhausted pools (with no-repeats on) disable the button instead of erroring
pool_exhausted = no_repeats and (
    not [n for n in names if n not in st.session_state.used_names]
    or not [q for q in questions if q not in st.session_state.used_questions]
)

draw_disabled = not names or not questions or pool_exhausted
if pool_exhausted:
    st.warning("All names or questions have been used. Uncheck 'No repeats' or add more.")

if st.button("Draw", disabled=draw_disabled):
    placeholder = st.empty()
    rng = random.Random()
    for _ in range(30):
        placeholder.write(f"{random.choice(names)}, please answer: {random.choice(questions)}")
        time.sleep(0.1)

    if no_repeats:
        chosen_name, chosen_question = rand_draw_no_repeat(
            names, questions, rng, st.session_state.used_names, st.session_state.used_questions
        )
        st.session_state.used_names.add(chosen_name)
        st.session_state.used_questions.add(chosen_question)
    else:
        chosen_name, chosen_question = rand_draw(names, questions, rng)

    placeholder.empty()
    st.session_state.current_pick = (chosen_name, chosen_question)

if st.session_state.current_pick is not None:
    chosen_name, chosen_question = st.session_state.current_pick
    st.success(f"{chosen_name}, please answer: {chosen_question}")
