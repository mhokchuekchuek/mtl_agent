# **🔧 Tools**

LangChain tools for agent workflows.


---


## **📍 Location**

[`src/modules/tools/`](../../../../src/modules/tools/)


---


## **📦 Categories**

| | |
|:---:|:---:|
| [🔍 **Knowledge Retrieval**](knowledge_retrieval/README.md)<br/>Tools for searching and retrieving information | [📊 **Visualization**](visualization/README.md)<br/>Tools for generating charts |


---


## **🎯 Tool Pattern**

All tools inherit from LangChain's `BaseTool` class:

```python
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

class MyToolInput(BaseModel):
    """Input schema for the tool."""
    param: str = Field(description="Parameter description")

class MyTool(BaseTool):
    name: str = "my_tool"
    description: str = "Tool description for LLM"
    args_schema: Type[BaseModel] = MyToolInput

    def __init__(self, dependency: SomeDependency, **kwargs):
        super().__init__(**kwargs)
        self.dependency = dependency

    def _run(self, param: str) -> Any:
        """Execute the tool."""
        return self.dependency.do_something(param)
```
