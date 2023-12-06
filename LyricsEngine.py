# Standard
import typing
import os
import io
import sys
import re

# Internal
from Engine import Engine
from CachedGenius import CachedGenius
from MinimalSongData import MinimalSongData
from Artist import Artist

from CustomLogger import logger

# External
import lyricsgenius
import dotenv
import ctransformers


class LyricsEngine(Engine):
    def __init__(self, model: ctransformers.LLM, forceOffline: bool):
        dotenv.load_dotenv("keys.env")
        GENIUS_ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")

        genius = lyricsgenius.Genius(GENIUS_ACCESS_TOKEN)
        self.genius = CachedGenius.loadFromCache(genius, forceOffline)
        self.llm = model

    def ask(self, prompt: str) -> typing.Generator[str, None, None]:
        logger.warning("Not implemented")
