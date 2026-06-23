"""
===========================================================================
 GRAMMAR & TONE POLISHER -- A Beginner's LangChain Single-Agent Project
===========================================================================

 WHAT THIS PROJECT TEACHES YOU:
   1. How LangChain works (chains, prompts, LLMs, tools, agents)
   2. How to build a SINGLE AGENT that uses tools
   3. How to connect LangChain to OpenAI
   4. How prompt templates shape LLM output
   5. How to design a two-step text editing workflow using tools

 HOW LANGCHAIN WORKS (the big picture):
   LangChain is a framework that makes it easy to build LLM-powered apps.

     [User Input] --> [Prompt Template] --> [LLM (GPT)] --> [Output]

   - Prompt Template : A reusable template with placeholders (like a form)
   - LLM            : The AI model that generates text (OpenAI GPT)
   - Output         : The generated response

 WHAT IS AN AGENT?
   An agent is an LLM that can USE TOOLS and DECIDE what to do next.
   Unlike a simple chain (input -> LLM -> output), an agent can:
     1. Think about what it needs to do
     2. Pick a tool to use
     3. Use the tool and see the result
     4. Decide if it needs more steps or if it's done

   This is the tool-calling loop:
     THINK -> ACT -> OBSERVE -> THINK -> ... -> FINAL ANSWER

 HOW THIS PROJECT FLOWS:
   1. User provides raw text and a desired tone
   2. Agent calls fix_grammar_and_clarity tool -> corrects grammar and clarity
   3. Agent calls adjust_tone tool -> rewrites text in the requested tone
   4. Agent returns the final polished text to the user

 KEY LANGCHAIN COMPONENTS USED:
   - ChatOpenAI      : LLM wrapper that sends prompts to OpenAI's GPT API
   - PromptTemplate  : Template with {placeholders} filled before sending to LLM
   - @tool decorator : Turns a Python function into a tool the agent can call
   - create_agent    : Wires LLM + tools + system prompt into a runnable agent

 SETUP:
   1. pip install -r requirements.txt
   2. Copy .env.example to .env and add your OpenAI API key
   3. python grammar_tone_polisher.py

 See langchain_tutorial.md for a full beginner's guide to LangChain.
 See architecture_diagram.drawio for a visual diagram of this project.
===========================================================================
"""

import logging
import sys
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langchain.agents import create_agent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("GrammarTonePolisher")

logger.info("Starting Grammar & Tone Polisher Agent...")

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key or api_key.startswith("sk-your"):
    logger.error("OPENAI_API_KEY not set! Copy .env.example to .env and add your key.")
    sys.exit(1)

logger.info("API key loaded successfully")
logger.info("All LangChain components imported")
logger.info("Initializing the LLM (OpenAI GPT)...")

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0.7,
    verbose=True,
)

logger.info("LLM initialized: model=gpt-4.1-mini, temperature=0.7")
logger.info("Defining agent tools...")


@tool
def fix_grammar_and_clarity(raw_text: str) -> str:
    """
    Corrects grammar, spelling, punctuation, and awkward phrasing while
    preserving the original meaning.
    Input should be the user's raw text (email, message, paragraph).
    Returns a cleaned-up, grammatically correct version of the text.
    """
    logger.info("[Tool: fix_grammar_and_clarity] Correcting grammar and clarity...")

    fix_prompt = PromptTemplate(
        input_variables=["raw_text"],
        template="""You are a professional editor.

Correct the grammar, spelling, punctuation, and awkward phrasing in this text.
Preserve the original meaning and keep the content neutral.

Text:
{raw_text}

Return ONLY the corrected and clarified text, nothing else.""",
    )

    formatted_prompt = fix_prompt.format(raw_text=raw_text)
    logger.info("[Tool: fix_grammar_and_clarity] Sending prompt to LLM...")

    response = llm.invoke(formatted_prompt)
    logger.info("[Tool: fix_grammar_and_clarity] Text corrected successfully!")
    return response.content


@tool
def adjust_tone(corrected_text: str, tone: str) -> str:
    """
    Rewrites the corrected text so it matches the requested tone without
    losing the core message.
    Input should be the corrected text and a target tone.
    Returns the final polished text in the requested tone.
    """
    logger.info("[Tool: adjust_tone] Adjusting tone...")

    tone_prompt = PromptTemplate(
        input_variables=["corrected_text", "tone"],
        template="""You are a professional editor.

Rewrite the following text so it matches the requested tone while keeping the
original meaning and key message unchanged.

Tone: {tone}

Text:
{corrected_text}

Return ONLY the rewritten text in the requested tone, nothing else.""",
    )

    formatted_prompt = tone_prompt.format(corrected_text=corrected_text, tone=tone)
    logger.info("[Tool: adjust_tone] Sending prompt to LLM...")

    response = llm.invoke(formatted_prompt)
    logger.info("[Tool: adjust_tone] Tone adjustment complete!")
    return response.content


tools = [fix_grammar_and_clarity, adjust_tone]
logger.info(f"Tools registered: {[t.name for t in tools]}")
logger.info("Creating the agent...")

SYSTEM_PROMPT = """You are a professional editor. Your job is to make any writing
correct, clear, and perfectly suited to its intended tone.

When the user gives you raw text and a target tone, follow these steps:
1. First, use the fix_grammar_and_clarity tool to correct grammar and clarity.
2. Then, use the adjust_tone tool to rewrite the corrected text to match the
   requested tone.
3. Return only the final polished text.

Always use both tools in order: fix grammar and clarity first, then adjust tone."""

agent_graph = create_agent(
    model=llm,
    tools=tools,
    system_prompt=SYSTEM_PROMPT,
    debug=True,
)

logger.info("Agent created and ready to run!")


def run_grammar_tone_polisher(raw_text: str, tone: str) -> str:
    """
    Main function to run the grammar and tone polisher agent.

    Args:
        raw_text: The user's original text input.
        tone: The desired target tone (e.g., formal, friendly, persuasive).

    Returns:
        The final polished text in the requested tone.
    """
    logger.info("=" * 60)
    logger.info(f"USER'S RAW TEXT: {raw_text}")
    logger.info(f"TARGET TONE: {tone}")
    logger.info("=" * 60)
    logger.info("Agent is now thinking... watch the tool-calling loop below!")
    logger.info("-" * 60)

    result = agent_graph.invoke(
        {"messages": [HumanMessage(content=f"Text: {raw_text}\nTone: {tone}")]}
    )

    final_text = result["messages"][-1].content

    logger.info("-" * 60)
    logger.info("Agent finished! Here's your polished text:")
    logger.info("=" * 60)

    return final_text


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  GRAMMAR & TONE POLISHER AGENT")
    print("  Powered by LangChain + OpenAI")
    print("=" * 60)
    print("\nPaste the text you want polished and enter your desired tone.")
    print("Type 'quit' to exit.\n")

    while True:
        raw_text = input("Your text: ").strip()

        if not raw_text:
            print("Please enter some text.\n")
            continue

        if raw_text.lower() in ("quit", "exit", "q"):
            print("\nGoodbye! Happy writing!")
            break

        tone = input("Desired tone (e.g., formal, friendly, persuasive): ").strip()
        if tone.lower() in ("quit", "exit", "q"):
            print("\nGoodbye! Happy writing!")
            break

        if not tone:
            print("Please enter a tone.\n")
            continue

        try:
            polished_text = run_grammar_tone_polisher(raw_text, tone)

            print("\n" + "=" * 60)
            print("YOUR POLISHED TEXT:")
            print("=" * 60)
            print(polished_text)
            print("=" * 60 + "\n")

        except Exception as e:
            logger.error(f"Something went wrong: {e}")
            print(f"\nError: {e}")
            print("Please check your API key and try again.\n")
