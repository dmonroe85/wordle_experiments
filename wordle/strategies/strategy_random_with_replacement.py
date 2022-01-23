import random

from .strategy import Strategy


class StrategyRandomWithReplacement(Strategy):
    def make_guess(self) -> str:
        return random.choice(self.wordlist)

    def incorporate_feedback(self, guess: str, feedback: str):
        pass
