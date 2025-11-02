# Prompt Playground App

An interactive Streamlit application for experimenting with different prompting techniques and LLM parameters.

## Features

- Adjustable temperature and token limits
- Multiple prompt templates
- Side-by-side comparison
- Token usage tracking

## Setup

1. Clone the repository
2. Create conda environment:

```bash
   conda create -n prompt-playground python=3.11
   conda activate prompt-playground
```

3. Install dependencies:

```bash
   pip install -r requirements.txt
```

4. Create `.env` file with your OpenAI API key:

```
   OPENAI_API_KEY=your_key_here
```

5. Run the app:

```bash
   streamlit run app.py
```

## Tech Stack

- Python 3.11
- Streamlit
- OpenAI API
- Pandas
- Plotly
