import pytest

from typing import List

from wordle.util import load_answers, load_non_answers
from wordle.simulator.answer import Answer
from wordle.strategies import StrategyFilterOnFeedback



@pytest.mark.parametrize(
    "guesses",
    [
        ['takis', 'babka'],
        ['wains', 'laxed', 'yabba'],
        ['yabba', 'wains'],
        ['aunes', 'addax', 'amrit', 'allay', 'abaca'],
    ]
)
def test_strategy_filter_on_feedback(guesses: List[str]):
    answers = load_answers()
    non_answers = load_non_answers()
    all_words = answers + non_answers

    answer = Answer('aback')

    strategy = StrategyFilterOnFeedback(all_words)

    for guess in guesses:
        strategy.wordlist = [w for w in strategy.wordlist if w != guess]
        assert answer.answer in strategy.wordlist, (answer, guess)
        feedback = answer.check_guess(guess)
        strategy.incorporate_feedback(guess, feedback)
        assert answer.answer in strategy.wordlist, (answer, guess, feedback)
