import time
import os
from typing import Callable, Set

from joblib import Parallel, delayed

from wordle.strategies.feedback_lookup_cache import (
    FeedbackLookupCache,
    OrderedLookupCache,
    FEEDBACK_CACHE_PATH,
    ORDERED_CACHE_PATH,
)
from wordle.types import Feedback, Word
from wordle.util import (
    load_answers,
    load_non_answers,
    partition_cache_for_a_guess,
    test_cache,
)

if not os.path.isdir(FEEDBACK_CACHE_PATH):
    raise FileNotFoundError(
        f"{FEEDBACK_CACHE_PATH} doesn't exist, please run "
        "wordle.scripts.precompute_matching_feedback first."
    )

os.makedirs(ORDERED_CACHE_PATH, exist_ok=True)

print("Partitioning the cache data for OrderedFeedbackCache")
all_words = sorted(load_answers() + load_non_answers(), key=lambda w: w.text)

# Partition the cache files
start_partition = time.time()
scores = Parallel(n_jobs=-1)(
    delayed(partition_cache_for_a_guess)(guess) for guess in all_words
)
partition_scores = {w.text: s for w, s in zip(all_words, scores)}
    
end_ordered = time.time()
print(f"Time it took: {end_ordered - start_partition}")

print("Runing tests...")

print("Finding scores using FLC")
def f_test_flc() -> Callable[[Word, Set[str]], int]:
    flc = FeedbackLookupCache()
    def f(guess: Word, all_word_set: Set[str]) -> int:
        return flc.sizeof_largest_feedback_set(guess, all_word_set)
    return f
test_cache(f_test_flc(), all_words, partition_scores)

print("Finding scores using OLC")
def f_test_olc() -> Callable[[Word, Set[str]], int]:
    olc = OrderedLookupCache()
    def f(guess: Word, all_word_set: Set[str]) -> int:
        return olc.sizeof_largest_feedback_set(guess, all_word_set)
    return f
test_cache(f_test_olc(), all_words, partition_scores)

print("Finding scores using OLC, first set")
def f_test_olc_first() -> Callable[[Word, Set[str]], int]:
    olc = OrderedLookupCache()
    def f(guess: Word, all_word_set: Set[str]) -> int:
        return olc.sizeof_first_feedback_set(guess)
    return f
test_cache(f_test_olc_first(), all_words, partition_scores)


print("Done!")