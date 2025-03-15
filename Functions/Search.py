import json
import os
import datetime
from dotenv import dotenv_values
from googlesearch import search
from groq import Groq

# Load environment variables
env_vars = dotenv_values(r"D:\jarvis\Jarvis\.env")

Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistant")
GroqAPI = env_vars.get("GroqAPI")

# Initialize Groq API client
client = Groq(api_key=GroqAPI)

# Define system message
system = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""

# Load chat history (create if missing or corrupted)
chatlog_path = r"D:\jarvis\Jarvis\Data\Chatlog.json"

try:
    with open(chatlog_path, 'r', encoding="utf-8") as f:
        messages = json.load(f)
        if not isinstance(messages, list):
            messages = []
except (FileNotFoundError, json.JSONDecodeError):
    messages = []
    with open(chatlog_path, 'w', encoding="utf-8") as f:
        json.dump(messages, f, indent=4)


# Google Search function (Fixed)
def GoogleSearch(query):
    try:
        results = list(search(query))  # Fetch search results
        Answer = f"The search results for '{query}' are:\n[start]\n"

        for i, url in enumerate(results[:5], 1):  # Limit to top 5 results
            Answer += f"{i}. {url}\n\n"

        Answer += "[end]"
        return Answer
    except Exception as e:
        return f"Error performing Google search: {e}"


# Function to clean extra blank lines
def AnswerModifier(Answer):
    return '\n'.join([line for line in Answer.split('\n') if line.strip()])


# System chatbot setup
SystemChatbot = [
    {'role': 'system', 'content': system},
    {'role': 'user', 'content': 'Hi'},
    {'role': 'assistant', 'content': 'Hello, how can I help you?'}
]


# Get real-time date & time information
def info():
    current_date_time = datetime.datetime.now()
    return (
        f"Use this information if needed:\n"
        f"Day: {current_date_time.strftime('%A')}\n"
        f"Date: {current_date_time.strftime('%d')}\n"
        f"Month: {current_date_time.strftime('%B')}\n"
        f"Year: {current_date_time.strftime('%Y')}\n"
        f"Time: {current_date_time.strftime('%H')} hours, "
        f"{current_date_time.strftime('%M')} minutes, "
        f"{current_date_time.strftime('%S')} seconds\n"
    )


# AI-powered real-time search
def RealtimeSearch(prompt):
    global messages

    # Load latest chat history
    with open(chatlog_path, 'r', encoding="utf-8") as f:
        messages = json.load(f)

    messages.append({'role': 'user', 'content': prompt})

    SystemChatbot.append({'role': 'system', 'content': GoogleSearch(prompt)})

    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=SystemChatbot + [{"role": "system", "content": info()}] + messages,
        max_tokens=2048,
        temperature=0.7,
        top_p=1,
        stream=True,
        stop=None
    )

    Answer = ""

    for chunk in completion:
        if hasattr(chunk, "choices") and chunk.choices:
            Answer += chunk.choices[0].delta.content or ""

    Answer = Answer.replace("</s>", "").strip()

    messages.append({"role": "assistant", "content": Answer})

    # Save updated chat history
    with open(chatlog_path, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=4)

    SystemChatbot.pop()

    return AnswerModifier(Answer)


if __name__ == '__main__':
    while True:
        prompt = input("Enter the prompt: ")
        print(RealtimeSearch(prompt))
