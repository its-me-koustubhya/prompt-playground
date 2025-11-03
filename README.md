# 🎨 Prompt Playground App

An interactive Streamlit application for experimenting with different prompting techniques and LLM parameters.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.51.0-red)
![OpenAI](https://img.shields.io/badge/OpenAI-2.6.1-green)

## ✨ Features

### 🎯 Three Interactive Modes

1. **Single Generation** - Test prompts with adjustable parameters
2. **Comparison Mode** - Compare responses with different temperature settings side-by-side
3. **Template Explorer** - Explore 10+ pre-built prompt templates

### 🔑 Secure API Key Management

- Enter your API key directly in the app interface
- **Privacy Guaranteed:** Your API key is stored only in browser session memory
- Never saved to disk or transmitted anywhere except OpenAI's API
- Option to use `.env` file for local development

### 📚 Pre-Built Templates

- Zero-Shot Prompting
- Few-Shot Learning
- Chain-of-Thought
- Role-Based Prompting
- Constrained Output
- Creative Writing
- Code Generation
- Structured Data Extraction
- Negative Prompting
- ReAct (Reasoning + Acting)

### 📊 Advanced Features

- Real-time token counting
- Cost calculation per request
- Temperature effect descriptions
- History tracking with CSV export
- Advanced parameter controls (Top P, Frequency Penalty, Presence Penalty)
- Model selection (GPT-4o, GPT-4o Mini, GPT-4 Turbo, GPT-3.5 Turbo)

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- OpenAI API Key ([Get one here](https://platform.openai.com/api-keys))
- Conda (recommended) or pip

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/its-me-koustubhya/prompt-playground.git
cd prompt-playground
```

2. **Create and activate conda environment**

```bash
conda create -n prompt-playground python=3.11 -y
conda activate prompt-playground
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the application**

```bash
streamlit run app.py
```

5. **Enter your API key**
   - Open the app in your browser (usually http://localhost:8501)
   - Enter your OpenAI API key in the sidebar
   - Start experimenting!

---

## 🔐 API Key Setup

### Option 1: Enter in App (Recommended for Most Users)

1. Run the app: `streamlit run app.py`
2. Enter your API key in the sidebar input field
3. Your key is stored only in session memory (never saved to disk)

### Option 2: Use .env File (For Local Development)

1. Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=sk-your-actual-key-here
```

2. The app will automatically detect and use this key

**⚠️ Security Note:**

- Never commit your `.env` file to Git (it's already in `.gitignore`)
- Never share your API key publicly
- The app only sends your key to OpenAI's official API

---

## 📁 Project Structure

```
prompt-playground/
│
├── app.py                      # Main Streamlit application
├── .env                        # API keys (optional, not committed)
├── .gitignore                  # Git ignore file
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
│
├── src/
│   ├── __init__.py
│   ├── api_client.py          # OpenAI API interactions
│   ├── prompt_templates.py    # Pre-built prompt templates
│   └── utils.py               # Helper functions
│
├── config/
│   ├── __init__.py
│   └── settings.py            # App configuration
│
└── assets/
    └── styles.css             # Custom CSS (optional)
```

---

## 📦 Dependencies

```
streamlit==1.51.0
openai==2.6.1
python-dotenv==1.2.1
pandas==2.3.3
tiktoken==0.12.0
plotly==6.3.1
```

---

## 🎓 Learning Outcomes

By using this app, you'll learn:

✅ **Prompt Engineering Fundamentals**

- How temperature affects AI creativity vs consistency
- When to use zero-shot vs few-shot prompting
- How to guide AI with system prompts

✅ **LLM Parameter Optimization**

- Token management and cost optimization
- Advanced parameters (Top P, penalties)
- Model selection for different tasks

✅ **Practical Skills**

- Testing and debugging prompts
- Comparing different approaches
- Building reusable prompt templates

---

## 💡 Usage Examples

### Example 1: Testing Different Temperatures

```
Mode: Comparison Mode
Prompt: "Write a creative story opening"
Temperatures: 0.2, 0.7, 1.5

Result: See how creativity increases with temperature!
```

### Example 2: Learning Chain-of-Thought

```
Mode: Template Explorer
Template: Chain-of-Thought
Task: Math problem solving

Result: AI shows step-by-step reasoning
```

### Example 3: Code Generation

```
Mode: Single Generation
System: "You are an expert Python programmer"
Temperature: 0.2 (for consistency)
Prompt: "Create a function to calculate fibonacci"

Result: Clean, consistent code
```

---

## 🔧 Advanced Configuration

### Temperature Guide

- **0.0 - 0.3**: Deterministic, factual tasks
- **0.4 - 0.7**: Balanced, general purpose
- **0.8 - 1.2**: Creative tasks, brainstorming
- **1.3 - 2.0**: Highly experimental, unpredictable

### Model Selection

- **GPT-4o**: Most advanced, best for complex tasks
- **GPT-4o Mini**: Fast, affordable, great for most tasks (recommended)
- **GPT-4 Turbo**: Previous generation, still powerful
- **GPT-3.5 Turbo**: Economical, good for simple tasks

---

## 📊 Cost Tracking

The app shows approximate costs for each API call:

- Input tokens: Charged per 1,000 tokens
- Output tokens: Charged per 1,000 tokens
- Costs vary by model (GPT-4o Mini is most economical)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [OpenAI API](https://openai.com/)
- Inspired by the prompt engineering community

---

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

## 🎯 Roadmap

- [ ] Add streaming responses
- [ ] Save favorite prompts
- [ ] Export prompts as code snippets
- [ ] Add more prompt templates
- [ ] Multi-turn conversation support
- [ ] Batch processing mode

---

**Happy Prompting! 🎨✨**
