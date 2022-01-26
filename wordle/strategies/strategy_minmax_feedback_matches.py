from dataclasses import dataclass
from typing import List

from ..types import Feedback, Strategy, Word
from .feedback_lookup_cache import FeedbackLookupCache


FIRST_GUESS = "roate"


class StrategyMinMaxFeedbackMatches(Strategy):
    """A faster version of the solution from here:
        https://github.com/mrdmnd/wordle_ai/blob/main/solver.py

    This makes the tradeoff of only choosing a guess from the remaining words.
    I haven't shown it, but we may be throwing away information by not taking a
    guess from the full original list of words.
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
            best_guess, best_score = None, float('inf')
            for potential_guess in self.wordlist:
                score = self.cache.sizeof_largest_feedback_set(
                    potential_guess,
                    wordset,
                )
                if score < best_score:
                    best_guess, best_score = potential_guess, score
            return best_guess


    def incorporate_feedback(self, guess: Word, feedback: List[Feedback]):
        """Only keep the words that can possibly produce the same feedback."""
        self.wordlist = [
            w for w in self.wordlist
            if Feedback.get_feedback(w, guess) == feedback
        ]


class StrategyMinMaxFeedbackMatchesV2(Strategy):
    """The original solution from here:
        https://github.com/mrdmnd/wordle_ai/blob/main/solver.py

    TODO: This is practically intractible (I don't want to wait days for this
    to finish), so I need to see if there is another optimization I can make.
    This is slow because it ALWAYS loops through the full original list to find
    a guess.

    The idea is that there may be more information gained by including words
    that we have ruled out.
    """
    def __init__(self, wordlist):
        super().__init__(wordlist)
        self.original_list = wordlist[:]
        self.first_guess = True
        self.cache = FeedbackLookupCache()

    def make_guess(self) -> Word:
        if self.first_guess:
            guess = Word(FIRST_GUESS)
            self.wordlist.remove(guess)
            self.first_guess = False
            return guess
        else:
            wordset = set(w.text for w in self.wordlist)
            best_guess, best_score = None, float('inf')
            for potential_guess in self.original_list:
                score = self.cache.sizeof_largest_feedback_set(
                    potential_guess,
                    wordset,
                )
                if score < best_score:
                    best_guess, best_score = potential_guess, score
            return best_guess

    def incorporate_feedback(self, guess: Word, feedback: List[Feedback]):
        """Only keep the words that can possibly produce the same feedback."""
        self.wordlist = [
            w for w in self.wordlist
            if Feedback.get_feedback(w, guess) == feedback
        ]
