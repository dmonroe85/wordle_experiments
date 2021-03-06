from typing import List

from ..types import Feedback, Strategy, Word


class StrategyMatchedFeedback(Strategy):
    """Part of the implementation from here:
        https://github.com/mrdmnd/wordle_ai/blob/main/solver.py
    """
    def make_guess(self) -> Word:
        return self.wordlist.pop()

    def incorporate_feedback(self, guess: Word, feedback: List[Feedback]):
        """Only keep the words that can possibly produce the same feedback."""
        self.wordlist = [
            w for w in self.wordlist
            if Feedback.get_feedback(w, guess) == feedback
        ]
