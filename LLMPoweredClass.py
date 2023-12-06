# Standard
import typing

# External
import ctransformers


TEMPLATE_ID = 0


PROMPT_TEMPLATES = [
    "### Prompt:\n{usrmsg}\n### Response:\n",
    "User: {usrmsg}\nAssistent: "
]

SYSTEM_TEMPLATES = [
    "### SYSTEM:\n{sysmsg}\n### Response:\n",
    "System: {sysmsg}\nAssistent: "
]

COMBINED_TEMPLATES = [
    "### Prompt:\n{usrmsg}\n### SYSTEM:\n{sysmsg}\n### Response:\n",
    "User: {usrmsg}\nSystem: {sysmsg}\nAssistent: "
]

STOP_SEQUENCES = [
    ["### Prompt:"],
    ["User:"]
]


SYSTEM_MESSAGE_TEMPLATE = SYSTEM_TEMPLATES[TEMPLATE_ID]
USER_MESSAGE_TEMPLATE = PROMPT_TEMPLATES[TEMPLATE_ID]
COMBINED_MESSAGE_TEMPLATE = COMBINED_TEMPLATES[TEMPLATE_ID]

STOP_SEQUENCE = STOP_SEQUENCES[TEMPLATE_ID]


class LLMPoweredClass:
    def __init__(self, model: ctransformers.LLM) -> None:
        self.llm = model

    def addInstruction(self, history: str, user_msg: str | None, system_msg: str | None) -> str:
        """
        Add a message from the user to the history.

        @param history: the conversation history

        @param user_msg: the message from the user to add

        @param system_msg: the system message that is enforced

        @return: the new conversation history with the user_message added with respect to the system message.
        """
        if user_msg is None:
            return history + SYSTEM_MESSAGE_TEMPLATE.replace("{sysmsg}", system_msg)
        elif system_msg is None:
            return history + USER_MESSAGE_TEMPLATE.replace("{usrmsg}", user_msg)
        else:
            return history + COMBINED_MESSAGE_TEMPLATE.replace("{sysmsg}", system_msg).replace("{usrmsg}", user_msg)

    def ask(self, prompt: str, **kwargs) -> typing.Generator[str, None, None]:
        yield from self.llm(prompt, stream=True, stop=STOP_SEQUENCE, **kwargs)
