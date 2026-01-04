# **🖼️ Assets**

Static assets for documentation.


---


## **📁 Structure**

```
assets/
├── screenshots/           # UI screenshots
│   ├── client_*.png
│   ├── customer_*.png
│   └── langfuse_*.png
└── diagrams/              # Mermaid diagrams (.mmd + .png)
    ├── api/
    ├── architecture/
    ├── cli/
    ├── configs/
    ├── decisions/
    ├── dependencies/
    ├── evaluation/
    ├── future_improvements/
    ├── guides/
    ├── modules/
    ├── multi-agent-systems/
    ├── prompts/
    ├── repositories/
    ├── ui/
    └── usecases/
```


---


## **📸 Screenshots**

| File | Description |
|------|-------------|
| `client_graph.png` | Client chatbot with chart |
| `client_without_graph.png` | Client chatbot without chart |
| `client_lookup_customer_chat.png` | Client looking up chat history |
| `customer_ask_for_product.png` | Customer searching products |
| `customer_order.png` | Customer placing order |
| `customer_cancel_order.png` | Customer canceling order |
| `customer_view_their_order.png` | Customer viewing orders |
| `langfuse_prompts.png` | Langfuse prompts dashboard |
| `langfuse_trace.png` | Langfuse trace view |
| `langfuse_dashboard.png` | Langfuse main dashboard |


---


## **📊 Diagrams**

Mermaid source files (`.mmd`) with generated PNGs.

```bash
# Regenerate all diagrams from .mmd files
cd scripts/diagram_generator && npm install && python generate_diagrams.py

# Extract mermaid from markdown and generate (one-time conversion)
cd scripts/diagram_generator && python extract_and_generate.py
```

| Folder | Contents |
|--------|----------|
| `api/` | API endpoint diagrams |
| `architecture/` | System layer diagrams |
| `cli/` | CLI flow diagrams |
| `configs/` | Configuration diagrams |
| `decisions/` | Decision documentation diagrams |
| `dependencies/` | Dependency injection diagrams |
| `evaluation/` | Evaluation system diagrams |
| `future_improvements/` | Future improvement proposals |
| `guides/` | Guide-related diagrams |
| `modules/` | Agent, tool, and workflow diagrams |
| `multi-agent-systems/` | Multi-agent system overview |
| `prompts/` | Prompt flow diagrams |
| `repositories/` | Repository layer diagrams |
| `ui/` | UI flow diagrams |
| `usecases/` | Use case diagrams |
