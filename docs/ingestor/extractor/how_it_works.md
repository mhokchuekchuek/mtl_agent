# **🔧 How It Works**


---


## **📋 Overview**

The extractor uses LLM to convert raw PDF text into structured product data.


---


## **🔄 Flow**

<details>
<summary>📊 Extraction Flow</summary>

![Extraction Flow](../../assets/diagrams/ingestor/extractor_how_it_works_1.png)

</details>


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
