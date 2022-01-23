from abc import ABC, abstractmethod
import random
from typing import List

from .feedback import Feedback
from .word import Word


class Strategy(ABC):

    def __init__(self, wordlist: List[Word]):
        """The wordlist is randomized for each trial, we don't need to do it
        here.
        """
        self.wordlist = wordlist[:]  # don't mutate the original

    def get_name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def make_guess(self) -> Word:
        ...

    @abstractmethod
    def incorporate_feedback(self, guess: Word, feedback: List[Feedback]):
        ...
