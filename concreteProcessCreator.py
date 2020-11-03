from processCreator import *

class concreteProcessCreator(Creator):
    """
    Note that the signature of the method still uses the abstract product type,
    even though the concrete product is actually returned from the method. This
    way the Creator can stay independent of concrete product classes.
    """
    def factory_method(self) -> process:
        return concreteProcessCreator()

    