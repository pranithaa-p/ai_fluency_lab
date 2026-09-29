"""Configuration for the Day 3 AI Fluency Lab."""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Groq's OpenAI-compatible API client
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

MODEL = os.getenv("MODEL", "openai/gpt-oss-20b")


def banner(title):
    print("=" * 65)
    print(title)
    print("=" * 65)