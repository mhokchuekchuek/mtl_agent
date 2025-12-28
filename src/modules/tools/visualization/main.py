"""Visualization tool for generating Plotly charts.

Uses LLM to generate Plotly code from data and natural language request,
then executes in a sandbox environment.
"""

import json
import re
from typing import Any, Optional, Type

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

from libs.llm.client.base import BaseLLM
from libs.llm.prompt_manager.base import BasePromptManager
from libs.logger.logger import get_logger

logger = get_logger(__name__)


class VisualizationInput(BaseModel):
    """Input schema for visualization tool."""

    data: list[dict] = Field(description="Data to visualize as list of dictionaries")
    request: str = Field(
        description="Natural language description of the chart to create"
    )


class VisualizationTool(BaseTool):
    """Create Plotly visualizations from data using LLM-generated code.

    Uses LLM to generate Plotly code based on the data and request,
    then executes the code in a sandbox with limited globals.
    """

    name: str = "create_visualization"
    description: str = (
        "Create a Plotly chart from data. "
        "Use this when you need to visualize query results as charts. "
        "Provide the data and describe what kind of chart you want."
    )
    args_schema: Type[BaseModel] = VisualizationInput
    llm_client: Optional[BaseLLM] = None
    prompt_manager: Optional[BasePromptManager] = None
    prompt_name: str = "client_chatbot_visualization"
    prompt_label: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True

    def __init__(
        self,
        llm_client: BaseLLM,
        prompt_manager: BasePromptManager,
        prompt_name: str = "client_chatbot_visualization",
        prompt_label: Optional[str] = None,
        **kwargs,
    ):
        """Initialize visualization tool.

        Args:
            llm_client: LLM client for code generation.
            prompt_manager: Prompt manager for retrieving prompts.
            prompt_name: Name of the prompt in prompt manager.
            prompt_label: Prompt version label.
            **kwargs: Additional arguments passed to BaseTool.
        """
        super().__init__(**kwargs)
        self.llm_client = llm_client
        self.prompt_manager = prompt_manager
        self.prompt_name = prompt_name
        self.prompt_label = prompt_label

        logger.info("VisualizationTool initialized")

    def _generate_plotly_code(self, data: list[dict], request: str) -> str:
        """Generate Plotly code using LLM.

        Args:
            data: Data to visualize.
            request: Natural language description of the chart.

        Returns:
            Python code string that creates a Plotly figure.
        """
        # Get column names and sample data for context
        if data:
            columns = list(data[0].keys())
            sample = data[:3] if len(data) > 3 else data
        else:
            columns = []
            sample = []

        # Get prompt and compile
        prompt = self.prompt_manager.get_prompt(
            self.prompt_name, label=self.prompt_label
        )
        compiled = prompt.compile(
            columns=json.dumps(columns),
            sample_data=json.dumps(sample, indent=2),
            row_count=len(data),
            request=request,
        )

        # Generate code
        response = self.llm_client.generate(prompt=compiled)
        code = self._extract_code(response)

        logger.debug(f"Generated Plotly code:\n{code}")
        return code

    def _extract_code(self, response: str) -> str:
        """Extract Python code from LLM response.

        Args:
            response: LLM response that may contain code blocks.

        Returns:
            Extracted Python code.
        """
        # Try to extract from markdown code block
        pattern = r"```(?:python)?\n(.*?)```"
        matches = re.findall(pattern, response, re.DOTALL)
        if matches:
            return matches[0].strip()

        # If no code block, return the whole response
        return response.strip()

    def _safe_exec(self, code: str, data: list[dict]) -> go.Figure:
        """Execute code in sandbox with limited globals.

        Args:
            code: Python code to execute.
            data: Data to make available as 'data' variable.

        Returns:
            Plotly Figure object.

        Raises:
            ValueError: If code execution fails or no figure is created.
        """
        # Convert data to DataFrame for easier manipulation
        df = pd.DataFrame(data)

        # Allowed globals only - block dangerous builtins
        allowed_globals = {
            "pd": pd,
            "px": px,
            "go": go,
            "data": data,
            "df": df,
            "__builtins__": {
                "len": len,
                "str": str,
                "int": int,
                "float": float,
                "list": list,
                "dict": dict,
                "range": range,
                "enumerate": enumerate,
                "zip": zip,
                "sorted": sorted,
                "sum": sum,
                "min": min,
                "max": max,
                "abs": abs,
                "round": round,
                "True": True,
                "False": False,
                "None": None,
            },
        }

        local_vars: dict[str, Any] = {}

        try:
            exec(code, allowed_globals, local_vars)
        except Exception as e:
            logger.error(f"Code execution failed: {e}")
            raise ValueError(f"Failed to execute visualization code: {e}")

        # Find the figure in local variables
        fig = local_vars.get("fig")
        if fig is None:
            # Try to find any Figure object
            for var in local_vars.values():
                if isinstance(var, go.Figure):
                    fig = var
                    break

        if fig is None:
            raise ValueError("No Plotly figure was created by the code")

        return fig

    def _run(
        self,
        data: list[dict],
        request: str,
    ) -> dict:
        """Create visualization from data.

        Args:
            data: Data to visualize.
            request: Natural language description of the chart.

        Returns:
            Dict with request and results (HTML chart or error message).
        """
        logger.info(f"Creating visualization: {request}")

        if not data:
            return {
                "request": request,
                "results": "<p>No data available for visualization</p>",
            }

        try:
            # Generate code
            code = self._generate_plotly_code(data, request)

            # Execute in sandbox
            fig = self._safe_exec(code, data)

            # Return HTML
            html = fig.to_html(full_html=False, include_plotlyjs="cdn")
            logger.info("Visualization created successfully")
            return {"request": request, "results": html}

        except Exception as e:
            error_msg = f"Failed to create visualization: {e}"
            logger.error(error_msg)
            return {"request": request, "results": f"<p>Error: {error_msg}</p>"}
