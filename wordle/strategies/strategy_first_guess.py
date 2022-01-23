from typing import List

from ..types import Feedback, Strategy, Word


class StrategyFirstGuess(Strategy):
    """Part of the implementation from here:
        https://github.com/mrdmnd/wordle_ai/blob/main/solver.py
    """
    def __init__(self, wordlist: List[Word]):
        super().__init__(wordlist)
        self.first_guess = True
        self.initial_word = None

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
    def __init__(self, wordlist: List[Word]):
        super().__init__(wordlist)
        self.initial_word = "adieu"


class StrategyFirstGuessAudio(StrategyFirstGuess):
    def __init__(self, wordlist: List[Word]):
        super().__init__(wordlist)
        self.initial_word = "audio"


class StrategyFirstGuessRoate(StrategyFirstGuess):
    def __init__(self, wordlist: List[Word]):
        super().__init__(wordlist)
        self.initial_word = "roate"


class StrategyFirstGuessRaise(StrategyFirstGuess):
    def __init__(self, wordlist: List[Word]):
        super().__init__(wordlist)
        self.initial_word = "raise"


class StrategyFirstGuessArise(StrategyFirstGuess):
    def __init__(self, wordlist: List[Word]):
        super().__init__(wordlist)
        self.initial_word = "arise"
