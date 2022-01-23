from abc import ABC, abstractmethod
import random
from typing import List


class Strategy(ABC):

    def __init__(self, wordlist: List[str]):
        self.wordlist = wordlist[:]
        random.shuffle(self.wordlist)

    def get_name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def make_guess(self) -> str:
        ...

    @abstractmethod
    def incorporate_feedback(self, guess: str, feedback: str):
        ...
