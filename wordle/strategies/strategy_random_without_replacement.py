import random
from typing import List

from ..types import Strategy, Word


class StrategyRandomWithoutReplacement(Strategy):
    def make_guess(self) -> Word:
        return self.wordlist.pop()

    def incorporate_feedback(self, guess: Word, feedback: str):
        pass
