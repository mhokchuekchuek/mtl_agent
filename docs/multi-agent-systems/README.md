# **🤖 Multi-Agent Systems**

Documentation for the MTL Agent multi-agent chatbot system.


---


## **📋 Overview**

Two LangGraph-based chatbot workflows:

| Chatbot | Target Users | Purpose |
|---------|--------------|---------|
| **Customer Chatbot** | External (shoppers) | Product search, orders, support |
| **Client Chatbot** | Internal (BI analysts) | Analytics, insights, visualization |


---


## **📖 Documentation**

| | | |
|:---:|:---:|:---:|
| [🏗️ **Architecture**](architecture/README.md)<br/>Code and system architecture | [🔄 **Modules**](modules/README.md)<br/>Workflows, agents, tools | [🗄️ **Repositories**](repositories/README.md)<br/>Data access layer |
| [💼 **Usecases**](usecases/README.md)<br/>Business orchestration | [🔌 **Dependencies**](dependencies/README.md)<br/>Dependency injection | [⚙️ **Configs**](configs/README.md)<br/>Configuration files |
| [🔗 **API**](api/README.md)<br/>REST API endpoints | [🖥️ **UI**](ui/README.md)<br/>Streamlit web interfaces | [⌨️ **CLI**](cli/README.md)<br/>Command-line interface |


---


## **🏗️ System Architecture**

<details>
<summary>📊 System Architecture</summary>

![System Architecture](../assets/diagrams/multi-agent-systems/multi-agent-systems_README_1.png)

</details>


---


## **🔄 Chatbot Workflows**


### 👤 **Customer Chatbot**

<details>
<summary>📊 Customer Chatbot</summary>

![Customer Chatbot](../assets/diagrams/multi-agent-systems/multi-agent-systems_README_2.png)

</details>

**Tools**: SQL (product, order), VectorDB (search, similar)


### 📊 **Client Chatbot**

<details>
<summary>📊 Client Chatbot</summary>

![Client Chatbot](../assets/diagrams/multi-agent-systems/multi-agent-systems_README_3.png)

</details>

**Tools**: SQL (analytics, chat_history), Visualization (charts)


---


## **🚀 Quick Start**

```bash
# Start API server
python main.py api

# Start Customer UI
python main.py customer_ui

# Start Client UI
python main.py client_ui
```


---


## **📝 Design Decisions**

| Decision | Link |
|----------|------|
| ReAct & LangGraph | [why_react_and_langgraph.md](../decisions/why_react_and_langgraph.md) |
| Checkpointer + Store | [why_checkpointer_and_store.md](../decisions/why_checkpointer_and_store.md) |
| OpenAI Model | [why_openai_model.md](../decisions/why_openai_model.md) |
| Langfuse | [why_langfuse.md](../decisions/why_langfuse.md) |


---


## **🔮 Future Improvements**

| Improvement | Link |
|-------------|------|
| Workflow Orchestrator | [workflow_orchestrator.md](../future_improvements/ingestion/workflow_orchestrator.md) |
| Async Store Writes | [async_store_writes.md](../future_improvements/chat_history/async_store_writes.md) |
| Embedding Models | [embedding_models.md](../future_improvements/ingestion/embedding_models.md) |
