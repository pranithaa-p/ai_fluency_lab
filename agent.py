
"""System 3: AI agent = LLM + tools + loop."""

import json
from config import client, MODEL, QUESTIONS, banner
from tools import TOOLS, TOOL_FUNCTIONS

SYSTEM_PROMPT = """
You are a college fee assistant.
Never guess a course fee. Always use get_course_fee
to retrieve the fee for each course.
Use calculator for arithmetic, totals, and scholarships.
Available course codes: CS101, AI202, DS303.
If no tool is needed, answer directly.
Explain the result clearly.
"""

def agent(question, max_steps=6, verbose=True):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question}
    ]

    for step in range(1, max_steps + 1):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            temperature=0
        )

        message = response.choices[0].message

        if not message.tool_calls:
            return message.content or "The model returned no answer."

        messages.append({
            "role": "assistant",
            "content": message.content,
            "tool_calls": [
                call.model_dump(exclude_none=True)
                for call in message.tool_calls
            ]
        })

        for call in message.tool_calls:
            name = call.function.name

            try:
                arguments = json.loads(
                    call.function.arguments or "{}"
                )
                function = TOOL_FUNCTIONS.get(name)

                if function is None:
                    result = f"Unknown tool: {name}"
                else:
                    result = function(**arguments)

            except Exception as error:
                result = f"Tool error: {error}"

            if verbose:
                print(
                    f"  step {step}: {name}"
                    f"({call.function.arguments}) -> {result}"
                )

            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": str(result)
            })

    return "Stopped: maximum steps reached without a final answer."


if __name__ == "__main__":
    banner("SYSTEM 3: AI AGENT")

    for question in QUESTIONS:
        print("Q:", question)
        print("A:", agent(question))
        print("-" * 70)