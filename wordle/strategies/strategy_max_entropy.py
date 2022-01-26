from dataclasses import dataclass
from typing import List

from ..types import Feedback, Strategy, Word
from .feedback_lookup_cache import FeedbackLookupCache


FIRST_GUESS = "roate"


class StrategyMaxEntropy(Strategy):
    """When we make a guess, we need to balance two things:
    1. The ability to match the word
    2. The ability to prune our guesses

    One way to do that is to find the maximum entropy guess, whose feedback
    matches are closest to 50% of the remaining words.
    """
    def __init__(self, wordlist):
        super().__init__(wordlist)
        self.first_guess = True
        self.cache = FeedbackLookupCache()

    def make_guess(self) -> Word:
        if self.first_guess:
            # Make a first guess to avoid getting stuck in a giant loop
            guess = Word(FIRST_GUESS)
            self.wordlist.remove(guess)
            self.first_guess = False
            return guess
        else:
            wordset = set(w.text for w in self.wordlist)
            target = len(wordset) / 2.0
            best_guess, best_score = None, float('inf')
            for potential_guess in self.wordlist:
                size = self.cache.sizeof_largest_feedback_set(
                    potential_guess,
                    wordset,
                )
                score = abs(target - size)
                if score < best_score:
                    best_guess, best_score = potential_guess, score
            return best_guess


    def incorporate_feedback(self, guess: Word, feedback: List[Feedback]):
        """Only keep the words that can possibly produce the same feedback."""
        self.wordlist = [
            w for w in self.wordlist
            if Feedback.get_feedback(w, guess) == feedback
        ]
