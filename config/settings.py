"""
Configuration settings for the Prompt Playground App
"""

# OpenAI Models
AVAILABLE_MODELS = [
    "gpt-4o",
    "gpt-4o-mini",
    "gpt-4-turbo",
    "gpt-3.5-turbo",
]

DEFAULT_MODEL = "gpt-4o-mini"

# Temperature Settings
MIN_TEMPERATURE = 0.0
MAX_TEMPERATURE = 2.0
DEFAULT_TEMPERATURE = 0.7

# Token Settings
MIN_TOKENS = 50
MAX_TOKENS = 4000
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
APP_DESCRIPTION = "Experiment with different prompting techniques and LLM parameters"

# Cost per 1K tokens (approximate, update as needed)
MODEL_COSTS = {
    "gpt-4o": {"input": 0.005, "output": 0.015},
    "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
    "gpt-4-turbo": {"input": 0.01, "output": 0.03},
    "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
}