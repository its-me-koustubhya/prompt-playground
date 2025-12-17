# 🎨 Prompt Playground App

An interactive Streamlit application for experimenting with different prompting techniques and LLM parameters using **Groq's FREE API**.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.51.0-red)
![Groq](https://img.shields.io/badge/Groq-FREE-green)

## 🎉 Why Groq?

- **100% FREE** - No credit card required!
- **Lightning Fast** - Groq's LPU technology delivers incredible speed
- **Powerful Models** - Access to Llama 3.3 70B, Mixtral, and more
- **No Quota Limits** - Generous free tier for learning and experimentation

## ✨ Features

### 🎯 Three Interactive Modes

1. **Single Generation** - Test prompts with adjustable parameters
2. **Comparison Mode** - Compare responses with different temperature settings side-by-side
3. **Template Explorer** - Explore 10+ pre-built prompt templates

### 🔑 Secure API Key Management

- Enter your API key directly in the app interface
- **Privacy Guaranteed:** Your API key is stored only in browser session memory
- Never saved to disk or transmitted anywhere except Groq's API
- Option to use `.env` file for local development

### 🤖 Available Models (All FREE!)

- **Llama 3.3 70B Versatile** - Most capable, excellent for complex tasks
- **Llama 3.1 70B Versatile** - Powerful and versatile
- **Llama 3.1 8B Instant** - Lightning fast responses
- **Mixtral 8x7B** - Mixture of experts model
- **Gemma 2 9B** - Google's efficient model

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
- Temperature effect descriptions
- History tracking with CSV export
- Advanced parameter controls (Top P, Frequency Penalty, Presence Penalty)
- Side-by-side model comparisons

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- FREE Groq API Key ([Get one here](https://console.groq.com/) - no credit card!)
- Conda (recommended) or pip

### Installation

1. **Clone the repository**

```bash
git clone <your-repo-url>
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

5. **Get your FREE Groq API key**
   - Visit [Groq Console](https://console.groq.com/)
   - Sign up (no credit card required!)
   - Create an API key
   - Enter it in the app sidebar
   - Start experimenting!

---

## 🔐 API Key Setup

### Option 1: Enter in App (Recommended)

1. Run the app: `streamlit run app.py`
2. Enter your Groq API key in the sidebar (starts with `gsk_`)
3. Your key is stored only in session memory (never saved to disk)

### Option 2: Use .env File (For Local Development)

1. Create a `.env` file in the project root:

```bash
GROQ_API_KEY=gsk_your-actual-key-here
```

2. The app will automatically detect and use this key

**⚠️ Security Note:**

- Never commit your `.env` file to Git (it's already in `.gitignore`)
- Never share your API key publicly
- The app only sends your key to Groq's official API

---

## 📦 Dependencies

```
streamlit==1.51.0
groq==0.37.1
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

- Token management
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

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [Groq](https://groq.com/) (FREE API!)
- Models: Meta's Llama, Mistral's Mixtral, Google's Gemma

---

**Happy Prompting! 🎨✨ (100% FREE!)**
