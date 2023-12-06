# Standard
import sys
import typing
import logging

# Internal
from NotesEngine import NotesEngine
from WikiEngine import WikiEngine
from NewsEngine import NewsEngine
from ComputeEngine import ComputeEngine
from SummaryEngine import SummaryEngine
from LyricsEngine import LyricsEngine
from ResponseEngine import ResponseEngine
from LLMPoweredClass import LLMPoweredClass

from CustomLogger import logger

# External
import ctransformers


class AdvancedGPT(LLMPoweredClass):
    def __init__(self, model: ctransformers.LLM) -> None:
        super().__init__(model)

    def removeExternalSources(self, prompt: str) -> str:
        logger.warning("Not implemented")
        return prompt

    
