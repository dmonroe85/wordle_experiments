from typing import List

from ..types import Feedback, Strategy, Word
from .feedback_lookup_cache import OrderedLookupCache


FIRST_GUESS = "serai"


class StrategySmallestFeedbackPartition(Strategy):
    """This is effectively the same as StrategyMinmaxFeedbackMatches, but it's
    more explicit about what it's doing and is therefore able to be implemented
    more efficiently.

    The reason the minmax strategy works is because the feedback set for a
    guess gives a mutually exclusive subset of potential answers.  In order
    to minimize our guesses, we need to reduce the answer space by the greatest
    amount on every turn.  In order to do this, we evaluate every potential
    guess and find the corresponding largest feedback set; and out of those
    max-sets, we pick the minimum.  This minimizes risk and prunes the space
    by the greatest amount.

    We can take advantage of this fact and structure our file-cache in such a
    way that we order the feedback sets by size on-disk.  This makes efficient
    lookup faster, and it makes iteration on the full list more tractable.
    """
    def __init__(self, wordlist):
        super().__init__(wordlist)
        self.first_guess = True
        self.cache = OrderedLookupCache()

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


class StrategySmallestFeedbackPartitionV2(Strategy):
    """This is the same as V1, but it iterates over the entire original
    wordlist instead of being restricted to the answer list.
    """
    def __init__(self, wordlist):
        super().__init__(wordlist)
        self.first_guess = True
        self.cache = OrderedLookupCache()
        self.original_list = wordlist[:]

    def make_guess(self) -> Word:
        if self.first_guess:
            # Make a first guess to avoid getting stuck in a giant loop
            guess = Word(FIRST_GUESS)
            self.wordlist.remove(guess)
            self.first_guess = False
            return guess
        else:
            wordset = set(w.text for w in self.original_list)
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
