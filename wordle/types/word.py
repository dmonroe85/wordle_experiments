from collections import Counter, defaultdict
from dataclasses import dataclass
import random
from typing import List

from .feedback import Feedback


@dataclass
class Word:
    text: str

    def __post_init__(self):
        self.stats = Counter(self.text)

    def get_feedback(self, guess: "Word") -> List[Feedback]:
        """Accounts for multi-letter rules, as outlined here:
        https://nerdschalk.com/wordle-same-letter-twice-rules-explained-how-does-it-work/
        """
        statuses = []
        guess_stats = defaultdict(lambda: 0)
        wrong_position_stack = []
        for i, (a, g) in enumerate(zip(self.text, guess.text)):
            if g == a:
                statuses.append(Feedback.CORRECT)
                if guess_stats[g] < self.stats[g]:
                    guess_stats[g] += 1
                else:
                    # This will only ever happen if we reached a WRONG_POSITION
                    # and met our character limit before finding a CORRECT
                    # position.  In this case, we need to go back and override
                    # the rightmost WRONG_POSITION to be WRONG instead.
                    lookback_idx = wrong_position_stack.pop()
                    statuses[lookback_idx] = Feedback.WRONG

            elif g in self.text and guess_stats[g] < self.stats[g]:
                statuses.append(Feedback.WRONG_POSITION)
                guess_stats[g] += 1
                wrong_position_stack.append(i)
            else:
                statuses.append(Feedback.WRONG)

        return statuses
