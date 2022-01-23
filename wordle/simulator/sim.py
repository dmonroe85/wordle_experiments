from typing import Callable, Iterable, List, Type

from .answer import Answer
from .game import run_game
from .stats import Stats
from ..strategies import Strategy
from ..util import load_answers, load_non_answers


def build_runners(
    strategy_classes: List[Type[Strategy]],
    n_iterations: int,
) -> Iterable[Callable[[], Stats]]:
    answer_list = load_answers()
    non_answers = load_non_answers()
    full_wordlist = answer_list + non_answers

    for answer in answer_list:
        answer = Answer(answer)
        print(answer)
        for _ in range(n_iterations):
            for strategy_class in strategy_classes:
                strategy = strategy_class(full_wordlist)
                yield runner(strategy, answer)


def runner(strategy: Strategy, answer: Answer) -> Callable[[], Stats]:
    def run() -> Stats:
        game_stats = run_game(strategy, answer)
        return game_stats

    return run
