from typing import List

from ..types import Feedback, Strategy, Word


class StrategyFirstGuess(Strategy):
    initial_word = None

    def __init__(self, wordlist: List[Word]):
        super().__init__(wordlist)
        self.first_guess = True

    def make_guess(self) -> Word:
        if self.first_guess:
            guess = Word(self.initial_word)
            self.wordlist.remove(guess)
            self.first_guess = False
            return guess
        else:
            return self.wordlist.pop()

    def incorporate_feedback(self, guess: Word, feedback: List[Feedback]):
        self.wordlist = [
            w for w in self.wordlist
            if Feedback.get_feedback(w, guess) == feedback
        ]


class StrategyFirstGuessAdieu(StrategyFirstGuess):
    initial_word = "adieu"


class StrategyFirstGuessAudio(StrategyFirstGuess):
    initial_word = "audio"


class StrategyFirstGuessRoate(StrategyFirstGuess):
    initial_word = "roate"


class StrategyFirstGuessRaise(StrategyFirstGuess):
    initial_word = "raise"


class StrategyFirstGuessArise(StrategyFirstGuess):
    initial_word = "arise"


class StrategyFirstGuessBoozy(StrategyFirstGuess):
    initial_word = "boozy"


class StrategyFirstGuessGypsy(StrategyFirstGuess):
    initial_word = "gypsy"


class StrategyFirstGuessSerai(StrategyFirstGuess):
    initial_word = "serai"


class StrategyFirstGuessSoare(StrategyFirstGuess):
    initial_word = "soare"
