from collections import defaultdict
import os
from typing import Callable, List

import ujson as json

from .strategies.feedback_lookup_cache import FEEDBACK_CACHE_PATH
from .types import Feedback, Word

THIS_DIR = os.path.dirname(__file__)
WORDLIST_DIR = os.path.join(THIS_DIR, os.pardir, 'wordlists')
ANSWERS_PATH = os.path.join(WORDLIST_DIR, 'answers.txt')
NON_ANSWERS_PATH = os.path.join(WORDLIST_DIR, 'non-answers.txt')


def load_list(path: str) -> List[Word]:
    with open(path, 'r') as istream:
        wordlist = [Word(l.strip()) for l in istream if l.strip()]
    return wordlist


def load_answers() -> List[Word]:
    answer_list = load_list(ANSWERS_PATH)
    return answer_list


def load_non_answers() -> List[Word]:
    non_answer_list = load_list(NON_ANSWERS_PATH)
    return non_answer_list


def compute_cache_for_a_guess(all_words: List[Word]) -> Callable[[Word], int]:
    def f(guess: Word) -> int:
        print(f"Analyzing word {guess}")
        feedback_lookup = defaultdict(list)
        feedback_scores = defaultdict(lambda: 0)
        for answer in all_words:
            feedback = Feedback.to_string(Feedback.get_feedback(answer, guess))
            feedback_lookup[feedback].append(answer.text)
            feedback_scores[feedback] += 1
        score = max(feedback_scores.values())

        file_name = os.path.join(FEEDBACK_CACHE_PATH, f"{guess.text}.json")
        with open(file_name, 'w') as ostream:
            json.dump(dict(feedback_lookup), ostream)

        return score
    return f