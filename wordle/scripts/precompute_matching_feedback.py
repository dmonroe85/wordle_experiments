import time
import os

from joblib import Parallel, delayed

from wordle.strategies.feedback_lookup_cache import (
    FeedbackLookupCache,
    FEEDBACK_CACHE_PATH,
)
from wordle.types import Feedback, Word
from wordle.util import load_answers, load_non_answers, compute_cache_for_a_guess

os.makedirs(FEEDBACK_CACHE_PATH, exist_ok=True)

print("Precomputing the FeedbackLookupCache data")
all_words = sorted(load_answers() + load_non_answers(), key=lambda w: w.text)

# Filling up the cache and calculating cartesian scores
start_cartesian = time.time()
f_cache = compute_cache_for_a_guess(all_words)
scores = Parallel(n_jobs=-1)(delayed(f_cache)(guess) for guess in all_words)
cartesian_scores = {w.text: s for w, s in zip(all_words, scores)}
    
end_cartesian = time.time()
print(f"Time it took for cartesian: {end_cartesian - start_cartesian}")

# Calculating the cache scores
flc = FeedbackLookupCache()
cache_scores = {}
all_word_set = set([w.text for w in all_words])
start_cache = time.time()
for guess in all_words:
    cache_scores[guess.text] = flc.sizeof_largest_feedback_set(guess, all_word_set)
end_cache = time.time()
print(f"Time it took for cached: {end_cache - start_cache}")

assert cache_scores == cartesian_scores

print("Done!")