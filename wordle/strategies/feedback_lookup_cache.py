from dataclasses import dataclass
import os
from typing import Dict, Set

import ujson as json

from ..types import Feedback, Strategy, Word

FeedbackDict = Dict[str, Set[str]]
FEEDBACK_CACHE_PATH = os.path.join(os.path.dirname(__file__), 'feedback_cache')


@dataclass
class FeedbackLookupCache:
    """Used to speed up these minmax algorithms.

    Intended data structure is:
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