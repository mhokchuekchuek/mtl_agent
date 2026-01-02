"""Product agent for handling product-related queries using ReAct pattern."""

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


class ProductAgent(BaseAgent):
    """ReAct agent for product queries.

    Uses LangChain v1 create_agent to dynamically decide which tools to use
    for product search, recommendations, comparisons, and stock queries.
    """

    def __init__(
        self,
        llm: ChatOpenAI,
        prompt_manager: BasePromptManager,
        tools: list[BaseTool],
        prompt_name: str = "product_agent",
        prompt_label: str | None = None,
        max_iterations: int = 5,
    ):
        """Initialize product agent.

        Args:
            llm: ChatOpenAI instance from LLMClient.get_client().
            prompt_manager: Prompt manager for retrieving prompts.
            tools: List of tools available to the agent.
            prompt_name: Name of the prompt in prompt manager.
            prompt_label: Label for prompt retrieval (e.g., "latest", "production").
            max_iterations: Maximum number of ReAct iterations. Default 5.
        """
        super().__init__(name="products")
        self.llm = llm
        self.prompt_manager = prompt_manager
        self.tools = tools
        self.prompt_name = prompt_name
        self.prompt_label = prompt_label
        self.max_iterations = max_iterations

        # Build the agent
        self._agent = self._build_agent()

    def _build_agent(self):
        """Build the ReAct agent.

        Returns:
            Configured agent.
        """
        # Get system prompt from prompt manager
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

        # Create agent using LangChain v1 API
        agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=system_prompt,
        )

        return agent

    def _extract_tool_steps(self, messages: list) -> list[dict]:
        """Extract tool calls from agent messages.

        Args:
            messages: List of messages from agent execution.

        Returns:
            List of tool step dicts with name, input, output.
        """
        steps = []
        tool_calls_pending = {}

        for msg in messages:
            msg_type = getattr(msg, "type", None)

            # AIMessage with tool_calls
            if msg_type == "ai" and hasattr(msg, "tool_calls"):
                for tool_call in msg.tool_calls:
                    tool_calls_pending[tool_call["id"]] = {
                        "name": tool_call["name"],
                        "input": tool_call["args"],
                    }

            # ToolMessage with result
            if msg_type == "tool":
                tool_call_id = getattr(msg, "tool_call_id", None)
                if tool_call_id and tool_call_id in tool_calls_pending:
                    step = tool_calls_pending.pop(tool_call_id)
                    step["output"] = msg.content
                    steps.append(step)

        return steps

    def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        """Execute product query using ReAct agent.

        Args:
            state: Current state with keys:
                - query: str - user's product query
                - messages: list - conversation history (optional)
                - customer_id: str - customer ID for order placement (optional)

        Returns:
            Updated state with:
                - response: str - agent's response
                - steps: list - tool calls made during execution
        """
        query = state.get("query", "")
        history = state.get("messages", [])
        customer_id = state.get("customer_id")

        # Set customer_id on tools that need it
        if customer_id:
            for tool in self.tools:
                if hasattr(tool, "set_customer_id"):
                    tool.set_customer_id(customer_id)

        if not query:
            return {
                **state,
                "response": "No query provided.",
                "steps": [],
            }

        try:
            # Build messages with conversation history
            messages = self._build_messages_with_history(query, history)

            logger.debug(f"ProductAgent invoking with {len(messages)} messages")

            # Invoke agent with messages format
            # Pass max_iterations in config
            result = self._agent.invoke(
                {"messages": messages},
                config={"configurable": {"max_iterations": self.max_iterations}},
            )

            # Extract response from messages
            result_messages = result.get("messages", [])
            response = ""
            if result_messages:
                last_message = result_messages[-1]
                response = getattr(last_message, "content", str(last_message))

            # Extract tool steps
            steps = self._extract_tool_steps(result_messages)

            logger.debug(f"ProductAgent response: {response[:100]}...")
            logger.debug(f"ProductAgent tool steps: {len(steps)}")

            return {
                **state,
                "response": response,
                "steps": steps,
            }

        except Exception as e:
            logger.error(f"ProductAgent execution failed: {e}")
            return {
                **state,
                "response": f"Error processing query: {e}",
                "steps": [],
            }
