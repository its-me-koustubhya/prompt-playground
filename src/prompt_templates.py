"""
Pre-built prompt templates demonstrating different prompting techniques
"""

PROMPT_TEMPLATES = {
    "Zero-Shot": {
        "system": "You are a helpful AI assistant.",
        "user": "Translate the following to French: Hello, how are you?",
        "description": "Basic prompt without examples"
    },
    
    "Few-Shot Learning": {
        "system": "You are a sentiment analyzer.",
        "user": """Classify the sentiment of these reviews:

        Example 1:
        Review: "This product is amazing! Best purchase ever."
        Sentiment: Positive

        Example 2:
        Review: "Terrible quality. Very disappointed."
        Sentiment: Negative

        Example 3:
        Review: "It's okay, nothing special."
        Sentiment: Neutral

        Now classify this:
        Review: "Absolutely love it! Exceeded my expectations."
        Sentiment:""",
        "description": "Provides examples before the actual task"
    },
    
    "Chain-of-Thought": {
        "system": "You are a math tutor who explains reasoning step-by-step.",
        "user": """Solve this problem step by step:

          Problem: A store has 23 apples. They sell 8 apples in the morning and 12 apples in the afternoon. 
          Then they receive a delivery of 30 apples. How many apples do they have now?

          Let's think through this step by step:""",
        "description": "Encourages the model to show reasoning process"
    },
    
    "Role-Based": {
        "system": "You are a professional copywriter specializing in engaging social media content.",
        "user": "Write a catchy Instagram caption for a photo of a sunset at the beach.",
        "description": "Assigns a specific role/persona to the AI"
    },
    
    "Constrained Output": {
        "system": "You are a concise assistant who follows formatting rules strictly.",
        "user": """Summarize the following article in exactly 3 bullet points:

          Article: "Artificial Intelligence is transforming industries worldwide. From healthcare to finance, 
          AI systems are improving efficiency and decision-making. 
          However, ethical concerns about bias and privacy remain important considerations."

          Format your response as:
          • Point 1
          • Point 2
          • Point 3""",
        "description": "Specifies exact output format and constraints"
    },
    
    "Creative Writing": {
        "system": "You are a creative storyteller with a vivid imagination.",
        "user": "Write a short story (3 paragraphs) about a robot who discovers emotions for the first time.",
        "description": "Open-ended creative task with high temperature recommended"
    },
    
    "Code Generation": {
        "system": "You are an expert Python programmer who writes clean, well-documented code.",
        "user": """Write a Python function that:
                  - Takes a list of numbers as input
                  - Returns the median value
                  - Includes docstring and type hints
                  - Handles edge cases""",
        "description": "Technical task with specific requirements"
    },
    
    "Structured Data Extraction": {
        "system": "You are a data extraction specialist. Always return valid JSON.",
        "user": """Extract key information from this text and return as JSON:

                    Text: "John Smith, 35 years old, works as a Software Engineer at TechCorp in San Francisco. 
                    He can be reached at john.smith@email.com or 555-0123."

                    Return JSON with fields: name, age, occupation, company, location, email, phone""",
        "description": "Extracts and structures information from text"
    },
    
    "Negative Prompting": {
        "system": "You are a professional business writer.",
        "user": """Write a professional email declining a meeting invitation.

                    Requirements:
                    - Be polite and respectful
                    - Provide a brief reason
                    - Suggest an alternative

                    Do NOT:
                    - Use overly casual language
                    - Make excuses
                    - Be too lengthy (keep under 100 words)""",
        "description": "Specifies what NOT to do"
    },
    
    "ReAct (Reasoning + Acting)": {
        "system": "You are a problem-solving assistant. For each problem, think through your reasoning and propose actions.",
        "user": """I want to learn web development but don't know where to start.

                    Please respond using this format:
                    Thought: [Your reasoning about the situation]
                    Action: [Specific steps to take]
                    Observation: [Expected outcomes or considerations]""",
        "description": "Combines reasoning with actionable steps"
    }
}


def get_template(template_name: str) -> dict:
    """
    Get a specific prompt template by name
    
    Args:
        template_name: Name of the template
        
    Returns:
        Dictionary containing system, user, and description
    """
    return PROMPT_TEMPLATES.get(template_name, PROMPT_TEMPLATES["Zero-Shot"])


def get_all_template_names() -> list:
    """
    Get list of all available template names
    
    Returns:
        List of template names
    """
    return list(PROMPT_TEMPLATES.keys())


def get_template_description(template_name: str) -> str:
    """
    Get description of a specific template
    
    Args:
        template_name: Name of the template
        
    Returns:
        Description string
    """
    template = PROMPT_TEMPLATES.get(template_name, {})
    return template.get("description", "No description available")