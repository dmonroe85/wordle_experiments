import pytest

from wordle.types import Feedback, Word


# feedback codes are defined in wordle.simulator.feedback
@pytest.mark.parametrize(
    "answer,guess,feedback_string",
    [
        pytest.param(
            "abbey",
            "algae",
            "CXXXP",
            id="A is correct, second A is wrong, E is in in wrong place",
        ),
        pytest.param(
            "abbey",
            "keeps",
            "XPXXX",
            id="E is in the wrong spot, second E is wrong",
        ),
        pytest.param(
            "abbey",
            "orbit",
            "XXCXX",
            id="B is in the right spot",
        ),
        pytest.param(
            "abbey",
            "abate",
            "CCXXP",
            id="AB are correct, second A should be wrong, E is in the wrong spot",
        ),
        pytest.param(
            "abbey",
            "abbey",
            "CCCCC",
            id="match",
        ),
        pytest.param(
            "abbey",
            "bubba",
            "PXCXP",
            id="Third B is wrong",
        ),
        pytest.param(
            "elate",
            "eerie",
            "CXXXC",
            id="This will require a lookback and correction",
        ),
    ]
)
def test_word(answer: str, guess: str, feedback_string: str):
    feedback = Feedback.from_string(feedback_string)
    assert Feedback.get_feedback(Word(answer), Word(guess)) == feedback