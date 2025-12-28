"""Base interface for workflows."""

from abc import ABC, abstractmethod

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
