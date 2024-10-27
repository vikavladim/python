import json
from typing import List


class Answer:
    """
    Class representing an answer to a question.
    """
    def __init__(self, text: str, value: int):
        """
        Constructor for Answer.

        :param text: Answer text
        :type text: str
        :param value: Answer value
        :type value: int
        """
        self.text = text
        self.value = value

    def to_dict(self):
        """
        Convert the Answer object to a dictionary.

        :return: A dictionary with 'text' and 'value' keys
        :rtype: dict
        """
        return {"text": self.text, "value": self.value}

    def __str__(self):
        """
        Return a string representation of the Answer.

        :return: A string representation of the Answer
        :rtype: str
        """
        return self.text

    def __eq__(self, other):
        """
        Check if two Answer objects are equal.

        :param other: The other Answer object
        :type other: Answer
        :return: True if the two Answer objects are equal, False otherwise
        :rtype: bool
        """
        return self.text == other.text and self.value == other.value


class Question:
    """
    Class representing a question.
    """
    def __init__(self, question: str, answers: List[Answer]):
        """
        Constructor for Question.

        :param question: Question text
        :type question: str
        :param answers: List of Answer objects
        :type answers: List[Answer]
        """
        self.question = question
        self.answers = answers

    def to_dict(self):
        """
        Convert the Question object to a dictionary.

        :return: A dictionary with 'question' and 'answers' keys
        :rtype: dict
        """
        return {"question": self.question, "answers": [a.to_dict() for a in self.answers]}

    def __str__(self):
        """
        Return a string representation of the Question.

        :return: A string representation of the Question
        :rtype: str
        """
        string = f'{self.question}:\n'
        for i, a in enumerate(self.answers):
            string += f'\t{i + 1} {a.text}\n'
        return string

    def __eq__(self, other):
        """
        Check if two Question objects are equal.

        :param other: The other Question object
        :type other: Question
        :return: True if the two Question objects are equal, False otherwise
        :rtype: bool
        """
        return self.question == other.question and self.answers == other.answers


class Questionnaire:
    """
    Class representing a questionnaire.
    """
    def __init__(self):
        """
        Constructor for Questionnaire.

        :return: A Questionnaire object
        :rtype: Questionnaire
        """
        self.questions = []

    def add_question(self, question: Question):
        """
        Add a Question object to the Questionnaire.

        :param question: The Question object to be added
        :type question: Question
        :return: None
        :rtype: None
        """
        self.questions.append(question)

    def save_to_json(self, filename: str):
        """
        Save the Questionnaire to a JSON file.

        :param filename: The name of the file to save to
        :type filename: str
        :return: None
        :rtype: None
        """
        data = {"questions": [q.to_dict() for q in self.questions]}
        try:
            with open(filename, "w") as f:
                json.dump(data, f, indent=4)

        except FileNotFoundError:
            print("Файл не найден")

    def load_from_json(self, filename: str):

        """
        Load a Questionnaire from a JSON file.

        :param filename: The name of the file to load from
        :type filename: str
        :return: None
        :rtype: None
        """
        with open(filename) as f:
            data = json.load(f)
            self.questions = []
            for q in data['questions']:
                answers = [Answer(a['text'], a['value']) for a in q['answers']]
                self.questions.append(Question(q['question'], answers))


if __name__ == "__main__":
    q = Questionnaire()

    q.add_question(
        Question("Your breathing frequency", [
            Answer('Less than 12', 0),
            Answer('12-16', 1),
            Answer('More than 12', 0),
        ]))

    q.add_question(Question("What is your pulse", [
        Answer("Less than 60", 0),
        Answer("60-70", 0),
        Answer("70-80", 1),
        Answer("80-90", 2),
        Answer("90-100", 1),
        Answer("Above 100", 0),
    ]))

    q.add_question(Question("What is your temperature", [
        Answer("Less than 35", 0),
        Answer("36-37", 2),
        Answer("37-42", 1),
        Answer("Above 42", 0),
    ]))

    q.add_question(Question("Level of skin redness", [
        Answer("White", 1),
        Answer("Red", 1),
        Answer("Green", 0),
        Answer("Orange", 1),
        Answer("Yellow", 1),
        Answer("Gray", 0),
    ]))

    q.add_question(Question("Pupil dilation in mm", [
        Answer("Less than 2", 0),
        Answer("2-8", 1),
        Answer("More than 8", 0),
    ]))

    q.add_question(
        Question("What is your height", [
            Answer("Less than 160", 0),
            Answer("160-170", 1),
            Answer("170-180", 2),
            Answer("180-190", 1),
            Answer("190-200", 0),
            Answer("Above 200", 0),
        ]))

    q.add_question(
        Question("What is your weight", [
            Answer("Less than 50", 0),
            Answer("50-60", 1),
            Answer("60-70", 2),
            Answer("70-80", 1),
            Answer("80-90", 0),
            Answer("Above 90", 0),
        ]))

    q.add_question(
        Question("What is your age", [
            Answer("Less than 20", 0),
            Answer("20-30", 1),
            Answer("30-40", 2),
            Answer("40-50", 1),
            Answer("50-60", 0),
            Answer("Above 60", 0),
        ]))

    q.add_question(
        Question("What is your foot size", [
            Answer("Less than 35", 0),
            Answer("35-40", 1),
            Answer("40-45", 1),
            Answer("Above 45", 0),
        ]))

    q.add_question(
        Question("What is your sex", [
            Answer("Male", 1),
            Answer("Female", 1),
            Answer("Other", 0),
        ]))

    # q.save_to_json("questions.json")

    # for q in q.questions:
    #     print(q)
