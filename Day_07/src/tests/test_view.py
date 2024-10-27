import pytest
from view import *
from creator import *


@pytest.mark.timeout(1)
def test_something_that_involves_user_input(monkeypatch):
    """
    Tests that the user can input something and the program will do something with it.

    This test will timeout if the user does not input something within 1 second.
    """
    monkeypatch.setattr('builtins.input', lambda _: '\n'.join(["Mark" for _ in range(10)]))
    questionaire = Questionnaire()
    questionaire.load_from_json("../questions.json")
    q = Quiz(questionaire)
    q.ask_questions()
    print(q.get_result())
    assert q.get_result() == "Replicant"


@pytest.mark.timeout(0.5)
def test_something_that_involves_user_input(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '\n'.join(map(str, [10 for _ in range(10)])))
    questionaire = Questionnaire()
    questionaire.load_from_json("../questions.json")
    q = Quiz(questionaire)
    q.ask_questions()
    print(q.get_result())
    assert q.get_result() == "Replicant"
