import pytest

from wordle.simulator.answer import Answer
from wordle.strategies.util import keep_after_feedback


@pytest.mark.parametrize(
    "answer,guess,word,keep",
    [
        pytest.param("ear", "ear", "ear", True, id="Perfect match"),
        pytest.param("ear", "are", "era", True, id="Permutations of matching characters"),
        pytest.param("ear", "era", "are", False, id="Permutations, but excluded by 'a'"),
        pytest.param("aa", "ab", "aa", True, id="Keep the matched word"),
        pytest.param("aback", "wains", "aback", True, id="Keep the actual answer"),
        pytest.param("aback", "yabba", "aback", True, id="Keep the actual answer"),
        pytest.param("aback", "abaca", "aback", True, id="Keep the actual answer"),
    ]
)
def test_keep_after_feedback(answer: str, guess: str, word: str, keep: bool):
    answer = Answer(answer)
    feedback = answer.check_guess(guess)
    assert keep_after_feedback(word, guess, feedback) == keep
