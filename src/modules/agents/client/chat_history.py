"""Customer chat history agent for looking up chat conversations."""

from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from langchain.agents import create_agent
from langchain.tools import BaseTool
from langchain_openai import ChatOpenAI

from libs.llm.prompt_manager.base import BasePromptManager
from libs.logger.logger import get_logger
from src.modules.agents.base import BaseAgent

logger = get_logger(__name__)


class CustomerChatHistoryAgent(BaseAgent):
    """ReAct agent for looking up customer chat history.

    Uses SQLTool with PostgreSQL to query the LangGraph store table
    for conversation history.
    """

    def __init__(
        self,
        llm: ChatOpenAI,
        prompt_manager: BasePromptManager,
        tools: list[BaseTool],
        prompt_name: str = "client_chatbot_chat_history",
        prompt_label: str | None = None,
        max_iterations: int = 5,
        recursion_limit: int = 25,
    ):
        """Initialize chat history agent.

        Args:
            llm: ChatOpenAI instance.
            prompt_manager: Prompt manager for retrieving prompts.
            tools: List of tools (SQLTool with PostgreSQL).
            prompt_name: Name of the prompt in prompt manager.
            prompt_label: Label for prompt retrieval.
            max_iterations: Maximum number of ReAct iterations.
            recursion_limit: LangGraph recursion limit for invoke.
        """
        super().__init__(name="chat_history")
        self.llm = llm
        self.prompt_manager = prompt_manager
        self.tools = tools
        self.prompt_name = prompt_name
        self.prompt_label = prompt_label
        self.max_iterations = max_iterations
        self.recursion_limit = recursion_limit

        self._agent = self._build_agent()

    def _build_agent(self):
        """Build the ReAct agent."""
        prompt_obj = self.prompt_manager.get_prompt(
            self.prompt_name,
            label=self.prompt_label,
        )

        # Compile prompt with current datetime context
        tz = ZoneInfo("Asia/Bangkok")
        now = datetime.now(tz)
        system_prompt = prompt_obj.compile(
            current_datetime=now.strftime("%Y-%m-%d %H:%M"),
            timezone="Asia/Bangkok",
        )

        agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=system_prompt,
        )

        return agent

    def _extract_tool_steps(self, messages: list) -> list[dict]:
        """Extract tool calls from agent messages."""
        steps = []
        tool_calls_pending = {}

        for msg in messages:
            msg_type = getattr(msg, "type", None)

            if msg_type == "ai" and hasattr(msg, "tool_calls"):
                for tool_call in msg.tool_calls:
                    tool_calls_pending[tool_call["id"]] = {
                        "name": tool_call["name"],
                        "input": tool_call["args"],
                    }

            if msg_type == "tool":
                tool_call_id = getattr(msg, "tool_call_id", None)
                if tool_call_id and tool_call_id in tool_calls_pending:
                    step = tool_calls_pending.pop(tool_call_id)
                    step["output"] = msg.content
                    steps.append(step)

        return steps

    def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        """Execute chat history lookup.

        Args:
            state: Current state with keys:
                - translated_query: str - query in English
                - messages: list - conversation history (optional)

        Returns:
            Updated state with:
                - response: str - chat history results
                - steps: list - tool calls made during execution
        """
        query = state.get("translated_query", state.get("query", ""))
        history = state.get("messages", [])

        if not query:
            return {"response": "No query provided.", "steps": []}

        try:
            messages = self._build_messages_with_history(query, history)

            logger.debug(f"ChatHistoryAgent invoking with {len(messages)} messages")

            result = self._agent.invoke(
                {"messages": messages},
                config={"recursion_limit": self.recursion_limit},
            )

            result_messages = result.get("messages", [])
            response = ""
            if result_messages:
                last_message = result_messages[-1]
                response = getattr(last_message, "content", str(last_message))

            steps = self._extract_tool_steps(result_messages)

            logger.debug(f"ChatHistoryAgent response: {response[:100]}...")
            logger.debug(f"ChatHistoryAgent tool steps: {len(steps)}")

            return {"response": response, "steps": steps}

        except Exception as e:
            logger.error(f"ChatHistoryAgent execution failed: {e}")
            return {"response": f"Error looking up chat history: {e}", "steps": []}
