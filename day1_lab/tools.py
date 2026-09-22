
"""Tools for the College Fee Assistant AI agent."""

import ast
import operator

from config import COURSE_FEES


def get_course_fee(course_code: str) -> str:
    """Retrieve the fee for a course."""

    code = course_code.strip().upper()

    if code not in COURSE_FEES:
        return f"Unknown course code: {code}"

    return f"{code} fee is Rs. {COURSE_FEES[code]}"


# Safe arithmetic operators (no eval)
OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def safe_calculate(expression: str):
    """Evaluate basic arithmetic safely."""

    def evaluate(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in OPS:
            return OPS[type(node.op)](
                evaluate(node.left),
                evaluate(node.right)
            )

        if isinstance(node, ast.UnaryOp) and isinstance(
            node.op, (ast.UAdd, ast.USub)
        ):
            value = evaluate(node.operand)
            return value if isinstance(node.op, ast.UAdd) else -value

        raise ValueError("Unsupported arithmetic expression")

    tree = ast.parse(expression, mode="eval")
    return evaluate(tree.body)


def calculator(expression: str) -> str:
    """Perform arithmetic using the safe calculator."""

    try:
        result = safe_calculate(expression)
        return str(result)
    except Exception as error:
        return f"Calculator error: {error}"


# Map tool names to Python functions
TOOL_FUNCTIONS = {
    "get_course_fee": get_course_fee,
    "calculator": calculator,
}


# Tool descriptions provided to the LLM
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_course_fee",
            "description": "Get the actual fee for a course code.",
            "parameters": {
                "type": "object",
                "properties": {
                    "course_code": {
                        "type": "string",
                        "description": "Course code such as CS101"
                    }
                },
                "required": ["course_code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Calculate a mathematical expression safely.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Arithmetic expression"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]


if __name__ == "__main__":
    print(get_course_fee("AI202"))
    print(calculator("(12000 + 18000) * 0.9"))