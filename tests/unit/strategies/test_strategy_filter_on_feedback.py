import pytest

from typing import List

from wordle.util import load_answers, load_non_answers
from wordle.strategies import StrategyFilterOnFeedback
from wordle.types import Word



@pytest.mark.parametrize(
    "guess_strings",
    [
        ['takis', 'babka'],
        ['wains', 'laxed', 'yabba'],
        ['yabba', 'wains'],
        ['aunes', 'addax', 'amrit', 'allay', 'abaca'],
    ]
)
def test_strategy_filter_on_feedback(guess_strings: List[str]):
    guesses = [Word(g) for g in guess_strings]

    answers = load_answers()
    non_answers = load_non_answers()
    all_words = answers + non_answers

    answer = Word('aback')

    strategy = StrategyFilterOnFeedback(all_words)

    for guess in guesses:
        strategy.wordlist = [w for w in strategy.wordlist if w != guess]
        assert answer in strategy.wordlist, (answer, guess)
        feedback = answer.get_feedback(guess)
        strategy.incorporate_feedback(guess, feedback)
        assert answer in strategy.wordlist, (answer, guess, feedback)
