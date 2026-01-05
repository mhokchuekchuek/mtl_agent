# **📚 MTL Agent Documentation**

Documentation for the MTL Agent ERP multi-agent system.

> 💡 **Tip:** New to the project? Start with the [Quick Start](../README.md#-quick-start) guide.


---


## **🔄 System Flow**


### 1️⃣ **Data Ingestion**

Ingest product PDFs into vector database for semantic search.

![Ingestor Pipeline](assets/diagrams/guides/guides_data-science_1.png)

→ See [Ingestor Pipeline](ingestor/README.md)


---


### 2️⃣ **Multi-Agent System**

Process user queries through agents, tools, and workflows.

![Full Architecture](assets/diagrams/misc/README_1.png)

→ See [Multi-Agent Systems](multi-agent-systems/README.md)


---


### 3️⃣ **Evaluation & Improvement**

Run LLM-as-Judge evaluation to measure and improve quality.

![Evaluation Cycle](assets/diagrams/evaluation/eval_cycle_1.png)

→ See [Evaluation](evaluation/README.md)


---


## **📖 Documentation**

| | | |
|:---:|:---:|:---:|
| [🤖 **Multi-Agent Systems**](multi-agent-systems/README.md)<br/>Agents, tools, workflows, repositories | [📝 **Decisions**](decisions/README.md)<br/>Architecture decision records | [🔧 **Infrastructure**](infrastructure/README.md)<br/>Docker services, setup guides |
| [📦 **Libs**](libs/README.md)<br/>Reusable libraries | [📖 **Guides**](guides/README.md)<br/>User, developer, data science guides | [💬 **Prompts**](prompts/README.md)<br/>Prompt management with Langfuse |
| [🗄️ **Databases**](database/README.md)<br/>SQLite, PostgreSQL, Redis | [⚙️ **Ingestor**](ingestor/README.md)<br/>PDF ingestion pipeline | [🧪 **Evaluation**](evaluation/README.md)<br/>Testing and LLM-as-Judge |
| [🔮 **Future**](future_improvements/README.md)<br/>Potential enhancements | | |
