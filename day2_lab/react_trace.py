
"""Day 2, Part D: print the agent's real ReAct trace to compare with your paper trace."""

from agent import agent

QUESTION = (
    "The courses are CS101, AI202, and DS303. "
    "Which is cheaper: CS101 + AI202 with a 10% scholarship, "
    "or all three courses with a 25% scholarship? "
    "Use get_course_fee to retrieve each fee and calculator "
    "to calculate both totals and the difference. "
    "Give the final answer in Indian rupees (₹)."
)

print("QUESTION:", QUESTION, "\n")
print("--- the agent's actions and observations ---")

answer = agent(QUESTION, max_steps=12)

print("\nFINAL ANSWER:", answer)