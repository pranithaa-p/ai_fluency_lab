# Day 4 Lab – Memory Estimation and Open Model Comparison

**Date:** 30 September 2026

## 1. Aim

The aim of this lab was to estimate the memory required by open models before downloading them, compare the estimates with actual runtime memory where possible, and compare four open model families by size, context, licence, tool-calling support, and local usability.

The lab manual states that the memory estimates are approximations intended to answer whether a model will fit, rather than predict memory usage exactly to the megabyte.

---

## 2. Memory Formula

The lab uses:

```text
weights (GB) = parameters in billions × bytes per parameter

KV cache (GB) = parameters in billions × context in K tokens × 0.02

total (GB) = (weights + KV cache) × 1.10
```

The stated bytes-per-parameter values are:

| Precision   | Bytes / parameter |
| ----------- | ----------------: |
| FP16 / BF16 |              2.00 |
| Q8_0        |              1.00 |
| Q6_K        |              0.81 |
| Q5_K_M      |              0.68 |
| Q4_K_M      |              0.57 |
| Q3_K_M      |              0.43 |

The KV-cache value is an approximation for a modern grouped-query-attention model with a 16-bit cache.

---

## 3. Part A – Hand Estimates at 8K Context

Using the formula from the lab manual:

| Model            | Precision | Weights (GB) | KV (GB) | Total (GB) |
| ---------------- | --------- | -----------: | ------: | ---------: |
| 1.5B small model | Q4_K_M    |        0.855 |   0.240 |      1.205 |
| 8B mid model     | Q4_K_M    |        4.560 |   1.280 |      6.424 |
| 8B mid model     | FP16      |       16.000 |   1.280 |     19.008 |
| 30B large model  | Q4_K_M    |       17.100 |   4.800 |     24.090 |
| 70B server model | Q4_K_M    |       39.900 |  11.200 |     56.210 |

Rounded to two decimal places, these are approximately **1.20 GB, 6.42 GB, 19.01 GB, 24.09 GB, and 56.21 GB** respectively.

### 3.1 My machine

The hardware-detection program reported:

* System RAM: **15.7 GB**
* GPU: **Intel(R) Iris(R) Xe Graphics**
* Reported GPU memory: **2.0 GB**
* Recommended dedicated-GPU budget after overhead: **1.8 GB**

The 1.8 GB figure is the conservative GPU budget used by the hardware-detection program. It is different from the laptop's total system RAM.

With an 8K context, the 1.5B Q4_K_M estimate fits within the 1.8 GB GPU budget, while the 8B Q4_K_M estimate does not. If the model is run on CPU/system RAM instead, the available-memory question is different because the laptop has 15.7 GB of reported system RAM.

### 3.2 8B Q4_K_M versus 8B FP16

At 8K context:

```text
8B Q4_K_M = 6.42 GB total
8B FP16   = 19.01 GB total
```

The estimated saving is:

```text
19.01 - 6.42 ≈ 12.59 GB
```

Therefore, quantization from FP16 to Q4_K_M greatly reduces the memory requirement, at the cost of some model precision/quality.

### 3.3 6 GB graphics card

At 8K context:

```text
8B Q4_K_M ≈ 6.42 GB
```

Therefore an 8B Q4_K_M model is slightly above a 6 GB budget.

A 7B Q4_K_M model would be approximately:

```text
weights = 7 × 0.57 = 3.99 GB
KV      = 7 × 8 × 0.02 = 1.12 GB
total   = (3.99 + 1.12) × 1.10 ≈ 5.62 GB
```

So a 7B Q4_K_M model is approximately the largest size in this range that fits a 6 GB budget under the lab's formula.

---

## 4. Part B – Python Estimator

The file `vram_estimate.py` implements the formula as Python functions and prints:

1. Several model sizes at Q4_K_M.
2. The same 8B model at different context lengths.
3. The same 8B model at different quantization levels.

The program therefore demonstrates that memory depends not only on the number of parameters, but also on context length and quantization.

---

## 5. Experiment 1 – Context Length

For an 8B Q4_K_M model:

| Context | Total estimate |
| ------: | -------------: |
|      4K |        5.72 GB |
|      8K |        6.42 GB |
|     32K |       10.65 GB |
|    128K |       27.54 GB |

The **weights stay at 4.56 GB** because the model itself has not changed.

The part that grows is the **KV cache**. A larger context means that more previous tokens have to be represented for attention, so the KV cache consumes more memory.

This matters for agents because tool results, previous messages, and intermediate information can accumulate in the conversation. A long-running agent can therefore require substantially more memory even when the model weights remain unchanged.

---

## 6. Experiment 2 – Quantization

For an 8B model at 8K context:

| Quantization |  Weights |    Total |
| ------------ | -------: | -------: |
| Q3_K_M       |  3.44 GB |  5.19 GB |
| Q4_K_M       |  4.56 GB |  6.42 GB |
| Q5_K_M       |  5.44 GB |  7.39 GB |
| Q8_0         |  8.00 GB | 10.21 GB |
| FP16         | 16.00 GB | 19.01 GB |

At an 8 GB memory budget, Q3_K_M, Q4_K_M, and Q5_K_M fit according to the lab's estimator, while Q8_0 and FP16 do not.

Q4_K_M is a practical middle point because it uses substantially less memory than FP16 while retaining more precision than Q3_K_M.

---

## 7. Part C – Check Against Reality

The lab manual asks for:

```powershell
ollama list
```

to compare model size on disk with the estimated weights, and:

```powershell
ollama run <model>
```

followed in a second terminal by:

```powershell
ollama ps
```

to compare actual runtime memory with the estimated total.

**Machine-specific Ollama values should only be entered after running these commands on the actual machine. They are not fabricated in this report.**

If no local Ollama model is available, the lab manual allows students using the Groq or Hugging Face option to complete Parts A, B, D and E and pair with another student for Part C.

---

# 8. Part D – Four Model Comparison

The four required families are Qwen, Mistral, IBM Granite, and OpenAI gpt-oss.

Representative models selected:

1. Qwen3-8B
2. Mistral-7B-Instruct-v0.3
3. Granite-4.0-Micro
4. gpt-oss-20b

## 8.1 Comparison Table

| Field                      | Qwen3-8B                         | Mistral-7B-Instruct-v0.3         | Granite-4.0-Micro                | gpt-oss-20b                      |
| -------------------------- | -------------------------------- | -------------------------------- | -------------------------------- | -------------------------------- |
| Publisher                  | Alibaba / Qwen                   | Mistral AI                       | IBM Granite                      | OpenAI                           |
| Parameters                 | 8.2B                             | 7B                               | 3B                               | 20.9B total / 3.6B active        |
| Architecture               | Dense                            | Dense                            | Dense                            | MoE                              |
| Context window             | 32K native; 131K with YaRN       | 32K                              | 128K                             | 128K                             |
| Licence                    | Apache 2.0                       | Apache 2.0                       | Apache 2.0                       | Apache 2.0                       |
| Commercial use             | Permitted under Apache 2.0 terms | Permitted under Apache 2.0 terms | Permitted under Apache 2.0 terms | Permitted under Apache 2.0 terms |
| Tool/function calling      | Explicitly supported             | Explicitly supported             | Explicitly supported             | Explicitly supported             |
| Ollama availability        | Yes                              | Yes                              | Yes                              | Yes                              |
| Representative Ollama size | ~5.2 GB                          | ~4.4 GB                          | ~2.1 GB                          | ~14 GB                           |
| 8K Q4_K_M estimate         | ~6.42 GB                         | ~5.62 GB                         | ~2.41 GB                         | ~16.06 GB*                       |

*The simple lab formula treats the parameter count directly and therefore does not model the special MoE memory behavior of gpt-oss. The official model information describes gpt-oss-20b as a mixture-of-experts model with 20B-class total parameters and 3.6B active parameters per token.

### Model-card observations

**Qwen3-8B:** The model card lists approximately 8B parameters, a long context window, and support for agent/tool use. It is licensed Apache 2.0.

**Mistral-7B-Instruct-v0.3:** The model card lists 7B parameters and explicitly documents function calling. It is licensed Apache 2.0.

**Granite-4.0-Micro:** The model card describes it as a 3B long-context instruct model with tool-calling capabilities. It is licensed Apache 2.0.

**gpt-oss-20b:** The model information describes it as a MoE model with approximately 20B total parameters and 3.6B active parameters, a 128K context window, Apache 2.0 licensing, and agentic capabilities including function calling.

---

## 8.2 Licence Questions

### Did two selected models have different licences?

No. The four selected models use **Apache 2.0** licensing.

### Which could be used in a product?

The selected models use Apache 2.0, which permits commercial use subject to the licence terms, notices, and conditions.

### Which has special conditions?

For the selected models, no additional model-specific licence restriction was identified beyond the Apache 2.0 terms. However, the model card and licence should always be checked again before deployment because terms can change.

### Which cards explicitly mention tool/function calling?

All four selected model families document tool/function-calling or agentic tool use.

### Documented limitation

Mistral's model information documents limitations that should be considered when deploying the model, including the absence of built-in moderation mechanisms.

---

# 9. Part E – Recommendations

## 9.1 8 GB Laptop, No GPU

For an 8 GB laptop running the Unit 1 agent labs, a small Apache 2.0 model with tool-calling support is appropriate. A smaller Qwen3 model is a practical candidate because the Qwen3 family supports tool use and smaller versions are available through Ollama. A lower parameter count and Q4_K_M quantization leave more memory for the operating system and the agent's context.

## 9.2 24 GB GPU Server Serving Multiple Students

A shared 24 GB GPU changes the problem because memory must account for concurrent users and context. A larger model may fit for one session but leave insufficient memory for many simultaneous users. A smaller Granite model can leave more headroom for multiple users and longer contexts.

## 9.3 Public Capstone Project

For a project that will be published on GitHub and demonstrated publicly, the licence must be clear and suitable for redistribution and commercial use. The selected models use Apache 2.0, which provides a permissive licence framework. The exact model version and licence should be recorded in the project documentation at the time of release.

---

# 10. Discussion Questions

### 1. Why can the same model stop fitting even though its weights never change?

The model weights remain constant, but the KV cache grows with context length. Tool results and conversation history increase the amount of context, which increases runtime memory requirements.

### 2. 14B Q4 or 8B Q8 on the same hardware?

The decision should be tested using the actual workload, context length, latency, quality, and available memory. Parameter count alone is not enough because quantization and KV-cache size also affect memory.

### 3. Why can the estimate and `ollama ps` disagree?

Three possible reasons are:

1. Ollama may use a different context length from the estimate.
2. Runtime memory and allocator overhead can differ.
3. Different model architectures can have different KV-cache behavior.

### 4. Is a model useless if its licence forbids commercial use?

No. It can still be useful for learning, research, or scenarios where commercial use is not required. However, it would not be suitable for a product where the licence restriction conflicts with the intended use.

### 5. What can be lost by using a free cloud model instead of running locally?

Two important trade-offs are:

1. Data and prompts are sent to an external service rather than staying local.
2. The application depends on network access and the provider's service limits, availability, and policies.

---

# 11. Observations

## 11.1 Hand Estimates vs Program

| Model       | Hand total | Program total | Difference |
| ----------- | ---------: | ------------: | ---------: |
| 1.5B Q4_K_M |   1.205 GB |       1.20 GB |   ~0.00 GB |
| 8B Q4_K_M   |   6.424 GB |       6.42 GB |   ~0.00 GB |
| 8B FP16     |  19.008 GB |      19.01 GB |   ~0.00 GB |
| 30B Q4_K_M  |  24.090 GB |      24.09 GB |   ~0.00 GB |
| 70B Q4_K_M  |  56.210 GB |      56.21 GB |   ~0.00 GB |

The small differences are only due to rounding.

## 11.2 Estimate vs Reality

This section must contain the actual output of `ollama list` and `ollama ps` if Part C is performed.

| Model on machine                        | `ollama list` size | `ollama ps` size | Total estimate |
| --------------------------------------- | -----------------: | ---------------: | -------------: |
| To be filled from actual machine output |                  — |                — |              — |

## 11.3 Effect of Context and Quantization

**Largest context for an 8B Q4 model:** Under an 8 GB budget, 8K fits at about 6.42 GB, while 32K requires about 10.65 GB and therefore does not fit.

**Quantization choice:** Q4_K_M is a practical balance between memory usage and quality. Q3_K_M uses less memory but has greater quality loss; Q5_K_M uses more memory.

**Largest model at Q4_K_M with 8K context:** Under an 8 GB budget, the 8B model fits according to the lab estimator at about 6.42 GB. Under the laptop's reported 1.8 GB GPU budget, only the 1.5B example fits comfortably.

---

# 12. Final Result

The lab demonstrated that model memory depends on parameters, quantization, context length, and runtime overhead. The experiments showed that increasing context length increases KV-cache memory even when the model weights remain unchanged, while lower-bit quantization reduces the weight memory requirement. The comparison of Qwen, Mistral, Granite, and gpt-oss also showed why model selection depends not only on size and performance but also on tool-calling support, deployment requirements, and licence terms.

---

## Sources Used for Part D

* Official Qwen model card
* Official Mistral model card
* Official IBM Granite model card
* Official OpenAI gpt-oss model card
* Official Ollama library pages for Qwen, Mistral, Granite, and gpt-oss

**Research date:** 30 September 2026.
