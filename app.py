"""
Prompt Playground - Main Streamlit Application
An interactive tool for experimenting with LLM prompting techniques
"""

import streamlit as st
import os
from dotenv import load_dotenv

# Import custom modules
from src.api_client import OpenAIClient
from src.prompt_templates import get_all_template_names, get_template, get_template_description
from src.utils import (
    format_token_count, format_cost, get_temperature_description,
    save_to_history, get_history_dataframe, clear_history,
    export_history_to_csv, get_model_info
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


def main():
    """Main application function"""
    initialize_session_state()
    
    # Header
    st.markdown(f'<div class="main-header">{APP_TITLE}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-header">{APP_DESCRIPTION}</div>', unsafe_allow_html=True)
    
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("⚠️ OpenAI API Key not found! Please add it to your .env file.")
        st.code("OPENAI_API_KEY=your_key_here")
        st.stop()
    
    # Initialize API client
    try:
        client = OpenAIClient()
    except Exception as e:
        st.error(f"❌ Failed to initialize OpenAI client: {e}")
        st.stop()
    
    # Sidebar - Configuration
    with st.sidebar:
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
        render_single_generation(client, selected_model, temperature, max_tokens, 
                                top_p, frequency_penalty, presence_penalty)
    
    elif mode == "Comparison Mode":
        render_comparison_mode(client, selected_model, temperature, max_tokens,
                              top_p, frequency_penalty, presence_penalty)
    
    elif mode == "Template Explorer":
        render_template_explorer(client, selected_model, temperature, max_tokens,
                                 top_p, frequency_penalty, presence_penalty)
    
    # History section at the bottom
    render_history_section()


def render_single_generation(client, model, temperature, max_tokens, 
                             top_p, frequency_penalty, presence_penalty):
    """Render single generation mode"""
    st.header("🎯 Single Generation Mode")
    st.markdown("Generate a single response with your custom prompt")
    
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
        if st.button("🚀 Generate Response", type="primary", use_container_width=True):
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
    
    # Display response
    if st.session_state.current_response:
        st.divider()
        display_response(st.session_state.current_response)


def render_comparison_mode(client, model, temperature, max_tokens,
                           top_p, frequency_penalty, presence_penalty):
    """Render comparison mode"""
    st.header("🔄 Comparison Mode")
    st.markdown("Compare responses with different temperature settings")
    
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
    if st.button("🚀 Compare Responses", type="primary", use_container_width=True):
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
                    
                    cost = client.calculate_cost(
                        model=result["model"],
                        prompt_tokens=result["prompt_tokens"],
                        completion_tokens=result["completion_tokens"],
                        costs=MODEL_COSTS
                    )
                    st.caption(f"💰 Cost: {format_cost(cost)}")
                else:
                    st.error(f"Error: {result['error']}")


def render_template_explorer(client, model, temperature, max_tokens,
                             top_p, frequency_penalty, presence_penalty):
    """Render template explorer mode"""
    st.header("📚 Template Explorer")
    st.markdown("Explore pre-built prompt templates demonstrating different techniques")
    
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
        
        if st.button("🚀 Try This Template", type="primary", use_container_width=True):
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
        cost = OpenAIClient().calculate_cost(
            model=result["model"],
            prompt_tokens=result["prompt_tokens"],
            completion_tokens=result["completion_tokens"],
            costs=MODEL_COSTS
        )
        st.metric("Cost", format_cost(cost))


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
                use_container_width=True,
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