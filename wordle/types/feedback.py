from collections import defaultdict
from enum import Enum
from typing import List

from .word import Word


CACHE = {}


class Feedback(Enum):
    # correct letter and position
    CORRECT = "C"
    # word contains this letter, but it's in the wrong place
    WRONG_POSITION = "P"
    # word does not contain this letter
    WRONG = "X"

    @staticmethod
    def calc_feedback(answer: Word, guess: Word) -> List["Feedback"]:
        """Accounts for multi-letter rules, as outlined here:
        https://nerdschalk.com/wordle-same-letter-twice-rules-explained-how-does-it-work/
        """
        statuses = []
        guess_stats = defaultdict(lambda: 0)
        wrong_position_stack = []
        for i, (a, g) in enumerate(zip(answer.text, guess.text)):
            if g == a:
                statuses.append(Feedback.CORRECT)
                if guess_stats[g] < answer.char_counts[g]:
                    guess_stats[g] += 1
                else:
                    # This will only ever happen if we reached a WRONG_POSITION
                    # and met our character limit before finding a CORRECT
                    # position.  In this case, we need to go back and override
                    # the rightmost WRONG_POSITION to be WRONG instead.
                    lookback_idx = wrong_position_stack.pop()
                    statuses[lookback_idx] = Feedback.WRONG

            elif g in answer.text and guess_stats[g] < answer.char_counts[g]:
                statuses.append(Feedback.WRONG_POSITION)
                guess_stats[g] += 1
                wrong_position_stack.append(i)
            else:
                statuses.append(Feedback.WRONG)

        return statuses

    @staticmethod
    def get_feedback(answer: Word, guess: Word) -> List["Feedback"]:
        return Feedback.calc_feedback(answer, guess)
