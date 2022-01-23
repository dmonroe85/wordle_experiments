from dataclasses import dataclass
import random
from typing import List

from ..types import Feedback, Stats, Strategy, Word


def run_game(strategy: Strategy, answer: Word) -> Stats:
    n_guesses = 0
    feedback = [WRONG]

    while any(c is not Feedback.CORRECT for c in feedback):
        guess = strategy.make_guess()
        feedback = answer.get_feedback(guess)
        strategy.incorporate_feedback(guess, feedback)
        n_guesses += 1

    stats = Stats()
    stats.add(strategy.get_name(), n_guesses)
    return stats
