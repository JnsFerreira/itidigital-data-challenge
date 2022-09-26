from typing import Protocol


class BaseBuilder(Protocol):
    """
    Base builder class to be used as reference to concrete builder

    You can implement as many other methods as you like to help build the class

    Args:
        config (dict): Class configuration as dictionary
    """
    config: dict

    def construct(self) -> object:
        """
        This method should be implemented on concrete class and must be able
        to construct your class instance
        """
        raise NotImplementedError()
