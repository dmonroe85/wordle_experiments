from ..simulator.feedback import *


def keep_after_feedback(list_word: str, guess: str, feedback: str) -> bool:
    keep = True
    seen_chars = set()
    for idx, (l, g, f) in enumerate(zip(list_word, guess, feedback)):
        seen_chars.add(g)
        if f == WRONG:
            keep = keep and (g in seen_chars or g not in list_word)
        elif f == WRONG_POSITION:
            keep = keep and (g in list_word)
        elif f == CORRECT:
            keep = keep and (g == l)
    return keep