# **🌐 Translation Agent Prompt**

System prompt for translating text between Thai and English.


---


## **🏷️ Langfuse Name**

`client_chatbot_translation`


---


## **📍 Location**

[`prompts/agents/translation.prompt`](../../prompts/agents/translation.prompt)


---


## **🔗 Used By**

- [TranslationAgent](../../multi-agent-systems/modules/agents/translation/main.md)


---


## **🤖 Model**

`gpt-4o-mini`


---


## **📥 Variables**

| Variable | Type | Description |
|----------|------|-------------|
| `text` | string | Text to translate |
| `target_lang` | string | Target language: "th" or "en" |


---


## **💡 Purpose**

Translate text between Thai and English while:
1. Preserving meaning and tone
2. Using natural business language
3. Keeping technical terms in English


---


## **📝 Key Instructions**

- **Preserve in English**: Technical terms, KPIs, metrics
- **Preserve in English**: Database table/column names
- **Preserve in English**: Product names, category names
- **Preserve in English**: Customer names, units/measurements
- **Output**: JSON with `translated_text` and `source_lang`


---


## **📤 Output Schema**

```json
{
  "translated_text": "...",
  "source_lang": "th|en"
}
```
