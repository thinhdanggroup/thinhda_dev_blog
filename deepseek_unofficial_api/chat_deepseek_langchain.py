import asyncio
import os
from typing import Any, AsyncIterator, Dict, Iterator, List, Mapping, Optional

from dotenv import load_dotenv
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM
from langchain_core.outputs import GenerationChunk
from chat_deepseek_api.model import MessageData
from chat_deepseek_api import DeepseekAPI

class ChatDeepSeekApiLLM(LLM):
    """
    A custom chat model that uses the Chat DeepSeek API.

    This model requires parameters for authentication:
    - email: The email to use for authentication.
    - password: The password to use for authentication.
    - device_id: The device ID to use for authentication.
    - cookies: The cookies to use for authentication.
    - ds_pow_response: The DS POW Response to use for authentication.

    The model uses the Chat DeepSeek API to generate responses to prompts.
    """

    email: str = None
    password: str = None
    device_id: str = None
    cookies: str = None
    ds_pow_response: str = None
    app: DeepseekAPI = None
    chat_session_id: str = None
    message_id: int = 0

    def __init__(
        self,
        email: str,
        password: str,
        device_id: str,
        cookies: str,
        ds_pow_response: str,
    ):
        """Initialize the model.

        Args:
            email: The email to use for authentication.
            password: The password to use for authentication.
            device_id: The device ID to use for authentication.
            cookies: The cookies to use for authentication.
            ds_pow_response: The DS POW Response to use for authentication.
            **kwargs: Arbitrary additional keyword arguments.
        """
        super(ChatDeepSeekApiLLM, self).__init__()
        self.email = email
        self.password = password
        self.device_id = device_id
        self.cookies = cookies
        self.ds_pow_response = ds_pow_response
        self.app = None
        self.chat_session_id = None
        self.message_id = None

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """Run the LLM on the given input.

        Override this method to implement the LLM logic.

        Args:
            prompt: The prompt to generate from.
            stop: Stop words to use when generating. Model output is cut off at the
                first occurrence of any of the stop substrings.
                If stop tokens are not supported consider raising NotImplementedError.
            run_manager: Callback manager for the run.
            **kwargs: Arbitrary additional keyword arguments. These are usually passed
                to the model provider API call.

        Returns:
            The model output as a string. Actual completions SHOULD NOT include the prompt.
        """
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")

        self._verify_config()

        for message in self._generate_message(prompt):
            chunk = GenerationChunk(text=message)
            if run_manager:
                run_manager.on_llm_new_token(chunk.text, chunk=chunk)
        return "".join([chunk for chunk in self._generate_message(prompt)])

    def _stream(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> Iterator[GenerationChunk]:
        """Stream the LLM on the given prompt.

        This method should be overridden by subclasses that support streaming.

        If not implemented, the default behavior of calls to stream will be to
        fallback to the non-streaming version of the model and return
        the output as a single chunk.

        Args:
            prompt: The prompt to generate from.
            stop: Stop words to use when generating. Model output is cut off at the
                first occurrence of any of these substrings.
            run_manager: Callback manager for the run.
            **kwargs: Arbitrary additional keyword arguments. These are usually passed
                to the model provider API call.

        Returns:
            An iterator of GenerationChunks.
        """
        self._verify_config()

        for message in self._generate_message(prompt):
            chunk = GenerationChunk(text=message)
            if run_manager:
                run_manager.on_llm_new_token(chunk.text, chunk=chunk)
            yield chunk

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Return a dictionary of identifying parameters."""
        return {
            # The model name allows users to specify custom token counting
            # rules in LLM monitoring applications (e.g., in LangSmith users
            # can provide per token pricing for their model and monitor
            # costs for the given LLM.)
            "model_name": "CustomChatModel",
        }

    def _generate_message(self, prompt: str) -> Iterator[str]:
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(self._get_all(prompt))
        return result

    async def _get_all(self, prompt: str) -> List[str]:
        return [message async for message in self._async_generate_message(prompt)]

    async def _async_generate_message(self, prompt: str) -> AsyncIterator[str]:
        if not self.app:
            self.app = await DeepseekAPI.create(
                email=self.email,
                password=self.password,
                save_login=True,
                device_id=self.device_id,
                custom_headers={
                    "cookie": self.cookies,
                    "x-ds-pow-response": self.ds_pow_response,
                },
            )

        if not self.chat_session_id:
            self.chat_session_id = await self.app.new_chat()
            self.message_id = None

        async for chunk in self.app.chat(
            message=prompt, id=self.chat_session_id, parent_message_id=self.message_id
        ):
            chunk_data: MessageData = chunk
            yield chunk_data.choices[0].delta.content

            cur_message_id = chunk.get_message_id()
            if not cur_message_id:
                cur_message_id = 0
            if not self.message_id or cur_message_id > self.message_id:
                self.message_id = cur_message_id

    def _close(self) -> None:
        if self.app:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.app.close())

    def _verify_config(self) -> None:
        """Verify the configuration."""
        if not self.email:
            raise ValueError("Email is required.")
        if not self.password:
            raise ValueError("Password is required.")
        if not self.device_id:
            raise ValueError("Device ID is required.")
        if not self.cookies:
            raise ValueError("Cookies are required.")
        if not self.ds_pow_response:
            raise ValueError("DS POW Response is required.")

    @property
    def _llm_type(self) -> str:
        return "chat_deepseek_api"


if __name__ == "__main__":
    load_dotenv()
    email = os.environ.get("DEEPSEEK_EMAIL")
    password = os.environ.get("DEEPSEEK_PASSWORD")
    device_id = os.environ.get("DEEPSEEK_DEVICE_ID")
    cookies = os.environ.get("DEEPSEEK_COOKIES")
    ds_pow_response = os.environ.get("DEEPSEEK_DS_POW_RESPONSE")

    model = ChatDeepSeekApiLLM(
        email=email,
        password=password,
        device_id=device_id,
        cookies=cookies,
        ds_pow_response=ds_pow_response,
    )
    result = model.invoke("who are you")
    print(result)
    result = model.invoke("what can you do")
    print(result)

    model._close()
