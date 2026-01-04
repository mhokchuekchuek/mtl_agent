# **📦 Libs Module**

Reusable utilities and external service integrations.


---


## **📑 Table of Contents**

- [Categories](#-categories)
- [Provider Pattern](#-provider-pattern)
- [Adding New Providers](#-adding-new-providers)


---


## **📂 Categories**

| | | |
|:---:|:---:|:---:|
| [🔧 **Base**](base/README.md)<br/>Base classes for provider pattern | [⚙️ **Configs**](configs/README.md)<br/>Configuration management | [🤖 **LLM**](llm/README.md)<br/>LLM provider integrations |
| [🗄️ **Database**](database/README.md)<br/>Database and vector store clients | [📝 **Logger**](logger/README.md)<br/>Logging utilities | |


---


## **🔌 Provider Pattern**

### 🎯 **Purpose**

Swappable implementations for external services.


### 📐 **Structure**

- **Base Class**: Abstract interface defining common methods
- **Selector**: Factory for provider selection via registry
- **Providers**: Concrete implementations


### ✅ **Benefits**

- Easy testing with mocks
- Switch providers without code changes
- Consistent interface across providers


---


## **➕ Adding New Providers**

> 💡 **Tip:** Follow these steps to add a new provider implementation.

### 📝 **Steps**

1. Create provider implementation inheriting from base class
2. Register in selector's `_PROVIDERS` registry
3. Configure provider name in settings
4. Create documentation file for the new provider
