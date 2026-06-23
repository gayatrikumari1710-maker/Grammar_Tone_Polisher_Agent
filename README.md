# Grammar & Tone Polisher Agent

A beginner-friendly project that demonstrates a **two-step editor agent** using **LangChain + OpenAI**. The agent takes user text and a requested tone, then first corrects grammar and clarity and finally rewrites the text to match the desired tone.

## What You'll Learn

- How LangChain tools can break text editing into multiple steps
- How to define a grammar/clarity tool and a tone-adjustment tool
- How an agent chooses which tool to call and uses the tool outputs
- How to structure prompts for tool-based editing workflows
- How to preserve original meaning while improving style and tone

## How It Works

```
User pastes raw text + desired tone
       |
       v
  [Agent decides to correct text first]
       |
       v
  [Tool: fix_grammar_and_clarity] --> cleans grammar and phrasing
       |
       v
  [Agent decides to adjust tone next]
       |
       v
  [Tool: adjust_tone] --> rewrites text in the requested tone
       |
       v
  Final polished text returned to user
```

## Prerequisites

- Python 3.10 or higher
- An OpenAI API key ([get one here](https://platform.openai.com/api-keys))

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/NisargKadam/Langchain_sample_project.git
cd Langchain_sample_project
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

- **Windows (PowerShell):**
  ```powershell
  .venv\Scripts\Activate
  ```
- **macOS / Linux:**
  ```bash
  source .venv/bin/activate
  ```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your API key

Copy the example env file and add your real key:

```bash
cp .env.example .env
```

Open `.env` and replace the placeholder with your actual OpenAI API key:

```
OPENAI_API_KEY=sk-your-actual-key-here
```

## Run

```bash
python grammar_tone_polisher.py
```

You'll see an interactive prompt:

```
============================================================
  GRAMMAR & TONE POLISHER AGENT
  Powered by LangChain + OpenAI
============================================================

Paste the text you want polished and enter your desired tone.

Type 'quit' to exit.

Your text:
```

The agent will first clean grammar and clarity, then rewrite the text in the requested tone.

## Example

**Input:**
```
hey team, wanted to say thanks for finishing project early. great job!
```

**Tone:**
```
friendly
```

**Output:**
```
Subject: Thank You for Finishing the Project Early

Hi team,

I just wanted to say thank you for finishing the project early. Your hard work and teamwork made this possible — great job!

Best,
[Your Name]
```

## Project Structure

```
.
├── grammar_tone_polisher.py   # Main agent code (fully commented)
├── requirements.txt           # Python dependencies
├── .env.example               # API key template
├── .gitignore                 # Keeps secrets and venv out of git
└── README.md                  # This file
```

## Tech Stack

- [LangChain](https://python.langchain.com/) - Framework for building LLM applications
- [OpenAI GPT-4o-mini](https://platform.openai.com/) - The LLM powering the agent
- [python-dotenv](https://pypi.org/project/python-dotenv/) - Environment variable management
