"""Customer chatbot workflow definition."""

from langgraph.graph import END, StateGraph

from libs.logger.logger import get_logger
from src.modules.agents.products.main import ProductAgent
from src.modules.agents.translation.main import TranslationAgent
from src.modules.workflows.customer_chatbot.state import ShoppingState

logger = get_logger(__name__)


class CustomerChatbotWorkflow:
    """Customer chatbot workflow definition.

    Defines the graph structure:
    translate_input → product_agent → translate_output

    Does NOT compile - that's done by ChatbotRepository.
    """

    def __init__(
        self,
        translation_agent: TranslationAgent,
        product_agent: ProductAgent,
    ):
        """Initialize workflow with agents.

        Args:
            translation_agent: Agent for language detection and translation.
            product_agent: ReAct agent for product queries.
        """
        self.translation_agent = translation_agent
        self.product_agent = product_agent

    def build(self) -> StateGraph:
        """Build and return the uncompiled graph.

        Returns:
            StateGraph ready to be compiled with checkpointer/store.
        """
        graph = StateGraph(ShoppingState)

        graph.add_node("translate_input", self._translate_input)
        graph.add_node("product_agent", self._run_product_agent)
        graph.add_node("translate_output", self._translate_output)

        graph.set_entry_point("translate_input")
        graph.add_edge("translate_input", "product_agent")
        graph.add_edge("product_agent", "translate_output")
        graph.add_edge("translate_output", END)

        return graph

    def _translate_input(self, state: ShoppingState) -> dict:
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

    def _run_product_agent(self, state: ShoppingState) -> dict:
        """Run product agent with translated query."""
        input_data = {"query": state["translated_query"]}
        result = self.product_agent.execute(input_data)

        # Get tool steps from product agent if available
        tool_steps = result.get("steps", [])

        return {
            "response": result["response"],
            "steps": [
                {
                    "name": "product_agent",
                    "input": input_data,
                    "output": {"response": result["response"]},
                    "tool_calls": tool_steps,
                }
            ],
        }

    def _translate_output(self, state: ShoppingState) -> dict:
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
