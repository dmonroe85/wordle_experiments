from typing import List

from ..types import Feedback, Strategy, Word
from .feedback_lookup_cache import OrderedLookupCache

WORD_SETS_25 = [
    ['brick', 'glent', 'jumpy', 'vozhd', 'waqfs'],
    ['bling', 'jumpy', 'treck', 'vozhd', 'waqfs'],
    ['clipt', 'jumby', 'kreng', 'vozhd', 'waqfs'],
    ['jumby', 'pling', 'treck', 'vozhd', 'waqfs'],
    ['glent', 'jumby', 'prick', 'vozhd', 'waqfs']
]


class Strategy25Characters(Strategy):
    """Inspired by the minimax method and this:
        https://bytepawn.com/optimal-coverage-for-wordle-with-monte-carlo-methods-part-iii.html

    The idea is that we can get the most information by maximizing
    letter coverage; so we choose the first 5 potential guesses that
    will cover 25 distinct letters of the alphabet.

    In order to choose from the guesses, we use minimax.

    And the wordlist pruning is done using feedback matching.
    """
    word_set_idx = None

    def __init__(self, wordlist: List[Word]):
        super().__init__(wordlist)
        self.guess_set = [
            Word(g) for g in WORD_SETS_25[self.word_set_idx]
        ]
        self.cache = OrderedLookupCache()

    def make_guess(self) -> Word:
        # If we have narrowed it down, return the answer
        if len(self.wordlist) == 1:
            return self.wordlist.pop()

        # sef of guesses is either from our guess set, or the
        # wordlist if guess set is exhausted
        guesses = self.guess_set or self.wordlist
            
        wordset = set(w.text for w in self.wordlist)
        best_guess, best_score = None, float('inf')
        for potential_guess in guesses:
            score = self.cache.sizeof_largest_feedback_set(
                potential_guess,
                wordset,
            )
            if score < best_score:
                best_guess, best_score = potential_guess, score

        return best_guess

    def incorporate_feedback(self, guess: Word, feedback: List[Feedback]):
        self.wordlist = [
            w for w in self.wordlist
            if Feedback.get_feedback(w, guess) == feedback
        ]
        self.guess_set = [
            g for g in self.guess_set
            if g.text != guess.text
        ]


class Strategy25Characters0(Strategy25Characters):
    word_set_idx = 0

class Strategy25Characters1(Strategy25Characters):
    word_set_idx = 1

class Strategy25Characters2(Strategy25Characters):
    word_set_idx = 2

class Strategy25Characters3(Strategy25Characters):
    word_set_idx = 3

class Strategy25Characters4(Strategy25Characters):
    word_set_idx = 4