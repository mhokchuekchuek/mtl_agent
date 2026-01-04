# **🔧 How It Works**


---


## **📋 Overview**

The extractor uses LLM to convert raw PDF text into structured product data.


---


## **🔄 Flow**

```mermaid
flowchart LR
    A[Raw Text<br/>from PDF] --> B[Build Prompt<br/>text + schema]
    B --> C[Call LLM<br/>gpt-4o-mini]
    C --> D[Parse Response<br/>extract JSON]
    D --> E[Structured<br/>Data]
```


---


## **📜 Prompt Template**

**Location**: [prompts/ingestor/extract_product.prompt](../../../prompts/ingestor/extract_product.prompt)

The extractor sends a prompt asking LLM to extract:

| Field | Description |
|-------|-------------|
| `product_name` | Product name from title |
| `description` | Description paragraph |
| `specifications` | Key-value pairs (type, category, dimensions, etc.) |
| `features` | List of features with title and description |
| `summary` | Closing summary paragraph |
