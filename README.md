# 🎙️ Jarvis: Your Intelligent Voice Assistant

Welcome to **Jarvis**, a powerful voice-activated assistant that listens to your commands and responds using the innovative **Retrieval-Augmented Generation (RAG)** method! Inspired by the iconic AI from Iron Man, JarvisVoice is designed to be your personal helper, executing tasks and providing intelligent responses—all without relying on traditional pre-trained models. Speak naturally, and let JarvisVoice handle the rest!

---

## ✨ Features
- **Voice Command Processing**: Speak your commands directly, and JarvisVoice responds instantly.
- **RAG-Powered Responses**: Uses Retrieval-Augmented Generation to fetch relevant context and generate natural, context-aware answers.
- **Task Execution**: Perform actions like opening apps (e.g., Chrome, YouTube) or retrieving information.


---

## 🚀 Getting Started

### Prerequisites
- Python 3.10.10
- A microphone for voice input

### Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Aniketkrish1/Personalized-AI-Model.git

2. **Install Dependency**
   Open Terminal and run :
   pip install -r req.txt

3. Run the Assistant :
   python main.py

4.**Execution**
    Give command in natural way , like "open chrome", "open Youtube" , "Tell me time", " Update me with today's news", etc..

🎬 **How It Works**
Jarvis listens for your voice commands and processes them using a RAG pipeline. Unlike traditional models, RAG combines a retrieval step (fetching relevant data from a knowledge base) with a generation step (creating natural language responses), making it highly adaptable and efficient.

Voice Input: Speak your command naturally (e.g., "Open YouTube").
RAG Pipeline: Retrieves context from a custom knowledge base and generates an appropriate response or action.
Actions: Executes predefined tasks or provides information based on the command.
Example Commands
"Open Chrome" → Opens the Chrome browser.
"Tell me the time" → Retrieves and responds with the current time.

🛠️ **Customize Your Jarvis**
Want to add more commands or enhance its knowledge? Here’s how:

-Update Commands: Modify the RAG data source in main.py to include new command-response pairs or knowledge snippets.
-Extend Actions: Edit the main function in main.py to add new actions (e.g., opening other apps or fetching data).
-Improve RAG: Expand the retrieval corpus with more data to make responses smarter.

⚠️ **Known Limitations**
Requires a quiet environment for accurate voice recognition.
RAG responses depend on the quality and quantity of your data—enhance it for better results!
Currently processes commands directly—consider adding a wake-word for hands-free activation.

🙌 **Acknowledgments**
Inspired by the Jarvis AI from Iron Man.
Built with love using Python and the power of RAG.

