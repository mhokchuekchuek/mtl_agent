# **🤖 Agents**

LLM-powered agents for complex reasoning and orchestration.


---


## **📍 Location**

`src/modules/agents/`


---


## **🏗️ Architecture**

```
src/modules/agents/
├── base.py              # BaseAgent abstract class
├── client/              # Client chatbot agents
│   ├── orchestrator.py  # Intent classification
│   ├── insight.py       # BI analytics
│   └── chat_history.py  # Chat lookup
├── products/            # Customer chatbot
│   └── main.py          # Product queries
└── translation/         # Shared
    └── main.py          # Thai ↔ English
```


---


## **📖 Documentation**


### 🎯 **base**

| | |
|:---:|:---:|
| [🎯 **Base**](base.md)<br/>BaseAgent abstract class | |


### 💼 **client**

| | | |
|:---:|:---:|:---:|
| [🔀 **Orchestrator**](client/orchestrator.md)<br/>Intent classification and routing | [📊 **Insight**](client/insight.md)<br/>BI analytics and visualization | [💬 **Chat History**](client/chat_history.md)<br/>Customer chat history lookup |


### 🛒 **products**

| | |
|:---:|:---:|
| [🛍️ **Main**](products/main.md)<br/>Product queries, orders, recommendations | |


### 🌐 **translation**

| | |
|:---:|:---:|
| [🌐 **Main**](translation/main.md)<br/>Thai ↔ English translation | |
