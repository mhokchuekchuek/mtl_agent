"""Customer insight agent for BI analytics and visualizations."""

from typing import Any

from langchain.agents import create_agent
from langchain.tools import BaseTool
from langchain_openai import ChatOpenAI

from libs.llm.prompt_manager.base import BasePromptManager
from libs.logger.logger import get_logger
from src.modules.agents.base import BaseAgent

logger = get_logger(__name__)


class CustomerInsightAgent(BaseAgent):
    """ReAct agent for customer insights and BI analytics.

    Uses SQLTool with SQLite to query ERP data (Orders, Customers, etc.)
    and VisualizationTool to create charts.
    """

    def __init__(
        self,
        llm: ChatOpenAI,
        prompt_manager: BasePromptManager,
        tools: list[BaseTool],
        prompt_name: str = "client_chatbot_insight",
        prompt_label: str | None = None,
        max_iterations: int = 5,
        recursion_limit: int = 25,
    ):
        """Initialize insight agent.

        Args:
            llm: ChatOpenAI instance.
            prompt_manager: Prompt manager for retrieving prompts.
            tools: List of tools (SQLTool with SQLite, VisualizationTool).
            prompt_name: Name of the prompt in prompt manager.
            prompt_label: Label for prompt retrieval.
            max_iterations: Maximum number of ReAct iterations.
            recursion_limit: LangGraph recursion limit for invoke.
        """
        super().__init__(name="insight")
        self.llm = llm
        self.prompt_manager = prompt_manager
        self.tools = tools
        self.prompt_name = prompt_name
        self.prompt_label = prompt_label
        self.max_iterations = max_iterations
        self.recursion_limit = recursion_limit

        self._agent = self._build_agent()

    def _build_messages_with_history(
        self, query: str, history: list
    ) -> list[dict[str, str]]:
        """Build messages list including conversation history.

        Args:
            query: Current user query.
            history: List of previous messages from state.

        Returns:
            List of message dicts with role and content.
        """
        messages = []

        for msg in history:
            msg_type = getattr(msg, "type", None)
            content = getattr(msg, "content", str(msg))

            if msg_type == "ai" or msg_type == "assistant":
                messages.append({"role": "assistant", "content": content})
            elif msg_type == "human" or msg_type == "user":
                messages.append({"role": "user", "content": content})

        messages.append({"role": "user", "content": query})

        return messages

    def _build_agent(self):
        """Build the ReAct agent."""
        prompt_obj = self.prompt_manager.get_prompt(
            self.prompt_name,
            label=self.prompt_label,
        )
        system_prompt = prompt_obj.compile()

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
                    # Truncate chart HTML in output
                    content = msg.content
                    if "<div" in content and len(content) > 500:
                        step["output"] = "[chart_html generated]"
                    else:
                        step["output"] = content
                    steps.append(step)

        return steps

    def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        """Execute insight analysis.

        Args:
            state: Current state with keys:
                - translated_query: str - query in English
                - messages: list - conversation history (optional)

        Returns:
            Updated state with:
                - response: str - analysis results
                - chart_html: str | None - visualization HTML if created
                - steps: list - tool calls made during execution
        """
        query = state.get("translated_query", state.get("query", ""))
        history = state.get("messages", [])

        if not query:
            return {"response": "No query provided.", "chart_html": None, "steps": []}

        try:
            messages = self._build_messages_with_history(query, history)

            logger.debug(f"InsightAgent invoking with {len(messages)} messages")

            result = self._agent.invoke(
                {"messages": messages},
                config={"recursion_limit": self.recursion_limit},
            )

            result_messages = result.get("messages", [])
            response = ""
            chart_html = None

            # Extract response and any chart HTML from messages
            for msg in result_messages:
                content = getattr(msg, "content", str(msg))

                # Check if this is a tool response containing chart HTML
                if "<div" in content and "plotly" in content.lower():
                    chart_html = content
                elif hasattr(msg, "role") and msg.role == "assistant":
                    response = content

            # If no explicit assistant response, use last message
            if not response and result_messages:
                last_message = result_messages[-1]
                response = getattr(last_message, "content", str(last_message))

            steps = self._extract_tool_steps(result_messages)

            logger.debug(f"InsightAgent response: {response[:100]}...")
            logger.debug(f"InsightAgent tool steps: {len(steps)}")
            if chart_html:
                logger.debug("InsightAgent created a chart")

            return {"response": response, "chart_html": chart_html, "steps": steps}

        except Exception as e:
            logger.error(f"InsightAgent execution failed: {e}")
            return {
                "response": f"Error analyzing customer insights: {e}",
                "chart_html": None,
                "steps": [],
            }
