from creator import *
from view import *

if __name__ == "__main__":
    q = Questionnaire()
    q.load_from_json("questions.json")
    quiz = Quiz(q)
    quiz.ask_questions()
    print(f"\n\n\nВаш результат: {quiz.get_result()}" )