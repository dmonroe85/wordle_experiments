import os
from typing import List

from .types import Word

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
