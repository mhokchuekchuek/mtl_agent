# Evaluation Framework

LLM-as-Judge evaluation framework for ERP Multi-Agent Chatbot.

## Overview

This framework evaluates chatbot responses using multiple judges:
- **SQLJudge** - SQL query correctness
- **SearchJudge** - Vector search quality
- **ResponseQualityJudge** - Response relevance and faithfulness
- **VisualizationJudge** - Chart generation quality

## Quick Start

```bash
# Run customer chatbot evaluation
python scripts/run_eval.py customer

# Run client chatbot evaluation
python scripts/run_eval.py client
```

## Directory Structure

```
evaluation/
├── datasets/
│   ├── customer/           # Customer chatbot test cases
│   │   ├── sql/
│   │   ├── search/
│   │   └── response_quality/
│   └── client/             # Client chatbot test cases
│       ├── sql/
│       ├── visualization/
│       └── response_quality/
├── judges/
│   ├── sql/
│   ├── search/
│   ├── response_quality/
│   └── visualization/
├── repositories/
├── usecases/
└── dependencies/
```

## Configuration

Config files in `configs/evaluation/`:
- `customer.yaml` - Customer chatbot evaluation config
- `client.yaml` - Client chatbot evaluation config

## Results

Results saved to `results/{chatbot}/{turn_type}/{test_id}_{timestamp}/`:
- `results.yaml` - Summary with scores
- `detail.yaml` - Full execution steps

## Documentation

- [Datasets](datasets.md) - Dataset format and structure
- [Results](results.md) - Results format
- [Adding Tests](adding-tests.md) - How to add new tests
- [Judges](judges/README.md) - Judge documentation
