
"""Day 2 Lab: Course fee lookup and calculator tools."""

COURSE_FEES = {
    "CS101": 12000,
    "AI202": 18000,
    "DS303": 15000,
}


def get_course_fee(course_code: str):
    """Return the fee for a course code."""
    course_code = course_code.upper().strip()

    if course_code not in COURSE_FEES:
        return f"Error: Course {course_code} not found."

    return COURSE_FEES[course_code]


def calculator(expression: str):
    """Evaluate a basic arithmetic expression safely."""
    import ast
    import operator

    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
    }

    def evaluate(node):
        if isinstance(node, ast.Constant) and isinstance(
            node.value, (int, float)
        ):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in operators:
            left = evaluate(node.left)
            right = evaluate(node.right)
            return operators[type(node.op)](left, right)

        if isinstance(node, ast.UnaryOp) and isinstance(
            node.op, (ast.UAdd, ast.USub)
        ):
            value = evaluate(node.operand)
            return value if isinstance(node.op, ast.UAdd) else -value

        raise ValueError("Unsupported calculator expression")

    try:
        return evaluate(ast.parse(expression, mode="eval").body)
    except Exception as e:
        return f"Calculator error: {e}"


# Tool schemas provided to the LLM
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_course_fee",
            "description": "Get the fee for a course using its course code.",
            "parameters": {
                "type": "object",
                "properties": {
                    "course_code": {
                        "type": "string",
                        "description": "Course code, e.g. CS101",
                    }
                },
                "required": ["course_code"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Evaluate a basic arithmetic expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Arithmetic expression to calculate",
                    }
                },
                "required": ["expression"],
            },
        },
    },
]


# Map tool names to their Python functions
TOOL_FUNCTIONS = {
    "get_course_fee": get_course_fee,
    "calculator": calculator,
}