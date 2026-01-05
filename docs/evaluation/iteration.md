# **🔄 Evaluation Iteration**

How to analyze evaluation results and iterate on improvements.


---


## **📑 Table of Contents**

- [Overview](#-overview)
- [Step 1: Run Evaluation](#-step-1-run-evaluation)
- [Step 2: Analyze & Fix with AI](#-step-2-analyze--fix-with-ai)
- [Step 3: Re-evaluate](#-step-3-re-evaluate)
- [Example: Round 1 vs Round 2](#-example-round-1-vs-round-2)


---


## **📋 Overview**

Evaluation is an iterative process:

![Evaluation Cycle](../assets/diagrams/evaluation/eval_cycle_1.png)


---


## **1️⃣ Step 1: Run Evaluation**

```bash
# Run evaluation for specific chatbot
python scripts/run_eval.py customer
python scripts/run_eval.py client
```

Results are saved to `results/` folder. See [Results Format](results.md) for details on `results.yaml` and `detail.yaml`.


---


## **2️⃣ Step 2: Analyze & Fix with AI**

Use this prompt to analyze results and implement fixes:

~~~
Please loop through each test in `/results` folder:

For each failed test:
1. Read `results.yaml` to understand:
   - What was the input question?
   - What did the agent respond?
   - What was expected?
   - What score did it get and why?

2. Read `detail.yaml` to understand:
   - What tools did the agent call?
   - What were the intermediate outputs?
   - Where did it go wrong?

3. Categorize the issue:
   - Code: Tool/logic bug
   - Prompt: Agent behavior issue
   - Dataset: Test case problem
   - Judge: Scoring bug

4. Create `/improvement_round{N}` folder with two files:

   **improvement.md** - Track test case status:
   ```markdown
   # Test Case Status

   ## Customer Chatbot

   | Test Case | Category | Status | Solution |
   |-----------|----------|--------|----------|
   | `test_id` | Code/Prompt/Dataset/Judge | ✅/❌ | How to fix |
   ```

   **plan.md** - Improvement plan:
   ```markdown
   # Improvement Plan

   ## Priority 1: [Issue Name]
   - Problem: ...
   - Solution: ...
   - Files to modify: ...

   ## Priority 2: [Issue Name]
   ...
   ```

5. Implement fixes based on category:
   - Code → fix in `src/modules/`
   - Prompt → fix in `prompts/`
   - Dataset → fix in `data/eval_datasets/`
   - Judge → fix in `evaluation/judges/`
~~~


---


## **3️⃣ Step 3: Re-evaluate**

Run evaluation again and compare:

```bash
python scripts/run_eval.py customer
python scripts/run_eval.py client
```

Repeat until quality targets are met.


---


## **💡 Example: Round 1 vs Round 2**

### Round 1 Results

| Category | Passed | Total | Rate |
|----------|--------|-------|------|
| Customer Single Turn | 11 | 17 | 64.7% |
| Customer Multi Turn | 1 | 7 | 14.3% |
| Customer Negative | 1 | 6 | 16.7% |
| Client Single Turn | 9 | 12 | 75% |
| Client Multi Turn | 2 | 6 | 33.3% |
| Client Negative | 4 | 7 | 57.1% |

### AI Analysis & Fixes

Issues found and fixed:

| Issue | Category | Fix Applied |
|-------|----------|-------------|
| Customer accesses other customer data | Code | Separate SQL tools by use case |
| Agent forgets previous context | Code | Pass messages to agents in workflow |
| Agent asks instead of searching | Prompt | Update product agent prompt |
| Orchestrator routes to wrong agent | Prompt | Fix orchestrator routing rules |
| Visualization judge wrong calculation | Judge | Handle `expected_has_chart: false` |

### Round 2 Results

| Category | Passed | Failed | Total |
|----------|--------|--------|-------|
| Analytics | 3 | 4 | 7 |
| Visualizations | 4 | 2 | 6 |
| Customer Insights | 2 | 4 | 6 |
| Chat History | 2 | 1 | 3 |
| Negative | 6 | 0 | 6 |
| **Total** | **17** | **11** | **28** |

### Continue to Round 3...

Remaining issues:

| Test Case | Score | Issue |
|-----------|-------|-------|
| `monthly_revenue` | 0.65 | SQL efficiency |
| `top_customers` | 0.0 | Wrong query |
| `line_chart_monthly_revenue` | 0.0 | Import in sandbox |
| `specific_customer_info` | 0.0 | Routing issue |
