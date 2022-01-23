import os
from typing import List

THIS_DIR = os.path.dirname(__file__)
WORDLIST_DIR = os.path.join(THIS_DIR, os.pardir, 'wordlists')
ANSWERS_PATH = os.path.join(WORDLIST_DIR, 'answers.txt')
NON_ANSWERS_PATH = os.path.join(WORDLIST_DIR, 'non-answers.txt')


def load_list(path: str) -> List[str]:
    with open(path, 'r') as istream:
        wordlist = [l.strip() for l in istream if l.strip()]
    return wordlist


def load_answers() -> List[str]:
    answer_list = load_list(ANSWERS_PATH)
    return answer_list


def load_non_answers() -> List[str]:
    non_answer_list = load_list(NON_ANSWERS_PATH)
    return non_answer_list
