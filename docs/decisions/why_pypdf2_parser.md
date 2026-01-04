# **📝 Why PyPDF2 Parser**


---


## **📋 Context**

Need to choose a PDF parser to extract text from product PDFs.


---


## **🔄 Options Considered**

| Parser | Pros | Cons |
|--------|------|------|
| **PyPDF2** | Fast, lightweight, simple API | Limited layout handling |
| Docling | Better structure preservation, handles complex layouts | Slower, heavier dependencies |


---


## **✅ Decision**

Use **PyPDF2**.


---


## **💡 Rationale**

- Product PDFs have simple layouts (no complex tables or multi-column)
- Faster processing for batch ingestion
- Fewer dependencies
- Good enough text extraction for LLM to understand


---


## **📄 Example Output**

Sample text extracted from `100_smart_fan.pdf`:

```text
Smart Fan
Description
The Smart Fan is a state-of-the-art cooling solution designed to enhance your comfort
and convenience. With its sleek design and advanced technology, this fan is perfect
for any room in your home or office.

Specifications
- Product Type: Miscellaneous
- Category: Others
- Price: $275
- Dimensions: 18 x 18 x 48 inches
- Weight: 10 lbs
- Power Supply: AC 110-240V, 50/60Hz
- Connectivity: Wi-Fi, Bluetooth

Features
- Smart Connectivity: Easily connect the Smart Fan to your home Wi-Fi network...
- Energy Efficient: Designed to consume minimal power while providing maximum airflow...
- Quiet Operation: Engineered to operate quietly...
```

> 💡 **Tip:** The text is clean and structured enough for LLM extraction.


---


## **🔗 References**

- [Preparing PDFs for RAGs](https://towardsdatascience.com/preparing-pdfs-for-rags-b1579fc697f1/)
