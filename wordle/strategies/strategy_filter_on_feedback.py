from typing import List

from ..types import Feedback, Strategy, Word
from .util import keep_after_feedback


class StrategyFilterOnFeedback(Strategy):
    def make_guess(self) -> Word:
        return self.wordlist.pop()

    def incorporate_feedback(self, guess: Word, feedback: List[Feedback]):
        self.wordlist = [
            w for w in self.wordlist
            if keep_after_feedback(w, guess, feedback)
        ]
