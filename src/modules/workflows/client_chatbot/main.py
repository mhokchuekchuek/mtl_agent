"""Client chatbot workflow definition."""

from langgraph.graph import END, StateGraph

from libs.logger.logger import get_logger
from src.modules.agents.client.chat_history import CustomerChatHistoryAgent
from src.modules.agents.client.insight import CustomerInsightAgent
from src.modules.agents.client.orchestrator import Intent, OrchestratorAgent
from src.modules.agents.translation.main import TranslationAgent
from src.modules.workflows.base import BaseWorkflow
from src.modules.workflows.client_chatbot.state import ClientChatbotState

logger = get_logger(__name__)


class ClientChatbotWorkflow(BaseWorkflow):
    """Client chatbot workflow definition.

    Defines the graph structure:
    translate_input → orchestrator → [chat_history | insight] → translate_output

    Does NOT compile - that's done by ClientChatbotRepository.
    """

    def __init__(
        self,
        translation_agent: TranslationAgent,
        orchestrator_agent: OrchestratorAgent,
        chat_history_agent: CustomerChatHistoryAgent,
        insight_agent: CustomerInsightAgent,
    ):
        """Initialize workflow with agents.

        Args:
            translation_agent: Agent for language detection and translation.
            orchestrator_agent: Agent for classifying intent.
            chat_history_agent: ReAct agent for chat history lookup.
            insight_agent: ReAct agent for BI analytics.
        """
        self.translation_agent = translation_agent
        self.orchestrator_agent = orchestrator_agent
        self.chat_history_agent = chat_history_agent
        self.insight_agent = insight_agent

    def build(self) -> StateGraph:
        """Build and return the uncompiled graph.

        Returns:
            StateGraph ready to be compiled with checkpointer/store.
        """
        graph = StateGraph(ClientChatbotState)

        # Add nodes
        graph.add_node("translate_input", self._translate_input)
        graph.add_node("orchestrator", self._run_orchestrator)
        graph.add_node("chat_history", self._run_chat_history)
        graph.add_node("insight", self._run_insight)
        graph.add_node("translate_output", self._translate_output)

        # Define edges
        graph.set_entry_point("translate_input")
        graph.add_edge("translate_input", "orchestrator")

        # Conditional routing based on intent
        graph.add_conditional_edges(
            "orchestrator",
            self._route_by_intent,
            {
                Intent.CHAT_HISTORY: "chat_history",
                Intent.INSIGHT: "insight",
            },
        )

        graph.add_edge("chat_history", "translate_output")
        graph.add_edge("insight", "translate_output")
        graph.add_edge("translate_output", END)

        return graph

    def _translate_input(self, state: ClientChatbotState) -> dict:
        """Detect language and translate to English."""
        input_data = {
            "user_input": state["query"],
            "target_lang": "en",
        }
        result = self.translation_agent.execute(input_data)

        return {
            "user_language": result["detected_lang"],
            "translated_query": result["translated_text"],
            "steps": [
                {
                    "name": "translation_agent",
                    "input": input_data,
                    "output": result,
                }
            ],
        }

    def _run_orchestrator(self, state: ClientChatbotState) -> dict:
        """Classify intent from query."""
        input_data = {"translated_query": state["translated_query"]}
        result = self.orchestrator_agent.execute(input_data)

        return {
            "intent": result["intent"],
            "steps": [
                {
                    "name": "orchestrator_agent",
                    "input": input_data,
                    "output": {"intent": result["intent"].value},
                }
            ],
        }

    def _route_by_intent(self, state: ClientChatbotState) -> Intent:
        """Route to appropriate agent based on intent."""
        return state["intent"]

    def _run_chat_history(self, state: ClientChatbotState) -> dict:
        """Run chat history agent."""
        input_data = {
            "translated_query": state["translated_query"],
            "messages": state.get("messages", []),
        }
        result = self.chat_history_agent.execute(input_data)

        tool_steps = result.get("steps", [])

        new_messages = self._build_conversation_messages(
            query=state["translated_query"],
            response=result["response"],
            tool_steps=tool_steps,
        )

        return {
            "response": result["response"],
            "messages": new_messages,
            "steps": [
                {
                    "name": "chat_history_agent",
                    "input": input_data,
                    "output": {"response": result["response"]},
                    "tool_calls": tool_steps,
                }
            ],
        }

    def _run_insight(self, state: ClientChatbotState) -> dict:
        """Run insight agent."""
        input_data = {
            "translated_query": state["translated_query"],
            "messages": state.get("messages", []),
        }
        result = self.insight_agent.execute(input_data)

        tool_steps = result.get("steps", [])

        new_messages = self._build_conversation_messages(
            query=state["translated_query"],
            response=result["response"],
            tool_steps=tool_steps,
        )

        return {
            "response": result["response"],
            "messages": new_messages,
            "chart_html": result.get("chart_html"),
            "steps": [
                {
                    "name": "insight_agent",
                    "input": input_data,
                    "output": {
                        "response": result["response"],
                        "has_chart": result.get("chart_html") is not None,
                    },
                    "tool_calls": tool_steps,
                }
            ],
        }

    def _translate_output(self, state: ClientChatbotState) -> dict:
        """Translate response back to user's language."""
        if state["user_language"] == "en":
            return {}

        input_data = {
            "text": state["response"],
            "target_lang": state["user_language"],
        }
        result = self.translation_agent.translate(
            state["response"],
            target_lang=state["user_language"],
        )

        return {
            "response": result["translated_text"],
            "steps": [
                {
                    "name": "translation_agent",
                    "input": input_data,
                    "output": result,
                }
            ],
        }
