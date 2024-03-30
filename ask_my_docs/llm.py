from enum import StrEnum
import os
from typing import Optional

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_openai import AzureChatOpenAI
from langchain_openai import ChatOpenAI
import tiktoken

from langchain_community.chat_models.ollama import ChatOllama

class LLMType(StrEnum):
    AZURE = "azure"
    GEMINI = "gemini"
    OPEN_ROUTER = "open_router"
    BING_CHAT = "bing_chat"
    OLLAMA = "ollama"
    
class ModelConfig:
    def __init__(self, llm_type: str = "azure"):
        self.llm_type = llm_type
        prefix = llm_type.upper() + "_"
        self.deployment = os.getenv(prefix+"MODEL_CONFIG_DEPLOYMENT", "")
        self.version = os.getenv(prefix+"MODEL_CONFIG_VERSION","")
        self.base = os.getenv(prefix+"MODEL_CONFIG_BASE","")
        self._key1 = os.getenv(prefix+"MODEL_CONFIG_KEY","")
        self._key2 = os.getenv(prefix+"MODEL_CONFIG_KEY2", self._key1)
        self._keys = [self._key1, self._key2]
        self._current_index = 0

    @property
    def key(self):
        current_key = self._keys[self._current_index]
        self._current_index = (self._current_index + 1) % len(self._keys)
        return current_key


def new_model_config(deployment:str, llm_type:str = LLMType.GEMINI ) -> ModelConfig:
    cfg = ModelConfig(llm_type=llm_type)
    cfg.deployment = deployment
    return cfg


def create_chat_model(
        temperature: float,
        model_config: ModelConfig,
        stream_callback_manager: BaseCallbackHandler = None,
        verbose: bool = True,
        max_tokens: Optional[int] = None,
        n: int = 1,
        callbacks: Optional[list] = None,
) -> BaseChatModel :
    streaming = stream_callback_manager is not None
    if callbacks is None:
        callbacks = []

    if stream_callback_manager:
        callbacks.append(stream_callback_manager)

    if model_config.llm_type == LLMType.AZURE:
        return AzureChatOpenAI(
            openai_api_version=model_config.version,
            openai_api_base=model_config.base,
            openai_api_key=model_config.key,
            deployment_name=model_config.deployment,
            temperature=temperature,
            streaming=streaming,
            callbacks=callbacks,
            max_tokens=max_tokens,
            verbose=verbose,
            n=n,
        )
    elif model_config.llm_type == LLMType.OPEN_ROUTER:
        return ChatOpenAI(
            openai_api_base=model_config.base,
            openai_api_key=model_config.key,
            model_name=model_config.deployment,
        )
    elif model_config.llm_type == LLMType.OLLAMA:
        return ChatOllama(
            streaming=streaming,
            model=model_config.deployment,
            callbacks=callbacks,
        )
    else:
        return ChatGoogleGenerativeAI(
            google_api_key=model_config.key,
            model=model_config.deployment,
            temperature=temperature,
            streaming=streaming,
            callbacks=callbacks,
            max_tokens=max_tokens,
            verbose=verbose,
            n=n,
            convert_system_message_to_human=True,
            max_output_tokens=2000,
        )

def count_tokens(tokens: str) -> int:
    enc = tiktoken.encoding_for_model("gpt-4")
    total = len(enc.encode(tokens))
    return total

def create_embedding_model() -> GoogleGenerativeAIEmbeddings:
    gemini_embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY")
        )
    return gemini_embeddings