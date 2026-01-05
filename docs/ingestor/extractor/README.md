# **🔄 Extractor**

LLM-based structured data extraction using provider/selector pattern.


---


## **📍 Location**

[`ingestor/extractor/`](../../../ingestor/extractor/)


---


## **🔄 Flow**

<details>
<summary>📊 Extraction Flow</summary>

![Extraction Flow](../../assets/diagrams/ingestor/extractor_how_it_works_1.png)

</details>


### **📥 Input**

Raw text extracted from PDF.


### **📤 Output**

```json
{
  "product_name": "Espresso Coffee Maker",
  "description": "Premium espresso machine for home use...",
  "specifications": {
    "product_type": "Coffee Maker",
    "category": "Kitchen Appliances",
    "dimensions": "12 x 8 x 14 inches",
    "weight": "10 lbs"
  },
  "features": [
    {
      "title": "15-Bar Pump",
      "description": "Professional-grade pressure for rich espresso"
    }
  ],
  "summary": "The perfect addition to your kitchen..."
}
```


---


## **📦 Providers**

| | |
|:---:|:---:|
| [🤖 **LiteLLM**](litellm.md)<br/>LiteLLM-based extraction | |


---


## **🔧 Classes**


### 🎯 **BaseExtractor**

Abstract base class for extractors.

**Location**: [`ingestor/extractor/base.py`](../../../ingestor/extractor/base.py)

**Methods**:

| Method | Description |
|--------|-------------|
| `extract(text, **kwargs)` | Extract structured data from text |


### 🔀 **ExtractorSelector**

Selector for extractor providers.

**Location**: [`ingestor/extractor/selector.py`](../../../ingestor/extractor/selector.py)

**Methods**:

| Method | Description |
|--------|-------------|
| `create(provider, **kwargs)` | Create extractor instance |
| `list_providers()` | List available providers |
