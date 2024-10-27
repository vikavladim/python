from creator import *

class Quiz:
    def __init__(self, questionnaire: Questionnaire):
        """
        Initialize the Quiz with a questionnaire.

        :param questionnaire: The questionnaire to be used for the quiz.
        :type questionnaire: Questionnaire
        """
        self.questionnaire = questionnaire
        self.score = 0

    def ask_questions(self):
        """
        Asks all the questions in the questionnaire and updates the score.

        Asks all the questions in the questionnaire and updates the score
        accordingly. The user is asked to input the number of the answer
        they want to choose. The input is validated to ensure it is a
        number and in the correct range.

        The score is updated by the value of the answer. If the answer
        is correct, the score is increased by the value of the answer.
        If the answer is incorrect, the score is decreased by the value
        of the answer.

        :return: None
        :rtype: None
        """
        for i, q in enumerate(self.questionnaire.questions):
            while True:
                print(f"Вопрос {i + 1}: {q}")
                answer_number = input("Введите номер ответа: ")
                try:
                    answer_number = int(answer_number)
                    if 1 <= answer_number <= len(q.answers):
                        self.score += q.answers[answer_number - 1].value
                        break
                    else:
                        print("Неправильный номер ответа")
                except ValueError:
                    print("Неправильный формат ответа")


    def get_result(self):
        """
        Gets the result of the quiz.

        If the score is greater than 7, the quiz returns 'Human'.
        Otherwise, it returns 'Replicant'.

        :return: The result of the quiz.
        :rtype: str
        """
        if self.score >7:
            return 'Human'
        else:
            return 'Replicant'
