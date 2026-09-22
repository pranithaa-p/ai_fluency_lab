
"""System 2: Rule-based workflow. No LLM."""

import re
from config import COURSE_FEES, QUESTIONS, banner


def workflow(question):
    # Identify course codes in the question
    codes = re.findall(r"[A-Z]{2}\d{3}", question.upper())

    # Retrieve fees for valid course codes
    fees = [
        COURSE_FEES[code]
        for code in codes
        if code in COURSE_FEES
    ]

    if not fees:
        return "Sorry, I can only answer questions about course fees."

    text = question.lower()

    # Rule 1: Calculate total fee
    if "total" in text:
        total = sum(fees)

        # Apply scholarship if specified
        percent = re.search(r"(\d+)\s*%", text)

        if "scholarship" in text and percent:
            discount = int(percent.group(1))
            total = total * (1 - discount / 100)

        return f"Total fee: Rs. {total:,.0f}"

    # Rule 2: Return fee for a single course
    if len(fees) == 1:
        return f"Fee for {codes[0]}: Rs. {fees[0]:,}"

    # No matching rule
    return "Sorry, I do not have a rule for this type of question."


if __name__ == "__main__":
    banner("SYSTEM 2: RULE-BASED WORKFLOW")

    for question in QUESTIONS:
        print("Q:", question)
        print("A:", workflow(question))
        print("-" * 70)