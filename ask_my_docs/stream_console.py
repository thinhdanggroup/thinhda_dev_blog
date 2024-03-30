import sys
from typing import Any, Optional
from uuid import UUID

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult
from tenacity import RetryCallState


class StreamConsoleCallbackManager(BaseCallbackHandler):
    output = ""

    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        sys.stdout.write(token)
        self.output += token

    def on_llm_end(
            self,
            response: LLMResult,
            *,
            run_id: UUID,
            parent_run_id: Optional[UUID] = None,
            **kwargs: Any,
    ) -> None:
        sys.stdout.write("\n\n")
        sys.stdout.write("========================================\n")

    def on_retry(
            self,
            retry_state: RetryCallState,
            *,
            run_id: UUID,
            **kwargs: Any,
    ) -> None:
        sys.stdout.write("\n\n")
        sys.stdout.write("========================================\n")
        sys.stdout.write("Retry: {}\n".format(retry_state))
        sys.stdout.write("========================================\n")
        sys.stdout.write("\n\n")