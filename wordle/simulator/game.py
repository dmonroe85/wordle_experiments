from dataclasses import dataclass
import random
from typing import List

from .answer import Answer
from .feedback import *
from .stats import Stats
from ..strategies.strategy import Strategy


def run_game(strategy: Strategy, answer: Answer) -> Stats:
    n_guesses = 0
    feedback = WRONG

    while any(c != CORRECT for c in feedback):
        guess = strategy.make_guess()
        feedback = answer.check_guess(guess)
        strategy.incorporate_feedback(guess, feedback)
        n_guesses += 1

    stats = Stats()
    stats.add(strategy.get_name(), n_guesses)
    return stats
