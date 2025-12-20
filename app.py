"""
Prompt Playground - Main Streamlit Application
An interactive tool for experimenting with LLM prompting techniques
"""

import streamlit as st
import os
from dotenv import load_dotenv

# Import custom modules
from src.api_client import GroqClient
from src.prompt_templates import get_all_template_names, get_template, get_template_description
from src.utils import (
    format_token_count, format_cost, get_temperature_description,
    save_to_history, get_history_dataframe, clear_history,
    export_history_to_csv, get_model_info, validate_api_key
)
from config.settings import (
    AVAILABLE_MODELS, DEFAULT_MODEL, MIN_TEMPERATURE, MAX_TEMPERATURE,
    DEFAULT_TEMPERATURE, MIN_TOKENS, MAX_TOKENS, DEFAULT_MAX_TOKENS,
    MIN_TOP_P, MAX_TOP_P, DEFAULT_TOP_P, MIN_FREQUENCY_PENALTY,
    MAX_FREQUENCY_PENALTY, DEFAULT_FREQUENCY_PENALTY, MIN_PRESENCE_PENALTY,
    MAX_PRESENCE_PENALTY, DEFAULT_PRESENCE_PENALTY, APP_TITLE,
    APP_DESCRIPTION, MODEL_COSTS
)

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Prompt Playground",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .stAlert {
        margin-top: 1rem;
    }
    .privacy-notice {
        background-color: #0b1011;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .warning-banner {
        background-color: #3c351d;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin-bottom: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if "history" not in st.session_state:
        st.session_state.history = []
    if "current_response" not in st.session_state:
        st.session_state.current_response = None
    if "comparison_mode" not in st.session_state:
        st.session_state.comparison_mode = False
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""
    if "api_key_valid" not in st.session_state:
        st.session_state.api_key_valid = False
    if "env_key_validated" not in st.session_state:
        st.session_state.env_key_validated = False
    if "env_key_validation_result" not in st.session_state:
        st.session_state.env_key_validation_result = None
    if "manual_key_validated" not in st.session_state:
        st.session_state.manual_key_validated = {}  # Dict to track validated keys


def render_api_key_input():
    """Render API key input section and return validity status"""
    st.sidebar.header("🔑 API Configuration")
    
    # Check if API key exists in environment
    env_api_key = os.getenv("GROQ_API_KEY")
    
    # Try to validate .env key if it exists
    if env_api_key:
        # Check format first
        if not validate_api_key(env_api_key):
            st.sidebar.error("❌ .env API key has invalid format (must start with 'gsk_' and be at least 40 characters)")
            st.sidebar.info("👇 Please enter a valid API key below")
        else:
            # Format is good, now validate with API
            if not st.session_state.get("env_key_validated", False):
                # First time checking this .env key
                with st.sidebar:
                    with st.spinner("🔍 Validating API key from .env file..."):
                        try:
                            temp_client = GroqClient(api_key=env_api_key)
                            validation = temp_client.test_api_key()
                            st.session_state.env_key_validation_result = validation
                            st.session_state.env_key_validated = True
                        except Exception as e:
                            st.session_state.env_key_validation_result = {
                                "valid": False,
                                "message": f"Failed to validate: {str(e)}"
                            }
                            st.session_state.env_key_validated = True
            
            # Check the validation result
            validation = st.session_state.get("env_key_validation_result", {})
            if validation.get("valid", False):
                st.sidebar.success("✅ Using validated API key from .env file")
                st.session_state.api_key = env_api_key
                st.session_state.api_key_valid = True
                return True, env_api_key
            else:
                # Validation failed
                error_msg = validation.get("message", "Unknown error")
                st.sidebar.error(f"❌ .env API key validation failed")
                with st.sidebar.expander("🔍 Error Details"):
                    st.error(error_msg)
                st.sidebar.info("👇 Please enter a valid API key below")
                # Continue to manual input
    
    # Privacy notice
    st.sidebar.markdown("""
        <div class="privacy-notice">
            <strong>🔒 Privacy Notice</strong><br>
            Your API key is only stored in your browser's session memory and is never saved to disk or transmitted to any server other than Groq's API.
        </div>
    """, unsafe_allow_html=True)
    
    # API key input - don't pre-fill with env key if it failed
    default_value = ""
    if st.session_state.api_key and st.session_state.api_key_valid:
        default_value = st.session_state.api_key
    
    api_key_input = st.sidebar.text_input(
        "Enter your Groq API Key",
        type="password",
        value=default_value,
        placeholder="gsk_...",
        help="Your API key starts with 'gsk_'. Get it FREE from https://console.groq.com/keys",
        key="api_key_input"
    )
    
    if api_key_input:
        # Check format first
        if not validate_api_key(api_key_input):
            st.session_state.api_key_valid = False
            st.sidebar.error("❌ Invalid API key format. It should start with 'gsk_' and be at least 40 characters")
            return False, None
        
        # Check if we've already validated this specific key
        if api_key_input in st.session_state.manual_key_validated:
            # Use cached validation result
            cached_result = st.session_state.manual_key_validated[api_key_input]
            if cached_result["valid"]:
                st.session_state.api_key = api_key_input
                st.session_state.api_key_valid = True
                st.sidebar.success("✅ Valid API key - You can now generate responses!")
                return True, api_key_input
            else:
                st.session_state.api_key_valid = False
                st.sidebar.error(f"❌ {cached_result['message']}")
                return False, None
        else:
            # New key, need to validate
            with st.sidebar:
                with st.spinner("🔍 Validating your API key..."):
                    try:
                        temp_client = GroqClient(api_key=api_key_input)
                        validation = temp_client.test_api_key()
                        
                        # Cache the result
                        st.session_state.manual_key_validated[api_key_input] = validation
                        
                        if validation["valid"]:
                            st.session_state.api_key = api_key_input
                            st.session_state.api_key_valid = True
                            st.sidebar.success("✅ Valid API key - You can now generate responses!")
                            return True, api_key_input
                        else:
                            st.session_state.api_key_valid = False
                            st.sidebar.error(f"❌ {validation['message']}")
                            return False, None
                    except Exception as e:
                        st.session_state.api_key_valid = False
                        error_msg = str(e)
                        st.sidebar.error(f"❌ Validation failed: {error_msg}")
                        # Cache the failure
                        st.session_state.manual_key_validated[api_key_input] = {
                            "valid": False,
                            "message": f"Validation error: {error_msg}"
                        }
                        return False, None
    else:
        st.session_state.api_key_valid = False
        st.sidebar.info("ℹ️ Exploring without API key - You can browse all features but won't be able to generate responses")
        
        with st.sidebar.expander("📖 How to get a FREE Groq API key"):
            st.markdown("""
                1. Go to [Groq Console](https://console.groq.com/)
                2. Sign up or log in (FREE!)
                3. Navigate to **API Keys** section
                4. Click **Create API Key**
                5. Copy and paste it here
                
                **🎉 Groq is 100% FREE - no credit card required!**
            """)
        
        return False, None


def render_no_api_warning():
    """Render warning banner when no API key is present"""
    st.markdown("""
        <div class="warning-banner">
            <strong>⚠️ No API Key Detected</strong><br>
            You're currently exploring in <strong>preview mode</strong>. To generate actual AI responses, please enter your Groq API key in the sidebar. 
            You can still explore all features, adjust settings, and see how everything works!
        </div>
    """, unsafe_allow_html=True)


def main():
    """Main application function"""
    initialize_session_state()
    
    # Header
    st.markdown(f'<div class="main-header">{APP_TITLE}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-header">{APP_DESCRIPTION}</div>', unsafe_allow_html=True)
    
    # Get API key status
    has_api_key, api_key = render_api_key_input()
    
    # Initialize API client only if we have a valid key
    client = None
    if has_api_key:
        try:
            client = GroqClient(api_key=api_key)
        except Exception as e:
            st.error(f"❌ Failed to initialize Groq client: {e}")
            has_api_key = False
    
    # Sidebar - Configuration (always shown)
    with st.sidebar:
        st.divider()
        st.header("⚙️ Configuration")
        
        # Mode selection
        mode = st.radio(
            "Mode",
            ["Single Generation", "Comparison Mode", "Template Explorer"],
            help="Choose how you want to experiment with prompts"
        )
        
        st.divider()
        
        # Model selection
        selected_model = st.selectbox(
            "Model",
            AVAILABLE_MODELS,
            index=AVAILABLE_MODELS.index(DEFAULT_MODEL),
            help="Select the AI model to use"
        )
        
        # Show model info
        model_info = get_model_info(selected_model)
        st.info(f"**{model_info['name']}**\n\n{model_info['description']}\n\n📊 Context: {model_info['context_window']}")
        
        st.divider()
        
        # Temperature slider
        temperature = st.slider(
            "Temperature",
            MIN_TEMPERATURE,
            MAX_TEMPERATURE,
            DEFAULT_TEMPERATURE,
            0.1,
            help="Controls randomness. Lower = more focused, Higher = more creative"
        )
        st.caption(get_temperature_description(temperature))
        
        # Max tokens
        max_tokens = st.slider(
            "Max Tokens",
            MIN_TOKENS,
            MAX_TOKENS,
            DEFAULT_MAX_TOKENS,
            50,
            help="Maximum length of the response"
        )
        
        # Advanced settings in expander
        with st.expander("🔧 Advanced Settings"):
            top_p = st.slider(
                "Top P",
                MIN_TOP_P,
                MAX_TOP_P,
                DEFAULT_TOP_P,
                0.05,
                help="Nucleus sampling parameter"
            )
            
            frequency_penalty = st.slider(
                "Frequency Penalty",
                MIN_FREQUENCY_PENALTY,
                MAX_FREQUENCY_PENALTY,
                DEFAULT_FREQUENCY_PENALTY,
                0.1,
                help="Reduces repetition of token sequences"
            )
            
            presence_penalty = st.slider(
                "Presence Penalty",
                MIN_PRESENCE_PENALTY,
                MAX_PRESENCE_PENALTY,
                DEFAULT_PRESENCE_PENALTY,
                0.1,
                help="Encourages talking about new topics"
            )
    
    # Main content area based on mode
    if mode == "Single Generation":
        render_single_generation(client, has_api_key, selected_model, temperature, max_tokens, 
                                top_p, frequency_penalty, presence_penalty)
    
    elif mode == "Comparison Mode":
        render_comparison_mode(client, has_api_key, selected_model, temperature, max_tokens,
                              top_p, frequency_penalty, presence_penalty)
    
    elif mode == "Template Explorer":
        render_template_explorer(client, has_api_key, selected_model, temperature, max_tokens,
                                 top_p, frequency_penalty, presence_penalty)
    
    # History section at the bottom (only show if there's history)
    if st.session_state.history:
        render_history_section()


def render_single_generation(client, has_api_key, model, temperature, max_tokens, 
                             top_p, frequency_penalty, presence_penalty):
    """Render single generation mode"""
    st.header("🎯 Single Generation Mode")
    st.markdown("Generate a single response with your custom prompt")
    
    # Show warning if no API key
    if not has_api_key:
        render_no_api_warning()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # System prompt
        system_prompt = st.text_area(
            "System Prompt",
            value="You are a helpful AI assistant.",
            height=100,
            help="Sets the behavior and context for the AI"
        )
        
        # User prompt
        user_prompt = st.text_area(
            "Your Prompt",
            value="Explain quantum computing in simple terms.",
            height=150,
            help="Your actual question or task"
        )
        
        # Generate button
        generate_button = st.button(
            "🚀 Generate Response", 
            type="primary", 
            width='stretch',
            disabled=not has_api_key
        )
        
        if not has_api_key:
            st.caption("⚠️ Enter your API key in the sidebar to enable generation")
        
        if generate_button:
            if has_api_key and client:
                with st.spinner("Generating response..."):
                    result = client.generate_completion(
                        system_prompt=system_prompt,
                        user_prompt=user_prompt,
                        model=model,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        top_p=top_p,
                        frequency_penalty=frequency_penalty,
                        presence_penalty=presence_penalty
                    )
                    
                    if result["success"]:
                        st.session_state.current_response = result
                        
                        # Save to history
                        save_to_history(
                            system_prompt=system_prompt,
                            user_prompt=user_prompt,
                            response=result["response"],
                            model=model,
                            temperature=temperature,
                            tokens=result["total_tokens"]
                        )
                        
                        st.success("✅ Response generated successfully!")
                    else:
                        st.error(f"❌ Error: {result['error']}")
    
    with col2:
        st.subheader("📊 Current Settings")
        st.metric("Model", model)
        st.metric("Temperature", f"{temperature:.1f}")
        st.metric("Max Tokens", format_token_count(max_tokens))
        
        if top_p != DEFAULT_TOP_P or frequency_penalty != DEFAULT_FREQUENCY_PENALTY or presence_penalty != DEFAULT_PRESENCE_PENALTY:
            st.caption("**Advanced Settings Active:**")
            st.caption(f"Top P: {top_p}")
            st.caption(f"Frequency Penalty: {frequency_penalty}")
            st.caption(f"Presence Penalty: {presence_penalty}")
        
        # Show preview of what will happen
        if not has_api_key:
            st.divider()
            st.info("**Preview Mode**\n\nWith an API key, clicking 'Generate Response' will:\n- Send your prompt to OpenAI\n- Display the AI's response\n- Track token usage\n- Calculate costs")
    
    # Display response
    if st.session_state.current_response:
        st.divider()
        display_response(st.session_state.current_response)
    elif not has_api_key:
        # Show demo response
        st.divider()
        st.subheader("💬 Demo Response Preview")
        st.info("This is where your AI-generated response will appear once you enter an API key and click 'Generate Response'. The response will be formatted and displayed with token usage metrics.")


def render_comparison_mode(client, has_api_key, model, temperature, max_tokens,
                           top_p, frequency_penalty, presence_penalty):
    """Render comparison mode"""
    st.header("🔄 Comparison Mode")
    st.markdown("Compare responses with different temperature settings")
    
    # Show warning if no API key
    if not has_api_key:
        render_no_api_warning()
    
    # Prompts
    col1, col2 = st.columns(2)
    
    with col1:
        system_prompt = st.text_area(
            "System Prompt",
            value="You are a creative writer.",
            height=100
        )
    
    with col2:
        user_prompt = st.text_area(
            "Your Prompt",
            value="Write a short poem about artificial intelligence.",
            height=100
        )
    
    st.divider()
    
    # Temperature configurations
    st.subheader("⚙️ Configure Temperatures to Compare")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        temp1 = st.slider("Temperature 1", 0.0, 2.0, 0.2, 0.1, key="temp1")
        st.caption(get_temperature_description(temp1))
    
    with col2:
        temp2 = st.slider("Temperature 2", 0.0, 2.0, 0.7, 0.1, key="temp2")
        st.caption(get_temperature_description(temp2))
    
    with col3:
        temp3 = st.slider("Temperature 3", 0.0, 2.0, 1.5, 0.1, key="temp3")
        st.caption(get_temperature_description(temp3))
    
    # Generate button
    compare_button = st.button(
        "🚀 Compare Responses", 
        type="primary", 
        width='stretch',
        disabled=not has_api_key
    )
    
    if not has_api_key:
        st.caption("⚠️ Enter your API key in the sidebar to enable comparison")
    
    if compare_button:
        if has_api_key and client:
            configs = [
                {"model": model, "temperature": temp1, "max_tokens": max_tokens, 
                 "top_p": top_p, "frequency_penalty": frequency_penalty, 
                 "presence_penalty": presence_penalty},
                {"model": model, "temperature": temp2, "max_tokens": max_tokens,
                 "top_p": top_p, "frequency_penalty": frequency_penalty,
                 "presence_penalty": presence_penalty},
                {"model": model, "temperature": temp3, "max_tokens": max_tokens,
                 "top_p": top_p, "frequency_penalty": frequency_penalty,
                 "presence_penalty": presence_penalty}
            ]
            
            with st.spinner("Generating comparisons..."):
                results = client.compare_completions(
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    configs=configs
                )
            
            st.divider()
            
            # Display results side by side
            cols = st.columns(3)
            
            for idx, (col, result) in enumerate(zip(cols, results), 1):
                with col:
                    st.subheader(f"Response {idx}")
                    st.caption(f"🌡️ Temperature: {result['config']['temperature']}")
                    
                    if result["success"]:
                        st.markdown(f"**Response:**")
                        st.info(result["response"])
                        
                        st.caption(f"📊 Tokens: {format_token_count(result['total_tokens'])}")
                        st.caption(f"💰 Cost: FREE! 🎉")
                    else:
                        st.error(f"Error: {result['error']}")
    
    # Show demo comparison if no API key
    if not has_api_key:
        st.divider()
        st.subheader("📊 Demo Comparison Preview")
        
        cols = st.columns(3)
        
        demo_responses = [
            "Low temperature (0.2) produces more focused, consistent, and deterministic responses. Perfect for factual tasks.",
            "Medium temperature (0.7) balances creativity with consistency. Good for general-purpose applications.",
            "High temperature (1.5) generates more creative, diverse, and unpredictable responses. Great for brainstorming!"
        ]
        
        for idx, (col, demo) in enumerate(zip(cols, demo_responses), 1):
            with col:
                st.markdown(f"**Response {idx}**")
                st.caption(f"🌡️ Temperature: {[temp1, temp2, temp3][idx-1]}")
                st.info(demo)
                st.caption("💡 This is a demo. Actual responses will appear here when you use your API key.")


def render_template_explorer(client, has_api_key, model, temperature, max_tokens,
                             top_p, frequency_penalty, presence_penalty):
    """Render template explorer mode"""
    st.header("📚 Template Explorer")
    st.markdown("Explore pre-built prompt templates demonstrating different techniques")
    
    # Show warning if no API key
    if not has_api_key:
        render_no_api_warning()
    
    # Template selection
    template_names = get_all_template_names()
    selected_template = st.selectbox(
        "Choose a Template",
        template_names,
        help="Select a prompt template to explore"
    )
    
    template = get_template(selected_template)
    description = get_template_description(selected_template)
    
    # Show description
    st.info(f"**About this template:** {description}")
    
    st.divider()
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Display and allow editing of template
        st.subheader("📝 Template Content")
        
        system_prompt = st.text_area(
            "System Prompt",
            value=template["system"],
            height=100,
            key=f"sys_{selected_template}"
        )
        
        user_prompt = st.text_area(
            "User Prompt",
            value=template["user"],
            height=200,
            key=f"user_{selected_template}"
        )
        
        try_button = st.button(
            "🚀 Try This Template", 
            type="primary", 
            width='stretch',
            disabled=not has_api_key
        )
        
        if not has_api_key:
            st.caption("⚠️ Enter your API key in the sidebar to test this template")
        
        if try_button:
            if has_api_key and client:
                with st.spinner("Generating response..."):
                    result = client.generate_completion(
                        system_prompt=system_prompt,
                        user_prompt=user_prompt,
                        model=model,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        top_p=top_p,
                        frequency_penalty=frequency_penalty,
                        presence_penalty=presence_penalty
                    )
                    
                    if result["success"]:
                        st.session_state.current_response = result
                        save_to_history(
                            system_prompt=system_prompt,
                            user_prompt=user_prompt,
                            response=result["response"],
                            model=model,
                            temperature=temperature,
                            tokens=result["total_tokens"]
                        )
                        st.success("✅ Response generated!")
                    else:
                        st.error(f"❌ Error: {result['error']}")
    
    with col2:
        st.subheader("💡 Template Tips")
        
        # Template-specific tips
        tips = {
            "Zero-Shot": "Best for simple, straightforward tasks. No examples needed.",
            "Few-Shot Learning": "Provide 2-3 examples. More examples = better results.",
            "Chain-of-Thought": "Use phrases like 'step by step' or 'let's think through this'.",
            "Role-Based": "Be specific about the role. 'Expert' is better than 'person'.",
            "Constrained Output": "Specify exact format (JSON, bullet points, etc.).",
            "Creative Writing": "Use higher temperature (0.8-1.2) for more creativity.",
            "Code Generation": "Use lower temperature (0.2-0.5) for consistent code.",
            "Structured Data Extraction": "Always specify the exact output format.",
            "Negative Prompting": "Tell the model what NOT to do for better control.",
            "ReAct (Reasoning + Acting)": "Great for problem-solving and planning tasks."
        }
        
        st.info(tips.get(selected_template, "Experiment with different settings!"))
        
        st.subheader("📊 Recommended Settings")
        if selected_template in ["Creative Writing"]:
            st.success("🌡️ Temperature: 0.8 - 1.2\n\n📝 Max Tokens: 1000+")
        elif selected_template in ["Code Generation", "Structured Data Extraction"]:
            st.success("🌡️ Temperature: 0.2 - 0.5\n\n📝 Max Tokens: 500 - 1000")
        else:
            st.success("🌡️ Temperature: 0.5 - 0.8\n\n📝 Max Tokens: 300 - 800")
    
    # Display response if available
    if st.session_state.current_response:
        st.divider()
        display_response(st.session_state.current_response)
    elif not has_api_key:
        # Show demo for templates
        st.divider()
        st.subheader("💬 Example Output Preview")
        
        # Show template-specific demo outputs
        demo_outputs = {
            "Zero-Shot": "This template demonstrates basic prompting without examples. AI responds directly to your query with no prior context or examples.",
            "Few-Shot Learning": "This technique shows the AI examples first, then asks it to perform a similar task. The AI learns from the pattern in your examples.",
            "Chain-of-Thought": "The AI will break down complex problems into steps, showing its reasoning process. This helps with math, logic, and analysis tasks.",
            "Role-Based": "By assigning a specific role or persona, you guide the AI's tone, expertise level, and response style.",
            "Constrained Output": "This ensures the AI follows specific formatting rules - perfect for structured data or when you need consistent output format.",
            "Creative Writing": "Higher temperature settings make responses more creative and varied. Great for stories, poetry, and imaginative content.",
            "Code Generation": "Lower temperature ensures consistent, reliable code. The AI focuses on correctness and best practices.",
            "Structured Data Extraction": "The AI pulls key information from text and formats it as requested (JSON, CSV, etc.).",
            "Negative Prompting": "Telling the AI what NOT to do often works better than just positive instructions.",
            "ReAct (Reasoning + Acting)": "Combines reasoning (thinking through the problem) with actions (specific steps to take)."
        }
        
        st.info(demo_outputs.get(selected_template, "Actual AI responses will appear here when you use your API key."))


def display_response(result):
    """Display the API response with metrics"""
    st.subheader("💬 Response")
    
    # Response text
    st.markdown(result["response"])
    
    st.divider()
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Tokens", format_token_count(result["total_tokens"]))
    
    with col2:
        st.metric("Input Tokens", format_token_count(result["prompt_tokens"]))
    
    with col3:
        st.metric("Output Tokens", format_token_count(result["completion_tokens"]))
    
    with col4:
        # Get API key from session state for cost calculation
        api_key = st.session_state.get("api_key", os.getenv("GROQ_API_KEY"))
        if api_key:
            client = GroqClient(api_key=api_key)
            cost = client.calculate_cost(
                model=result["model"],
                prompt_tokens=result["prompt_tokens"],
                completion_tokens=result["completion_tokens"],
                costs=MODEL_COSTS
            )
            # Show FREE badge instead of cost
            st.metric("Cost", "FREE! 🎉")


def render_history_section():
    """Render the history section"""
    st.divider()
    
    with st.expander("📜 View History", expanded=False):
        df = get_history_dataframe()
        
        if df.empty:
            st.info("No history yet. Generate some responses to see them here!")
        else:
            st.dataframe(
                df[["timestamp", "model", "temperature", "tokens", "user_prompt"]],
                width='stretch',
                hide_index=True
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                csv = export_history_to_csv()
                if csv:
                    st.download_button(
                        label="📥 Download History (CSV)",
                        data=csv,
                        file_name="prompt_history.csv",
                        mime="text/csv"
                    )
            
            with col2:
                if st.button("🗑️ Clear History"):
                    clear_history()
                    st.rerun()


if __name__ == "__main__":
    main()