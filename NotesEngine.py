# Standard
import re
import typing
import os

# Internal
from Engine import Engine

from CustomLogger import logger


class NotesEngine(Engine):
    def ask(self, prompt: str) -> typing.Generator[str, None, None]:
        logger.warning("Not implemented")

    def fetchNotes(self, prompt: str) -> str:
        logger.warning("Not implemented")
