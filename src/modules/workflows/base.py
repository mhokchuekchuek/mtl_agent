"""Base interface for workflows."""

from abc import ABC, abstractmethod

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langgraph.graph import StateGraph


class BaseWorkflow(ABC):
    """Abstract base for workflow definitions.

    Workflows define graph structure but do NOT compile.
    Compilation with checkpointer/store is done by repositories.
    """

    @abstractmethod
    def build(self) -> StateGraph:
        """Build and return the uncompiled graph."""
        pass

    def _build_conversation_messages(
        self,
        query: str,
        response: str,
        tool_steps: list[dict],
    ) -> list:
        """Build messages list with ToolMessages for checkpoint.

        Args:
            query: User query (translated)
            response: Agent response
            tool_steps: List of tool calls from agent

        Returns:
            List of messages [HumanMessage, ToolMessage..., AIMessage]
        """
        messages = [HumanMessage(content=query)]

        for i, step in enumerate(tool_steps):
            tool_output = step.get("output", "")
            tool_name = step.get("name", "tool")
            messages.append(
                ToolMessage(
                    content=str(tool_output),
                    tool_call_id=f"tool_{i}",
                    name=tool_name,
                )
            )

        messages.append(AIMessage(content=response))

        return messages
