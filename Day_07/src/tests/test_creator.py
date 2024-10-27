import pytest
from creator import *

def test_answer_init():
    answer = Answer("text", 1)
    assert answer.text == "text"
    assert answer.value == 1

def test_answer_to_dict():
    answer = Answer("text", 1)
    assert answer.to_dict() == {"text": "text", "value": 1}

def test_answer_str():
    answer = Answer("text", 1)
    assert str(answer) == "text"

def test_question_init():
    answer1 = Answer("text1", 1)
    answer2 = Answer("text2", 2)
    question = Question("question", [answer1, answer2])
    assert question.question == "question"
    assert question.answers == [answer1, answer2]

def test_question_to_dict():
    answer1 = Answer("text1", 1)
    answer2 = Answer("text2", 2)
    question = Question("question", [answer1, answer2])
    assert question.to_dict() == {"question": "question", "answers": [{"text": "text1", "value": 1}, {"text": "text2", "value": 2}]}

def test_question_str():
    answer1 = Answer("text1", 1)
    answer2 = Answer("text2", 2)
    question = Question("question", [answer1, answer2])
    assert str(question) == "question:\n\t1 text1\n\t2 text2\n"

def test_questionnaire_init():
    questionnaire = Questionnaire()
    assert questionnaire.questions == []

def test_questionnaire_add_question():
    questionnaire = Questionnaire()
    answer1 = Answer("text1", 1)
    answer2 = Answer("text2", 2)
    question = Question("question", [answer1, answer2])
    questionnaire.add_question(question)
    assert questionnaire.questions == [question]

def test_questionnaire_save_to_json():
    questionnaire = Questionnaire()
    answer1 = Answer("text1", 1)
    answer2 = Answer("text2", 2)
    question = Question("question", [answer1, answer2])
    questionnaire.add_question(question)
    filename = "questions.json"
    questionnaire.save_to_json(filename)
    with open(filename) as f:
        data = json.load(f)
    assert data == {"questions": [{"question": "question", "answers": [{"text": "text1", "value": 1}, {"text": "text2", "value": 2}]}]}

def test_questionnaire_load_from_json():
    questionnaire = Questionnaire()
    answer1 = Answer("text1", 1)
    answer2 = Answer("text2", 2)
    question = Question("question", [answer1, answer2])
    filename ="questions1.json"
    data = {"questions": [
        {"question": "question",
         "answers": [
             {"text": "text1", "value": 1},
             {"text": "text2", "value": 2}
         ]}]}
    with open(filename, "w") as f:
        json.dump(data, f)
    questionnaire.load_from_json(filename)
    assert questionnaire.questions == [question]

def test_questionnaire_load_from_json_file_not_found():
    questionnaire = Questionnaire()
    with pytest.raises(FileNotFoundError):
        questionnaire.load_from_json("non_existent_file.json")

def test_questionnaire_load_from_json_invalid_json():
    questionnaire = Questionnaire()
    filename = "questions.json"
    with open(filename, "w") as f:
        f.write("invalid json")
    with pytest.raises(json.JSONDecodeError):
        questionnaire.load_from_json(filename)