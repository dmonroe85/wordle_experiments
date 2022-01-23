from collections import Counter
from typing import List

from ..types import Feedback, Strategy, Word


class StrategyMaxCharacterFrequency(Strategy):
    def make_guess(self) -> Word:
        char_counts = Counter(''.join([w.text for w in self.wordlist]))
        self.wordlist.sort(
            key=lambda word: sum(char_counts[c] for c in word.text),
            reverse=False,
        )
        return self.wordlist.pop()

    def incorporate_feedback(self, guess: Word, feedback: List[Feedback]):
        self.wordlist = [
            w for w in self.wordlist
            if Feedback.get_feedback(w, guess) == feedback
        ]