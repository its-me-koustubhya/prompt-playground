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
    # This is a simple implementation
    # In a real app, you might use more sophisticated parsing
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
    Validate OpenAI API key format
    
    Args:
        api_key: API key to validate
        
    Returns:
        True if valid format, False otherwise
    """
    if not api_key:
        return False
    
    # OpenAI API keys start with 'sk-' and are at least 20 characters
    if api_key.startswith("sk-") and len(api_key) > 20:
        return True
    
    return False


def get_model_info(model: str) -> Dict:
    """
    Get information about a specific model
    
    Args:
        model: Model name
        
    Returns:
        Dictionary with model information
    """
    model_info = {
        "gpt-4o": {
            "name": "GPT-4o",
            "description": "Most advanced multimodal model, great for complex tasks",
            "context_window": "128K tokens"
        },
        "gpt-4o-mini": {
            "name": "GPT-4o Mini",
            "description": "Fast and affordable, great for most tasks",
            "context_window": "128K tokens"
        },
        "gpt-4-turbo": {
            "name": "GPT-4 Turbo",
            "description": "Previous generation high-performance model",
            "context_window": "128K tokens"
        },
        "gpt-3.5-turbo": {
            "name": "GPT-3.5 Turbo",
            "description": "Fast and economical, good for simple tasks",
            "context_window": "16K tokens"
        }
    }
    
    return model_info.get(model, {
        "name": model,
        "description": "Unknown model",
        "context_window": "Unknown"
    })