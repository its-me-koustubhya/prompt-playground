"""
Groq API client wrapper using the latest Groq Python SDK
"""

import os
from typing import Dict, Optional
from groq import Groq
from dotenv import load_dotenv
import tiktoken

# Load environment variables
load_dotenv()


class GroqClient:
    """
    Wrapper for Groq API interactions
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Groq client
        
        Args:
            api_key: Groq API key (optional, will use env var if not provided)
        """
        # Use provided API key or fall back to environment variable
        if api_key is None:
            api_key = os.getenv("GROQ_API_KEY")
        
        if not api_key:
            raise ValueError("API key must be provided either as parameter or in GROQ_API_KEY environment variable")
        
        # Initialize client using the Groq SDK
        self.client = Groq(api_key=api_key)
    
    def test_api_key(self) -> Dict:
        """
        Test if the API key is valid by making a minimal API call
        
        Returns:
            Dictionary with success status and message
        """
        try:
            # Make a minimal API call to test the key
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5
            )
            return {
                "valid": True,
                "message": "API key is valid and working"
            }
        except Exception as e:
            error_message = str(e)
            
            # Parse common error types
            if "invalid" in error_message.lower() or "unauthorized" in error_message.lower():
                return {
                    "valid": False,
                    "message": "Invalid API key. Please check your key and try again."
                }
            elif "rate_limit" in error_message.lower():
                return {
                    "valid": True,  # Key is valid, just rate limited
                    "message": "API key is valid (rate limit reached, but key works)"
                }
            else:
                return {
                    "valid": False,
                    "message": f"API key validation failed: {error_message}"
                }
    
    def count_tokens(self, text: str, model: str = "llama-3.1-8b-instant") -> int:
        """
        Count the number of tokens in a text string
        Uses tiktoken as an approximation for Llama models
        
        Args:
            text: The text to count tokens for
            model: The model (not used, here for compatibility)
            
        Returns:
            Number of tokens (approximate)
        """
        try:
            # Use cl100k_base encoding as approximation for Llama models
            encoding = tiktoken.get_encoding("cl100k_base")
            return len(encoding.encode(text))
        except Exception:
            # Fallback: rough estimate (1 token ≈ 4 characters)
            return len(text) // 4
    
    def generate_completion(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str = "llama-3.1-8b-instant",
        temperature: float = 0.7,
        max_tokens: int = 500,
        top_p: float = 1.0,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0
    ) -> Dict:
        """
        Generate a completion using Groq API
        
        Args:
            system_prompt: System message (sets behavior)
            user_prompt: User message (the actual prompt)
            model: Model to use
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens in response
            top_p: Nucleus sampling parameter
            frequency_penalty: Penalty for token frequency
            presence_penalty: Penalty for token presence
            
        Returns:
            Dictionary containing response and metadata
        """
        try:
            # Make API call using Groq SDK
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty
            )
            
            # Extract response data
            completion_text = response.choices[0].message.content
            
            # Get token usage from response
            prompt_tokens = response.usage.prompt_tokens
            completion_tokens = response.usage.completion_tokens
            total_tokens = response.usage.total_tokens
            
            return {
                "success": True,
                "response": completion_text,
                "model": model,
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens,
                "finish_reason": response.choices[0].finish_reason
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response": None
            }
    
    def compare_completions(
        self,
        system_prompt: str,
        user_prompt: str,
        configs: list[Dict]
    ) -> list[Dict]:
        """
        Generate multiple completions with different configurations for comparison
        
        Args:
            system_prompt: System message
            user_prompt: User message
            configs: List of configuration dictionaries
            
        Returns:
            List of response dictionaries
        """
        results = []
        
        for config in configs:
            result = self.generate_completion(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                **config
            )
            result["config"] = config
            results.append(result)
        
        return results
    
    def calculate_cost(
        self,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
        costs: Dict
    ) -> float:
        """
        Calculate the cost of an API call (Groq is FREE!)
        
        Args:
            model: Model used
            prompt_tokens: Number of input tokens
            completion_tokens: Number of output tokens
            costs: Dictionary of model costs
            
        Returns:
            Total cost in dollars (always 0.0 for Groq)
        """
        # Groq is FREE!
        return 0.0


# Convenience function for quick testing
def quick_test():
    """Quick test of the API client"""
    try:
        client = GroqClient()
        result = client.generate_completion(
            system_prompt="You are a helpful assistant.",
            user_prompt="Say 'Hello, World!' in a creative way.",
            model="llama-3.1-8b-instant",
            temperature=0.7,
            max_tokens=50
        )
        
        if result["success"]:
            print("✅ API Test Successful!")
            print(f"Response: {result['response']}")
            print(f"Tokens used: {result['total_tokens']}")
        else:
            print(f"❌ API Test Failed: {result['error']}")
            
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    quick_test()