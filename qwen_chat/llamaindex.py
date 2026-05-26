import os
from typing import Any, AsyncGenerator, Generator, Optional, Sequence

from llama_index.core.base.llms.types import (
    ChatMessage as LlamaChatMessage,
    ChatResponse as LlamaChatResponse,
    CompletionResponse,
    CompletionResponseAsyncGen,
    CompletionResponseGen,
    LLMMetadata,
)
from llama_index.core.llms.callbacks import llm_chat_callback, llm_completion_callback
from llama_index.core.llms.llm import LLM
from pydantic import ConfigDict, Field, PrivateAttr

from .client import Qwen
from .core.types.chat import ChatMessage as QwenChatMessage
from .core.types.chat_model import ChatModel


DEFAULT_MODEL = "qwen-max-latest"


class QwenLlamaIndex(LLM):
    """LlamaIndex adapter backed by the working qwen-chat client."""

    context_window: int = Field(default=6144)
    is_chat_model: bool = Field(default=True)
    supports_function_calling: bool = Field(default=True)
    cookie: Optional[str] = Field(default=None)

    _client: Qwen = PrivateAttr()
    model_config = ConfigDict(extra="allow")

    def __init__(
        self,
        auth_token: Optional[str] = None,
        cookie: Optional[str] = None,
        model: ChatModel = DEFAULT_MODEL,
        temperature: float = 0.7,
        max_tokens: Optional[int] = 1500,
        base_url: str = "https://chat.qwen.ai",
        timeout: int = 600,
        log_level: str = "INFO",
        save_logs: bool = False,
        **kwargs: Any,
    ):
        auth_token = auth_token or os.environ.get("QWEN_AUTH_TOKEN")
        cookie = cookie or os.environ.get("QWEN_COOKIE")

        super().__init__(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            api_key=auth_token,
            **kwargs,
        )
        self.cookie = cookie
        self._client = Qwen(
            api_key=auth_token,
            cookie=cookie,
            base_url=base_url,
            timeout=timeout,
            log_level=log_level,
            save_logs=save_logs,
        )

    @classmethod
    def class_name(cls) -> str:
        return "QwenLlamaIndex"

    @property
    def metadata(self) -> LLMMetadata:
        return LLMMetadata(
            context_window=self.context_window,
            num_output=self.max_tokens or -1,
            is_chat_model=self.is_chat_model,
            model_name=self.model,
            is_function_calling_model=self.supports_function_calling,
        )

    def cancel(self) -> None:
        self._client.cancel()

    def _convert_messages(self, messages: Sequence[LlamaChatMessage]) -> list[QwenChatMessage]:
        converted = []
        for message in messages:
            role = getattr(message.role, "value", message.role)
            converted.append(QwenChatMessage(role=role, content=message.content or ""))
        return converted

    @llm_completion_callback()
    def complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        result = self.chat([LlamaChatMessage(role="user", content=prompt)], **kwargs)
        return CompletionResponse(text=result.message.content or "", raw=result.raw)

    @llm_completion_callback()
    def stream_complete(self, prompt: str, **kwargs: Any) -> CompletionResponseGen:
        response_generator = self.stream_chat(
            [LlamaChatMessage(role="user", content=prompt)], **kwargs
        )

        def gen() -> Generator[CompletionResponse, None, None]:
            for chat_response in response_generator:
                yield CompletionResponse(
                    text=chat_response.message.content or "",
                    delta=chat_response.delta,
                    raw=chat_response.raw,
                )

        return gen()

    @llm_chat_callback()
    def chat(self, messages: Sequence[LlamaChatMessage], **kwargs: Any) -> LlamaChatResponse:
        response = self._client.chat.create(
            messages=self._convert_messages(messages),
            model=kwargs.pop("model", self.model),
            stream=False,
            temperature=kwargs.pop("temperature", self.temperature),
            max_tokens=kwargs.pop("max_tokens", self.max_tokens),
            **kwargs,
        )
        content = response.choices.message.content
        return LlamaChatResponse(
            message=LlamaChatMessage(role="assistant", content=content),
            raw=response.model_dump(),
        )

    @llm_chat_callback()
    def stream_chat(
        self, messages: Sequence[LlamaChatMessage], **kwargs: Any
    ) -> Generator[LlamaChatResponse, None, None]:
        response_generator = self._client.chat.create(
            messages=self._convert_messages(messages),
            model=kwargs.pop("model", self.model),
            stream=True,
            temperature=kwargs.pop("temperature", self.temperature),
            max_tokens=kwargs.pop("max_tokens", self.max_tokens),
            **kwargs,
        )
        for chunk in response_generator:
            delta = chunk.choices[0].delta.content or ""
            content = chunk.message.content or ""
            yield LlamaChatResponse(
                message=LlamaChatMessage(role="assistant", content=content),
                delta=delta,
                raw=chunk.model_dump(),
            )

    @llm_completion_callback()
    async def acomplete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        result = await self.achat([LlamaChatMessage(role="user", content=prompt)], **kwargs)
        return CompletionResponse(text=result.message.content or "", raw=result.raw)

    @llm_completion_callback()
    async def astream_complete(self, prompt: str, **kwargs: Any) -> CompletionResponseAsyncGen:
        response_generator = await self.astream_chat(
            [LlamaChatMessage(role="user", content=prompt)], **kwargs
        )

        async def gen() -> AsyncGenerator[CompletionResponse, None]:
            async for chat_response in response_generator:
                yield CompletionResponse(
                    text=chat_response.message.content or "",
                    delta=chat_response.delta,
                    raw=chat_response.raw,
                )

        return gen()

    @llm_chat_callback()
    async def achat(
        self, messages: Sequence[LlamaChatMessage], **kwargs: Any
    ) -> LlamaChatResponse:
        response = await self._client.chat.acreate(
            messages=self._convert_messages(messages),
            model=kwargs.pop("model", self.model),
            stream=False,
            temperature=kwargs.pop("temperature", self.temperature),
            max_tokens=kwargs.pop("max_tokens", self.max_tokens),
            **kwargs,
        )
        content = response.choices.message.content
        return LlamaChatResponse(
            message=LlamaChatMessage(role="assistant", content=content),
            raw=response.model_dump(),
        )

    @llm_chat_callback()
    async def astream_chat(
        self, messages: Sequence[LlamaChatMessage], **kwargs: Any
    ) -> AsyncGenerator[LlamaChatResponse, None]:
        response_generator = await self._client.chat.acreate(
            messages=self._convert_messages(messages),
            model=kwargs.pop("model", self.model),
            stream=True,
            temperature=kwargs.pop("temperature", self.temperature),
            max_tokens=kwargs.pop("max_tokens", self.max_tokens),
            **kwargs,
        )
        async for chunk in response_generator:
            delta = chunk.choices[0].delta.content or ""
            content = chunk.message.content or ""
            yield LlamaChatResponse(
                message=LlamaChatMessage(role="assistant", content=content),
                delta=delta,
                raw=chunk.model_dump(),
            )
