import sys
from typing import Any, Optional, List
from uuid import UUID

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.outputs import LLMResult
from tenacity import RetryCallState
from logger import logger
from llm import count_tokens

class StreamTokenHandler:
    def __init__(self, llm: BaseChatModel):
        self.llm = llm
        self.output = ""

    @staticmethod
    def _parse_message(messages: List[BaseMessage]) -> str:
        output = ""
        for message in messages:
            if message.content:
                output += message.content
        return output

    def __call__(self, messages: List[BaseMessage], debug:bool = True) -> str:
        if debug:
            log_msg= self._parse_message(messages)
            logger.info(f"\033[31m****StreamTokenHandler****\n%s\033[0m \nTotal tokens: {count_tokens(log_msg)} \n", log_msg    )

        for chunk in self.llm.stream(messages):
            content = chunk.content
            self.output += content
        if debug:
            logger.info(f"\033[31m****StreamTokenHandler output****\n%s\033[0m \n Token output tokens: {count_tokens(self.output)} \n", self.output)
        return self.output
