# Standard
import typing

# External

# Internal
from LLMPoweredClass import LLMPoweredClass

from CustomLogger import logger


class Engine(LLMPoweredClass):
    def rawAskYesNo(self, prompt: str, max_retry: int = 5) -> bool | None:
        logger.debug("Asking a raw yes-no question")
        while max_retry:
            response = ""

            for token in self.rawAsk(prompt, max_new_tokens=16):
                response += token

                if len(response) >= 3:
                    if response.startswith("Yes"):
                        logger.debug("Yes responded")
                        return True
                    elif response.startswith("No"):
                        logger.debug("No responded")
                        return False
                    else:
                        break

            logger.info("Retrying YES/NO question")

            max_retry -= 1

        logger.warning("RAW ASK YES NO RETRY EXCEEDED")
