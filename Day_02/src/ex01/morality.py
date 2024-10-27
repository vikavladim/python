from collections import Counter
from abc import ABC, abstractmethod


class Player(ABC):
    def __init__(self):
        self.last_choice = None

    @abstractmethod
    def play(self):
        pass


class Cheater(Player):
    def play(self):
        return False


class Cooperator(Player):
    def play(self):
        return True


class Copycat(Player):
    def __init__(self):
        super().__init__()
        self.is_first = True

    def play(self):
        if self.is_first:
            self.is_first = False
            return True
        else:
            return self.last_choice


class Expert(Player):
    def __init__(self):
        super().__init__()
        self.is_first = True
        self.round = 0

    def play(self):
        self.round += 1
        if self.round > 8:
            return False
        if self.is_first:
            self.is_first = False
            return True
        else:
            return self.last_choice


class Grudger(Player):
    def __init__(self):
        super().__init__()
        self.was_cheat = False

    def play(self):
        if self.last_choice == False:
            self.was_cheat = True
        if not self.was_cheat:
            return True
        else:
            return False


class Detective(Player):
    def __init__(self):
        super().__init__()
        self.plays = [True, True, False, True]
        self.tactic = self.plays.pop
        self.was_cheat = False
        self.round = 0

    def play(self):
        if self.last_choice == False:
            self.was_cheat = True
        if self.round == 4:
            if self.was_cheat:
                self.tactic = self.tactic_copicat
            else:
                self.tactic = self.tactic_cheat
        self.round += 1
        return self.tactic()

    def tactic_copicat(self):
        return self.last_choice

    def tactic_cheat(self):
        return False


class Game(object):

    def __init__(self, matches=10):
        self.matches = matches
        self.registry = Counter()

    def play(self, class1, class2):
        player1, player2 = class1(), class2()
        count1, count2 = 0, 0

        for _ in range(self.matches):
            decision1 = player1.play()
            decision2 = player2.play()

            if not decision1 and not decision2:
                pass
            elif not decision1 and decision2:
                count1 += 3
                count2 += -1
            elif decision1 and not decision2:
                count1 += -1
                count2 += 3
            elif decision1 and decision2:
                count1 += 2
                count2 += 2

            player1.last_choice = decision2
            player2.last_choice = decision1

        self.registry[class1.__name__] += count1
        self.registry[class2.__name__] += count2
        # print(class1.__name__, count1, class2.__name__, count2)

    def top3(self):
        print(self.registry.most_common(3), sep='\n')


if __name__ == '__main__':
    behavior = [
        Cheater, Cooperator, Copycat, Grudger, Detective, Expert
    ]

    game = Game()

    for i in range(len(behavior)):
        for j in range(i + 1, len(behavior)):
            game.play(behavior[i], behavior[j])

    game.top3()
