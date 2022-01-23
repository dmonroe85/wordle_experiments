from abc import ABC, abstractmethod
import random
from typing import List

from .word import Feedback, Word


class Strategy(ABC):

    def __init__(self, wordlist: List[Word]):
        self.wordlist = wordlist[:]
        random.shuffle(self.wordlist)

    def get_name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def make_guess(self) -> Word:
        ...

    @abstractmethod
    def incorporate_feedback(self, guess: Word, feedback: List[Feedback]):
        ...
