from __future__ import annotations
from abc import ABC, abstractmethod
##abc doc: https://docs.python.org/3/library/abc.html

class processCreator(ABC):
    """
    The Creator class declares the factory method that is supposed to return an
    object of a Product class. The Creator's subclasses usually provide the
    implementation of this method.
    """
    @abstractmethod
    def factory_method(self):
        """
        Note that the Creator may also provide some default implementation of
        the factory method.
        """
        pass

    def some_operation(self) -> str:

        # Call the factory method to create a Product object.
        process = self.factory_method()

        # Now, use the process.
        result = f"Creator: The same creator's code has just worked with {process.operation()}"

        return result