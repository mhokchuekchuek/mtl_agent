# Evaluation Architecture

System design and request flow.

## Layers

```mermaid
flowchart TD
    subgraph Entry
        CLI[run_eval.py]
    end
    
    subgraph Dependencies
        DEP[build_evaluation_service]
    end
    
    subgraph Usecases
        SVC[EvaluationService]
    end
    
    subgraph Repositories
        REPO[EvaluationRepository]
    end
    
    subgraph Judges
        SQL[SQLJudge]
        SEARCH[SearchJudge]
        VIZ[VisualizationJudge]
        RQ[ResponseQualityJudge]
    end
    
    CLI --> DEP
    DEP --> SVC
    SVC --> REPO
    REPO --> SQL
    REPO --> SEARCH
    REPO --> VIZ
    REPO --> RQ
```

| Layer | Location | Responsibility |
|-------|----------|----------------|
| CLI | `scripts/run_eval.py` | Entry point, select chatbot type |
| Dependencies | `evaluation/dependencies/` | Factory, wire components |
| Usecases | `evaluation/usecases/` | Orchestrate evaluation run |
| Repositories | `evaluation/repositories/` | Load data, invoke API, run judges |
| Judges | `evaluation/judges/` | Evaluate specific aspects |

## Evaluation Flow

```mermaid
flowchart TD
    subgraph 1. Load
        DS[Load Datasets] --> TC[Test Cases]
    end
    
    subgraph 2. For Each Test Case
        TC --> INV[Invoke Chatbot API]
        INV --> OUT[Get Response + Steps]
    end
    
    subgraph 3. Judge
        OUT --> J1[SQL Judge]
        OUT --> J2[Search Judge]
        OUT --> J3[Viz Judge]
        OUT --> J4[RQ Judge]
        J1 --> |Skip if no expected.sql| AGG
        J2 --> |Skip if no expected.search_results| AGG
        J3 --> |Skip if no expected.chart| AGG
        J4 --> |Skip if no expected.response_quality| AGG
        AGG[Aggregate Scores]
    end
    
    subgraph 4. Save
        AGG --> YAML[results.yaml]
        AGG --> DET[detail.yaml]
    end
```

## Single-Turn vs Multi-Turn

| Type | Description | Thread ID |
|------|-------------|-----------|
| Single-turn | One question, one response | New UUID per test |
| Multi-turn | Multiple turns in sequence | Same UUID for all turns |

### Multi-Turn Flow

```mermaid
flowchart LR
    T1[Turn 1] --> |Same thread_id| T2[Turn 2]
    T2 --> |Same thread_id| T3[Turn 3]
```

Each turn is evaluated separately, scores are aggregated.

## Judge Selection

Judges are selected based on `expected` fields in test case:

| Expected Field | Judge Activated |
|----------------|-----------------|
| `sql` | SQLJudge |
| `search_results` | SearchJudge |
| `chart` | VisualizationJudge |
| `response_quality` | ResponseQualityJudge |

If expected field is missing, judge returns `None` (skipped).

## Negative Cases

For negative test cases:
- `sql: "null"` → Pass if no SQL generated
- `search_results: []` → Pass if no results found
- `chart: "null"` → Pass if no chart generated

## References

- [EvaluationRepository](../../evaluation/repositories/main.py)
- [EvaluationService](../../evaluation/usecases/main.py)
