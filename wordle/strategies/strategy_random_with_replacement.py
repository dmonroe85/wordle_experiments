import random
from typing import List

from ..types import Feedback, Strategy, Word


class StrategyRandomWithReplacement(Strategy):
    def make_guess(self) -> Word:
        return random.choice(self.wordlist)

    def incorporate_feedback(self, guess: Word, feedback: List[Feedback]):
        pass
