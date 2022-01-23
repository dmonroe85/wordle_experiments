import pytest

from wordle.strategies.util import keep_after_feedback
from wordle.types import Feedback, Word


@pytest.mark.parametrize(
    "answer_string,guess_string,word_string,keep",
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
def test_keep_after_feedback(answer_string: str, guess_string: str, word_string: str, keep: bool):
    answer = Word(answer_string)
    guess = Word(guess_string)
    list_word = Word(word_string)
    feedback = Feedback.get_feedback(answer, guess)
    assert keep_after_feedback(list_word, guess, tuple(feedback)) == keep
