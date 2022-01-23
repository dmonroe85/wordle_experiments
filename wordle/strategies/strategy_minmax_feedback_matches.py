from collections import Counter, defaultdict
from typing import List

from ..types import Feedback, Strategy, Word


class StrategyMinMaxFeedbackMatches(Strategy):
    """The full solution from here:
        https://github.com/mrdmnd/wordle_ai/blob/main/solver.py
    """
    def __init__(self, wordlist):
        super().__init__(wordlist)
        self.first_guess = True

    def make_guess(self) -> Word:
        if self.first_guess:
            # Hack to avoid getting stuck in a giant loop
            # According to the github repo, this is the optimal first guess
            guess = Word("arise")
            self.wordlist.remove(guess)
            self.first_guess = False
            return guess
        else:
            best_guess, best_score = None, float('inf')
            for potential_guess in self.wordlist:
                feedback_counts = defaultdict(lambda: 0)
                for potential_answer in self.wordlist:
                    feedback = tuple(
                        Feedback.get_feedback(potential_answer, potential_guess)
                    )
                    feedback_counts[feedback] += 1

                score = max(feedback_counts.values())
                if score < best_score:
                    best_guess, best_score = potential_guess, score
            return best_guess


    def incorporate_feedback(self, guess: Word, feedback: List[Feedback]):
        self.wordlist = [
            w for w in self.wordlist
            if Feedback.get_feedback(w, guess) == feedback
        ]