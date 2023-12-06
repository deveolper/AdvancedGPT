# Standard
import typing

# Standard
import os
import re

# Internal
from Engine import Engine

from CustomLogger import logger


class SummaryEngine(Engine):
    def ask(self, prompt: str) -> typing.Generator[str, None, None]:
        logger.warning("Not implemented")
