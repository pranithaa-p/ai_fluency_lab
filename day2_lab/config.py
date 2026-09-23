
"""Configuration for the Day 2 AI Fluency Lab."""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from day2_lab/.env
load_dotenv()

# Groq's OpenAI-compatible API client
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

MODEL = os.getenv("MODEL", "openai/gpt-oss-20b")