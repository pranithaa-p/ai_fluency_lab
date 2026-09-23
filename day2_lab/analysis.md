## Part E: ReAct Agent Analysis

### Objective
To observe how a ReAct agent uses tools to retrieve course fees,
perform calculations, and compare two course-fee options.

### Problem Statement
Compare the following options:

- Option 1: CS101 + AI202 with a 10% scholarship.
- Option 2: CS101 + AI202 + DS303 with a 25% scholarship.

### ReAct Trace

| Step | Thought | Action | Observation |
|---|---|---|---|
| 1 | I need the fee for CS101. | get_course_fee("CS101") | ₹12,000 |
| 2 | I need the fee for AI202. | get_course_fee("AI202") | ₹18,000 |
| 3 | I need the fee for DS303. | get_course_fee("DS303") | ₹15,000 |
| 4 | I need the total fee for Option 1. | calculate(12000 + 18000) | ₹30,000 |
| 5 | I need to calculate Option 1 after a 10% scholarship. | calculate(30000 * 0.90) | ₹27,000 |
| 6 | I need the total fee for Option 2. | calculate(12000 + 18000 + 15000) | ₹45,000 |
| 7 | I need to calculate Option 2 after a 25% scholarship. | calculate(45000 * 0.75) | ₹33,750 |

### Final Answer
Option 1 costs ₹27,000, while Option 2 costs ₹33,750.
Therefore, Option 1 is cheaper by ₹6,750.

### Analysis
The ReAct agent alternates between reasoning, tool actions,
and observations. It retrieves course fees using the course-fee
tool and performs arithmetic using the calculator tool.
The final answer is based on the tool observations and calculations.

### Result
The ReAct agent successfully retrieved the course fees,
calculated the discounted totals, and identified the cost
difference between the two options.


## Part C: Chain-of-Thought (CoT) Comparison

### Objective
To compare direct answers with Chain-of-Thought reasoning
for three problem-solving questions.

### Observations

| Question | Direct Answer | CoT Answer | Result |
|---|---|---|---|
| Course fee instalment | ₹9,562.50 | ₹9,562.50 | Match |
| Computer sittings | 90 | 90 | Match |
| Height comparison | Ravi tallest, Priya shortest | Ravi tallest, Priya shortest | Match |

### Analysis
Direct prompting provides an answer without explicitly
showing intermediate reasoning. CoT prompting produces
intermediate reasoning steps before giving the final answer.

For all three questions, both approaches produced the
same correct final answers.

### Result
The comparison showed agreement between direct prompting
and CoT prompting for all three test questions.

## Part D: Self-Consistency

### Objective
To improve answer reliability by generating multiple
Chain-of-Thought responses and selecting the majority answer.

### Configuration
- Number of runs: 5
- Temperature: 0.8
- Question: Course fee instalment calculation

### Observations

| Run | Final Answer |
|---|---|
| 1 | ₹9,562.50 |
| 2 | ₹9,562.50 |
| 3 | ₹9,562.50 |
| 4 | ₹9,562.50 |
| 5 | ₹9,562.50 |

### Majority Answer
₹9,562.50 (5 out of 5 runs)

### Analysis
All five runs produced the same normalized numerical answer.
The majority-voting mechanism identified the correct
instalment amount.

### Result
Self-Consistency successfully returned the correct answer
of ₹9,562.50 per instalment, with 5/5 agreement.