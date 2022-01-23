from dataclasses import dataclass
import random
from typing import List

from ..types import Feedback, Stats, Strategy, Word


def run_game(strategy: Strategy, answer: Word, max_guesses: int) -> Stats:
    n_guesses = 0
    feedback = [Feedback.WRONG]

    while (
        # Run one more guess than specified because it will be a huge histogram
        # bin that we can ignore
        n_guesses <= max_guesses and
        any(c is not Feedback.CORRECT for c in feedback)
    ):
        guess = strategy.make_guess()
        feedback = Feedback.get_feedback(answer, guess)
        strategy.incorporate_feedback(guess, feedback)
        n_guesses += 1

    stats = Stats()
    stats.add(strategy.get_name(), n_guesses)
    return stats
