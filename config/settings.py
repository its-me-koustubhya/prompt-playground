"""
Configuration settings for the Prompt Playground App
"""

# Groq Models (FREE!)
AVAILABLE_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-70b-versatile",
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768",
    "gemma2-9b-it",
]

DEFAULT_MODEL = "llama-3.1-8b-instant"

# Temperature Settings
MIN_TEMPERATURE = 0.0
MAX_TEMPERATURE = 2.0
DEFAULT_TEMPERATURE = 0.7

# Token Settings
MIN_TOKENS = 50
MAX_TOKENS = 8000
DEFAULT_MAX_TOKENS = 500

# Top P Settings
MIN_TOP_P = 0.0
MAX_TOP_P = 1.0
DEFAULT_TOP_P = 1.0

# Frequency Penalty
MIN_FREQUENCY_PENALTY = -2.0
MAX_FREQUENCY_PENALTY = 2.0
DEFAULT_FREQUENCY_PENALTY = 0.0

# Presence Penalty
MIN_PRESENCE_PENALTY = -2.0
MAX_PRESENCE_PENALTY = 2.0
DEFAULT_PRESENCE_PENALTY = 0.0

# App Settings
APP_TITLE = "🎨 Prompt Playground"
APP_DESCRIPTION = "Experiment with different prompting techniques using Groq's FREE API"

# Cost per 1M tokens (Groq is FREE but we track for educational purposes)
MODEL_COSTS = {
    "llama-3.3-70b-versatile": {"input": 0.0, "output": 0.0},
    "llama-3.1-70b-versatile": {"input": 0.0, "output": 0.0},
    "llama-3.1-8b-instant": {"input": 0.0, "output": 0.0},
    "mixtral-8x7b-32768": {"input": 0.0, "output": 0.0},
    "gemma2-9b-it": {"input": 0.0, "output": 0.0},
}