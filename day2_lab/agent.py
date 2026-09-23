"""Day 2: ReAct agent with tool-calling and trace output."""

import json
from config import client, MODEL
from tools import TOOLS, TOOL_FUNCTIONS


SYSTEM_PROMPT = """
You are a helpful course-fee assistant.

Use the available tools to look up course fees and perform calculations.
For questions involving multiple fees or scholarships, use the tools
instead of guessing.

Think step by step, observe tool results, and give a clear final answer.
"""


def agent(question, max_steps=8):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]

    for step in range(max_steps):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
        )

        message = response.choices[0].message

        # Add the assistant's response to the conversation
        messages.append(message.model_dump(exclude_none=True))

        # If no tool is requested, return the final answer
        if not message.tool_calls:
            return message.content or "No final answer was returned."

        # Execute each requested tool
        for tool_call in message.tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            print(f"\n[Step {step + 1}] ACTION: {function_name}")
            print(f"INPUT: {arguments}")

            function = TOOL_FUNCTIONS.get(function_name)

            if function is None:
                result = f"Error: Unknown tool '{function_name}'"
            else:
                try:
                    result = function(**arguments)
                except Exception as error:
                    result = f"Tool error: {error}"

            print(f"OBSERVATION: {result}")

            # Send the tool result back to the model
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result),
            })

    return "Stopped: maximum tool-calling steps reached."


if __name__ == "__main__":
    question = (
    "The course fees are CS101, AI202, and DS303. "
    "Use the get_course_fee tool to retrieve their fees. "
    "Compare CS101 + AI202 after a 10% scholarship "
    "against CS101 + AI202 + DS303 after a 25% scholarship. "
    "Use the calculator tool for both totals and tell me "
    "which option is cheaper and by how much."
)

    print("QUESTION:", question)
    print("\n--- ReAct Trace ---")

    answer = agent(question)

    print("\nFINAL ANSWER:", answer)