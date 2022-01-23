import random

from ..simulator.feedback import *
from .strategy import Strategy
from .util import keep_after_feedback


class StrategyFilterOnFeedback(Strategy):
    def make_guess(self) -> str:
        return self.wordlist.pop()

    def incorporate_feedback(self, guess: str, feedback: str):
        self.wordlist = [
            w for w in self.wordlist
            if keep_after_feedback(w, guess, feedback)
        ]

