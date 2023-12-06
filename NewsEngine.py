# Standard
import typing

# Internal
from Engine import Engine

from CustomLogger import logger


class NewsEngine(Engine):
    def ask(self, prompt: str) -> typing.Generator[str, None, None]:
        logger.warning("Not implemented")
