"""
Utility functions for the Prompt Playground App
"""

import pandas as pd
from datetime import datetime
from typing import Dict, List
import streamlit as st


def format_token_count(tokens: int) -> str:
    """
    Format token count with commas for readability
    
    Args:
        tokens: Number of tokens
        
    Returns:
        Formatted string
    """
    return f"{tokens:,}"


def format_cost(cost: float) -> str:
    """
    Format cost in dollars
    
    Args:
        cost: Cost in dollars
        
    Returns:
        Formatted cost string
    """
    return f"${cost:.6f}"


def create_comparison_dataframe(results: List[Dict]) -> pd.DataFrame:
    """
    Create a comparison DataFrame from multiple results
    
    Args:
        results: List of result dictionaries
        
    Returns:
        Pandas DataFrame for comparison
    """
    data = []
    
    for idx, result in enumerate(results, 1):
        if result["success"]:
            config = result.get("config", {})
            data.append({
                "Config": f"Config {idx}",
                "Temperature": config.get("temperature", "N/A"),
                "Max Tokens": config.get("max_tokens", "N/A"),
                "Model": result["model"],
                "Tokens Used": result["total_tokens"],
                "Response Preview": result["response"][:100] + "..." if len(result["response"]) > 100 else result["response"]
            })
    
    return pd.DataFrame(data)


def get_temperature_description(temperature: float) -> str:
    """
    Get a description of what a temperature value means
    
    Args:
        temperature: Temperature value (0-2)
        
    Returns:
        Description string
    """
    if temperature < 0.3:
        return "🎯 Very Deterministic - Same input = same output (best for factual tasks)"
    elif temperature < 0.7:
        return "⚖️ Balanced - Consistent with some variation (general purpose)"
    elif temperature < 1.2:
        return "🎨 Creative - More varied responses (good for brainstorming)"
    else:
        return "🌀 Highly Random - Very unpredictable (experimental)"


def save_to_history(
    system_prompt: str,
    user_prompt: str,
    response: str,
    model: str,
    temperature: float,
    tokens: int
) -> None:
    """
    Save a prompt-response pair to session history
    
    Args:
        system_prompt: System message
        user_prompt: User message
        response: AI response
        model: Model used
        temperature: Temperature used
        tokens: Tokens used
    """
    if "history" not in st.session_state:
        st.session_state.history = []
    
    st.session_state.history.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "system_prompt": system_prompt,
        "user_prompt": user_prompt,
        "response": response,
        "model": model,
        "temperature": temperature,
        "tokens": tokens
    })


def get_history_dataframe() -> pd.DataFrame:
    """
    Get history as a DataFrame
    
    Returns:
        Pandas DataFrame of history
    """
    if "history" not in st.session_state or not st.session_state.history:
        return pd.DataFrame()
    
    return pd.DataFrame(st.session_state.history)


def clear_history() -> None:
    """Clear the session history"""
    if "history" in st.session_state:
        st.session_state.history = []


def export_history_to_csv() -> str:
    """
    Export history to CSV format
    
    Returns:
        CSV string
    """
    df = get_history_dataframe()
    if df.empty:
        return ""
    return df.to_csv(index=False)


def highlight_code_in_response(response: str) -> str:
    """
    Detect and highlight code blocks in response
    
    Args:
        response: AI response text
        
    Returns:
        Response with markdown code formatting
    """
    return response


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to a maximum length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text with ellipsis if needed
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def validate_api_key(api_key: str) -> bool:
    """
    Validate Groq API key format
    
    Args:
        api_key: API key to validate
        
    Returns:
        True if valid format, False otherwise
    """
    if not api_key:
        return False
    
    # Strip whitespace
    api_key = api_key.strip()
    
    # Groq API keys start with this prefix
    valid_prefixes = ['gsk_']
    starts_with_valid_prefix = any(api_key.startswith(prefix) for prefix in valid_prefixes)
    
    if not starts_with_valid_prefix:
        return False
    
    # Check minimum length (Groq keys are long)
    if len(api_key) < 40:
        return False
    
    # Only contains valid characters (alphanumeric and underscores)
    import re
    if not re.match(r'^[a-zA-Z0-9_]+$', api_key):
        return False
    
    return True


def get_model_info(model: str) -> Dict:
    """
    Get information about a specific model
    
    Args:
        model: Model name
        
    Returns:
        Dictionary with model information
    """
    model_info = {
        "llama-3.3-70b-versatile": {
            "name": "Llama 3.3 70B",
            "description": "Most capable Llama model, excellent for complex tasks",
            "context_window": "128K tokens",
            "cost": "FREE"
        },
        "llama-3.1-70b-versatile": {
            "name": "Llama 3.1 70B",
            "description": "Powerful and versatile, great for most tasks",
            "context_window": "128K tokens",
            "cost": "FREE"
        },
        "llama-3.1-8b-instant": {
            "name": "Llama 3.1 8B Instant",
            "description": "Fast and efficient, perfect for quick responses",
            "context_window": "128K tokens",
            "cost": "FREE"
        },
        "mixtral-8x7b-32768": {
            "name": "Mixtral 8x7B",
            "description": "Mixture of experts model, balanced performance",
            "context_window": "32K tokens",
            "cost": "FREE"
        },
        "gemma2-9b-it": {
            "name": "Gemma 2 9B",
            "description": "Google's efficient model, good for general tasks",
            "context_window": "8K tokens",
            "cost": "FREE"
        }
    }
    
    return model_info.get(model, {
        "name": model,
        "description": "Unknown model",
        "context_window": "Unknown",
        "cost": "FREE"
    })