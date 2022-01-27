from dataclasses import dataclass
import os
from typing import Dict, Set

import ujson as json

from ..types import Feedback, Strategy, Word

FeedbackDict = Dict[str, Set[str]]
FEEDBACK_CACHE_PATH = os.path.join(os.path.dirname(__file__), 'feedback_cache')
ORDERED_CACHE_PATH = os.path.join(os.path.dirname(__file__), 'ordered_cache')


@dataclass
class FeedbackLookupCache:
    """Used to speed up these minmax algorithms.

    Data structure is:
        Guess-> Feedback -> Set(Potential Answers)
    """

    def load_feedback(self, guess: str) -> FeedbackDict:
        guess_file = os.path.join(FEEDBACK_CACHE_PATH, f"{guess}.json")
        with open(guess_file, "r") as istream:
            feedback_dict = json.load(istream)

        return {
            tuple(Feedback.from_string(feedback)): set(words)
            for feedback, words in feedback_dict.items()
        }

    def sizeof_largest_feedback_set(self, guess: Word, wordset: Set[str]) -> int:
        feedback_dict = self.load_feedback(guess.text)
        max_score = float('-inf')
        for feedback_set in feedback_dict.values():
            score = len(wordset.intersection(feedback_set))
            if score > max_score:
                max_score = score
        return max_score


@dataclass
class OrderedLookupCache:
    """Used to speed up these minmax algorithms even more because the files will
    be ordered on disk by feedback set size (descending).

    This is only possible because we don't actually need the feedback itself,
    we only need the set.
    """

    def load_feedback(self, guess: str, set_index: int) -> Set[str]:
        guess_file = os.path.join(
            ORDERED_CACHE_PATH,
            f"{guess}_{set_index}.txt",
        )
        with open(guess_file, "r") as istream:
            feedback_partition = [line.strip() for line in istream]

        return set(feedback_partition)

    def sizeof_first_feedback_set(self, guess: Word) -> int:
        return len(self.load_feedback(guess.text, set_index=0))

    def sizeof_largest_feedback_set(self, guess: Word, wordset: Set[str]) -> int:
        idx = 0
        max_size = float('-inf')
        while True:
            try:
                feedback_set = self.load_feedback(guess.text, idx)
            except FileNotFoundError:
                # Exit condition 1: we have exhausted the files for this word.
                break

            set_size = len(feedback_set)
            if set_size < max_size:
                # Exit condition 2: the full set size is strictly less than the
                # current best score.  We aren't going to do any better.
                break

            intersection_size = len(wordset.intersection(feedback_set))
            if intersection_size > max_size:
                max_size = intersection_size

            idx += 1
        return max_size