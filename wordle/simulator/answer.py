from collections import Counter, defaultdict
from dataclasses import dataclass
import random
from typing import List

from .feedback import *


@dataclass
class Answer:
    answer: str

    def __post_init__(self):
        self.answer_stats = Counter(self.answer)

    @classmethod
    def random_answer(cls, wordlist: List[str]) -> "Answer":
        return cls(answer=random.choice(wordlist))

    def check_guess(self, guess) -> str:
        """Accounts for multi-letter rules, as outlined here:
        https://nerdschalk.com/wordle-same-letter-twice-rules-explained-how-does-it-work/
        """
        statuses = []
        guess_stats = defaultdict(lambda: 0)
        wrong_position_stack = []
        for i, (a, g) in enumerate(zip(self.answer, guess)):
            if g == a:
                statuses.append(CORRECT)
                if guess_stats[g] < self.answer_stats[g]:
                    guess_stats[g] += 1
                else:
                    # This will only ever happen if we reached a WRONG_POSITION
                    # and met our character limit before finding a CORRECT
                    # position.  In this case, we need to go back and override
                    # the WRONG_POSITION to be WRONG
                    lookback_idx = wrong_position_stack.pop()
                    statuses[lookback_idx] = WRONG

            elif g in self.answer and guess_stats[g] < self.answer_stats[g]:
                statuses.append(WRONG_POSITION)
                guess_stats[g] += 1
                wrong_position_stack.append(i)
            else:
                statuses.append(WRONG)

        feedback = ''.join(statuses)
        return feedback
