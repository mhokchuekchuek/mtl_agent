"""Customer insight agent for BI analytics and visualizations."""

import json
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
            chart_htmls = []

            # Extract response and chart HTML from messages
            for msg in result_messages:
                msg_type = getattr(msg, "type", None)
                content = getattr(msg, "content", str(msg))

                # Extract chart HTML from tool responses (visualization tool output)
                if msg_type == "tool" and "plotly" in content.lower():
                    # Tool returns JSON: {"request": ..., "results": "<html>"}
                    try:
                        tool_result = json.loads(content)
                        if isinstance(tool_result, dict) and "results" in tool_result:
                            html = tool_result["results"]
                            if "<div" in html:
                                chart_htmls.append(html)
                    except (json.JSONDecodeError, TypeError):
                        # Fallback: content might be raw HTML
                        if "<div" in content:
                            chart_htmls.append(content)

            # Get the final assistant response (last AI message)
            for msg in reversed(result_messages):
                msg_type = getattr(msg, "type", None)
                if msg_type == "ai":
                    response = getattr(msg, "content", str(msg))
                    # Remove any raw HTML/chart content that may have leaked into response
                    if "<div" in response or "<script" in response:
                        import re

                        # Remove HTML tags and script blocks
                        response = re.sub(
                            r"<div[^>]*>.*?</div>", "", response, flags=re.DOTALL
                        )
                        response = re.sub(
                            r"<script[^>]*>.*?</script>", "", response, flags=re.DOTALL
                        )
                        response = response.strip()
                    break

            # Combine all chart HTMLs if multiple visualizations were created
            chart_html = "\n".join(chart_htmls) if chart_htmls else None

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
