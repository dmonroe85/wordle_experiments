import random
from typing import List

from .strategy import Strategy


class StrategyRandomWithoutReplacement(Strategy):
    def make_guess(self) -> str:
        return self.wordlist.pop()

    def incorporate_feedback(self, guess: str, feedback: str):
        pass
