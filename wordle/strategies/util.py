from typing import List

from ..types import Feedback, Word


def keep_after_feedback(list_word: Word, guess: Word, feedback: List[Feedback]) -> bool:
    keep = True
    seen_chars = set()
    for idx, (l, g, f) in enumerate(zip(list_word.text, guess.text, feedback)):
        seen_chars.add(g)
        if f is Feedback.WRONG:
            keep = keep and (g in seen_chars or g not in list_word.text)
        elif f is Feedback.WRONG_POSITION:
            keep = keep and (g in list_word.text)
        elif f is Feedback.CORRECT:
            keep = keep and (g == l)
    return keep