from __future__ import annotations
from abc import ABC, abstractmethod

##abc doc: https://docs.python.org/3/library/abc.html
## Interface Implementation
class process(ABC):
    """
    The Product interface declares the operations that all concrete products
    must implement.
    """

    @abstractmethod
    def operation(self) -> str:
        pass
