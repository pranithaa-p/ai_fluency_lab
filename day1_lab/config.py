"""Shared configuration for the College Fee Assistant lab."""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load settings from .env
load_dotenv()

PROVIDER = os.getenv("PROVIDER", "groq").strip().lower()

if PROVIDER == "groq":
    BASE_URL = "https://api.groq.com/openai/v1"
    API_KEY = os.getenv("GROQ_API_KEY", "").strip()
    MODEL = os.getenv("MODEL", "openai/gpt-oss-20b")

else:
    raise SystemExit(
        f"Unknown provider: {PROVIDER}. This setup uses Groq."
    )

if not API_KEY:
    raise SystemExit(
        "No API key found. Check GROQ_API_KEY in your .env file."
    )

# Create the Groq client using the OpenAI SDK
client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY
)

# Private college fee data for the lab
COURSE_FEES = {
    "CS101": 12000,
    "AI202": 18000,
    "DS303": 15000
}

# Common questions for all three systems
QUESTIONS = [
    "What is the fee for AI202?",
    "What is the total fee for CS101 and AI202 after a 10% scholarship?",
    "Is DS303 more expensive than CS101, and by how much?",
    "Write a two-line welcome message for new AI students."
]


def banner(system_name):
    print(
        f"\n=== {system_name} | "
        f"provider: {PROVIDER} | model: {MODEL} ===\n"
    )