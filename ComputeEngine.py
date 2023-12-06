# Standard
import re
import io
import sys

# Internal
import typing
from Engine import Engine
from CustomLogger import logger


class ComputeEngine(Engine):
    def ask(self, prompt: str) -> typing.Generator[str, None, None]:
        logger.warning("Not implemented")

    def compute(self, script: str) -> str:
        if any(k in script for k in [
            "import",
            "exec",
            "eval",
            "open",
            "input",
            "__builtins__",
            "globals"
        ]):
            return "Script was not trusted and therefore did not run."

        logger.debug(f"Running: {script}")

        output_stream = io.StringIO()

        old_stdout = sys.stdout

        sys.stdout = output_stream

        exec(script)

        sys.stdout = old_stdout

        logger.debug("Finished.")

        logger.debug(output_stream.getvalue())

        return output_stream.getvalue()
