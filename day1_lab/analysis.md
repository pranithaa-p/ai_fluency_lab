
# Analysis: College Fee Assistant

## 3.1 System 1 – Plain Chatbot

The plain chatbot uses an LLM to generate responses without accessing
private college fee data or external tools.

For fee-related questions, it asks for additional information because
it does not have access to the predefined fee database. However, it can
generate general responses, such as a welcome message for new AI students.

## 3.2 System 2 – Rule-Based Workflow

The rule-based workflow uses predefined Python rules to process user
queries and generate responses without using an LLM.

It correctly answers supported fee questions, including calculating
the total fee after a scholarship. However, it cannot answer questions
that are not covered by its predefined rules, such as comparing fees
or generating a welcome message.

## 3.3 System 3 – AI Agent

The AI agent combines an LLM with Python tools and a tool-execution loop.

It uses the get_course_fee tool to retrieve course fees and the
calculator tool to perform arithmetic operations.

The agent successfully retrieved the fees for AI202, CS101, and DS303.
It calculated the total fee after a 10% scholarship as Rs. 27,000
and identified that DS303 costs Rs. 3,000 more than CS101.

The agent also generated a welcome message without requiring a tool.

## 3.4 Comparison and Conclusion

The three systems differ in how they process queries and access
information.

- The plain chatbot generates responses using an LLM but has no access
  to the private fee database.
- The rule-based workflow provides predictable results for supported
  queries but is limited to predefined rules.
- The AI agent dynamically selects tools, retrieves data, performs
  calculations, and generates contextual responses.

This experiment demonstrates how an AI agent can combine the language
understanding capabilities of an LLM with external tools to solve
structured, data-dependent tasks.