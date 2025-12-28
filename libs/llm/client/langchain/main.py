"""LangChain ChatOpenAI client wrapper for LiteLLM proxy.

This client provides ChatOpenAI instances configured to use the LiteLLM proxy,
enabling LangChain/LangGraph agents to work with any model via the proxy.
Also implements BaseLLM interface for tools that need generate/embed methods.
"""

from typing import Any, Optional

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from libs.llm.client.base import BaseLLM
from libs.logger.logger import get_logger

logger = get_logger(__name__)


class LLMClient(BaseLLM):
    """LangChain ChatOpenAI wrapper for LiteLLM proxy.

    Provides ChatOpenAI instances that work with LangChain agents and LangGraph.
    Also implements BaseLLM interface (generate/embed) for tools.
    All requests go through the LiteLLM proxy for unified model access.

    Example:
        >>> from libs.llm.client.selector import LLMClientSelector
        >>> client = LLMClientSelector.create(
        ...     provider="langchain",
        ...     proxy_url="http://litellm-proxy:4000",
        ...     api_key="sk-1234"
        ... )
        >>>
        >>> # Standard mode - for agents
        >>> chat = client.get_client(model="gpt-4", temperature=0.7)
        >>> from langchain.agents import create_agent
        >>> agent = create_agent(model=chat, tools=[...])
        >>>
        >>> # BaseLLM interface - for tools
        >>> response = client.generate(prompt="Hello")
        >>> embeddings = client.embed(["text1", "text2"])
    """

    def __init__(
        self,
        proxy_url: str = "http://litellm-proxy:4000",
        api_key: str = "sk-1234",
        default_model: str = "gpt-4",
        default_temperature: float = 0.7,
        default_max_tokens: int = 2000,
        embedding_model: Optional[str] = None,
        **kwargs,
    ):
        """Initialize LangChain ChatOpenAI client wrapper.

        Args:
            proxy_url: LiteLLM proxy URL
            api_key: API key for proxy (use dummy if auth disabled)
            default_model: Default model name from proxy config
            default_temperature: Default sampling temperature (0-1)
            default_max_tokens: Default maximum tokens in response
            embedding_model: Embedding model name (e.g., "text-embedding-3-small")
            **kwargs: Additional default parameters for ChatOpenAI
        """
        self.proxy_url = proxy_url
        self.api_key = api_key
        self.default_model = default_model
        self.default_temperature = default_temperature
        self.default_max_tokens = default_max_tokens
        self.embedding_model = embedding_model
        self.default_kwargs = kwargs

        # Create default ChatOpenAI for generate() method
        self._chat = ChatOpenAI(
            model=default_model,
            openai_api_base=proxy_url,
            openai_api_key=api_key,
            temperature=default_temperature,
            max_tokens=default_max_tokens,
        )

        # Create embeddings client if model specified
        self._embeddings = None
        if embedding_model:
            self._embeddings = OpenAIEmbeddings(
                model=embedding_model,
                openai_api_base=proxy_url,
                openai_api_key=api_key,
            )

        logger.info(
            f"ChatOpenAI client initialized (proxy={proxy_url}, model={default_model}, "
            f"embedding={embedding_model})"
        )

    def get_client(
        self,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        extra_body: Optional[dict[str, Any]] = None,
        **kwargs,
    ) -> ChatOpenAI:
        """Get ChatOpenAI instance configured for LiteLLM proxy.

        Supports two modes:
        1. Standard mode: For LangChain agents, chains, direct chat
        2. Dotprompt mode: Pass extra_body={"prompt_variables": {...}} for templates

        Args:
            model: Model name (defaults to default_model)
            temperature: Sampling temperature (defaults to default_temperature)
            max_tokens: Maximum tokens (defaults to default_max_tokens)
            extra_body: Extra body for LiteLLM (e.g., {"prompt_variables": {...}})
            **kwargs: Additional ChatOpenAI parameters

        Returns:
            Configured ChatOpenAI instance

        Examples:
            Standard mode (for agents):
            >>> chat = client.get_client(model="gpt-4", temperature=0.5)
            >>> from langchain.agents import create_agent
            >>> agent = create_agent(model=chat, tools=[...])

            Dotprompt mode (for custom templates):
            >>> chat = client.get_client(
            ...     model="rag-dotprompt",
            ...     extra_body={"prompt_variables": {"query": "What is RAG?"}}
            ... )
            >>> response = chat.invoke([])
        """
        chat_kwargs = {
            "model": model or self.default_model,
            "openai_api_base": self.proxy_url,
            "openai_api_key": self.api_key,
            "temperature": temperature
            if temperature is not None
            else self.default_temperature,
            "max_tokens": max_tokens
            if max_tokens is not None
            else self.default_max_tokens,
            **self.default_kwargs,
            **kwargs,
        }

        # Add extra_body if provided (for dotprompt mode)
        if extra_body is not None:
            chat_kwargs["extra_body"] = extra_body
            logger.debug(
                f"Creating ChatOpenAI with extra_body "
                f"(model={chat_kwargs['model']}, keys={list(extra_body.keys())})"
            )
        else:
            logger.debug(f"Creating ChatOpenAI (model={chat_kwargs['model']})")

        return ChatOpenAI(**chat_kwargs)

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs,
    ) -> str:
        """Generate text completion via LangChain ChatOpenAI.

        Implements BaseLLM interface for tools that need generate method.
        Uses the default ChatOpenAI instance created in __init__.

        Args:
            prompt: User prompt
            system_prompt: System instructions (optional)
            **kwargs: Additional parameters (ignored for compatibility)

        Returns:
            Generated text
        """
        try:
            messages = []
            if system_prompt:
                messages.append(SystemMessage(content=system_prompt))
            messages.append(HumanMessage(content=prompt))

            response = self._chat.invoke(messages)
            content = response.content

            logger.info(f"Generated (length={len(content)})")
            return content

        except Exception as e:
            logger.error(f"Generation failed: {e}", exc_info=True)
            raise

    def embed(self, texts: list[str], **kwargs) -> list[list[float]]:
        """Generate embeddings via LangChain OpenAIEmbeddings.

        Implements BaseLLM interface for tools that need embed method.

        Args:
            texts: List of texts to embed
            **kwargs: Additional parameters (ignored for compatibility)

        Returns:
            List of embedding vectors

        Raises:
            ValueError: If embedding_model is not configured
        """
        if not self._embeddings:
            raise ValueError(
                "embedding_model not set. Provide it in __init__ to use embed()"
            )

        try:
            embeddings = self._embeddings.embed_documents(texts)

            logger.info(f"Generated {len(embeddings)} embeddings")
            return embeddings

        except Exception as e:
            logger.error(f"Embedding failed: {e}", exc_info=True)
            raise
