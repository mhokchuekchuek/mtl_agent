# **🛠️ Developers Guide**

Guide for software engineers who want to extend the chatbot and manage infrastructure.


---


## **🏗️ Architecture**

| Topic | Documentation |
|-------|---------------|
| System Overview | [multi-agent-systems/README.md](../multi-agent-systems/README.md) |
| Code Architecture | [architecture/code.md](../architecture/code.md) |


---


## **📁 Code Structure**

| Layer | Documentation | Purpose |
|-------|---------------|---------|
| Libraries | [libs/README.md](../libs/README.md) | Reusable components |
| Modules | [modules/README.md](../multi-agent-systems/modules/README.md) | Workflows, agents, tools |
| Repositories | [repositories/README.md](../multi-agent-systems/repositories/README.md) | Data access layer |
| Usecases | [usecases/README.md](../multi-agent-systems/usecases/README.md) | Business orchestration |
| Dependencies | [dependencies/README.md](../multi-agent-systems/dependencies/README.md) | Dependency injection |
| Configs | [configs/README.md](../multi-agent-systems/configs/README.md) | Configuration files |


---


## **🔧 Infrastructure**

| Topic | Documentation |
|-------|---------------|
| Docker Services | [infrastructure/docker/README.md](../infrastructure/docker/README.md) |
| Setup Guide | [infrastructure/setup/README.md](../infrastructure/setup/README.md) |
| Data Sources | [data-sources/README.md](../data-sources/README.md) |


---


## **🤖 Adding New Agents**

1. Create agent class in `src/modules/agents/`
2. Inherit from `BaseAgent`
3. Implement `execute()` method
4. Create prompt in Langfuse
5. Add to workflow
6. Wire up in dependencies

> 📝 **Note:** See [agents/base.md](../multi-agent-systems/modules/agents/base.md) for the base class reference.


---


## **🔧 Adding New Tools**

1. Create tool class in `src/modules/tools/`
2. Inherit from appropriate base (SQLTool, etc.)
3. Define `name`, `description`, `args_schema`
4. Implement `_run()` method
5. Create prompt if needed
6. Add to agent's tool list

> 📝 **Note:** See [tools/README.md](../multi-agent-systems/modules/tools/README.md) for tool documentation.


---


## **🔄 Adding New Workflows**

1. Create workflow class in `src/modules/workflows/`
2. Inherit from `BaseWorkflow`
3. Define state schema
4. Implement nodes and edges
5. Create repository to compile with memory
6. Wire up in dependencies

> 📝 **Note:** See [workflows/base.md](../multi-agent-systems/modules/workflows/base.md) for the base class reference.


---


## **🚀 Running Locally**

```bash
# Start all services
docker-compose up -d

# Or run individually
python main.py api
python main.py customer-ui
python main.py client-ui
```


---


## **📝 Design Decisions**

| Decision | Documentation |
|----------|---------------|
| ReAct & LangGraph | [why_react_and_langgraph.md](../decisions/why_react_and_langgraph.md) |
| Checkpointer + Store | [why_checkpointer_and_store.md](../decisions/why_checkpointer_and_store.md) |
| Langfuse | [why_langfuse.md](../decisions/why_langfuse.md) |
