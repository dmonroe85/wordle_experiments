from collections import defaultdict
import os
from typing import Callable, Dict, List, Set
import time

import ujson as json

from .strategies.feedback_lookup_cache import (
    FEEDBACK_CACHE_PATH,
    ORDERED_CACHE_PATH,
)
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


def partition_cache_for_a_guess(guess: Word) -> int:
    print(f"Partitioning feedback for word {guess}")
    input_file_name = os.path.join(FEEDBACK_CACHE_PATH, f"{guess.text}.json")
    with open(input_file_name, 'r') as istream:
        feedback_lookup = json.load(istream)

    ordered_partitions = sorted(feedback_lookup.values(), key=len, reverse=True)

    for idx, part in enumerate(ordered_partitions):
        output_file_name = os.path.join(
            ORDERED_CACHE_PATH,
            f"{guess.text}_{idx}.txt",
        )
        with open(output_file_name, 'w') as ostream:
            # Dedupe and order the partition words
            ostream.write('\n'.join(sorted(set(part))))
    return len(ordered_partitions[0])


def test_cache(
    f_get_cache: Callable[[Word, Set[str]], int],
    all_words: Set[Word],
    expected_scores: Dict[str, int]
):
    all_word_set = set([w.text for w in all_words])

    start = time.time()
    scores = {
        guess.text: f_get_cache(guess, all_word_set) for guess in all_words
    }
    end = time.time()
    print(f"Time it took: {end - start}")

    assert scores == expected_scores