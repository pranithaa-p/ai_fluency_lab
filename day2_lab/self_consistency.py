"""Day 2, Part D: Self-Consistency."""

from collections import Counter
from config import client, MODEL
from cot_compare import COT_PROMPT, QUESTIONS

RUNS = 5
TEMPERATURE = 0.8

import re

def final_answer(text):
    """Extract and normalize the numerical final answer."""
    lines = text.splitlines()

    answer_line = next(
        (
            line for line in reversed(lines)
            if "final answer" in line.lower()
        ),
        lines[-1] if lines else ""
    )

    match = re.search(r"\d[\d,]*(?:\.\d+)?", answer_line)

    if match:
        value = float(match.group().replace(",", ""))
        return f"₹{value:,.2f}"

    return answer_line.strip() or "(empty)"


def run_many(question, runs=RUNS, temperature=TEMPERATURE):
    answers = []

    for attempt in range(1, runs + 1):
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": COT_PROMPT},
                {"role": "user", "content": question},
            ],
            temperature=temperature,
        )

        answer = final_answer(
            response.choices[0].message.content or ""
        )

        print(f"Run {attempt}: {answer}")
        answers.append(answer)

    return answers


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("SELF-CONSISTENCY")
    print("=" * 60)

    question = QUESTIONS[0]
    print("QUESTION:", question, "\n")

    answers = run_many(question)

    winner, count = Counter(answers).most_common(1)[0]

    print(
        f"\nMajority answer ({count} of {len(answers)} runs): "
        f"{winner}"
    )