from typing import Protocol


class BaseBuilder(Protocol):
    config: dict

    def construct(self) -> object:
        raise NotImplementedError()
