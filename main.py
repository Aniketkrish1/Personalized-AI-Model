import asyncio
import pygame
import threading
from concurrent.futures import ThreadPoolExecutor
from Jarvis.Functions import Chatbot, Model, Search, SpeechToText, TextToSpeech, Automation
import difflib  # For text similarity comparison
import psutil,pyttsx3
# Global storage for background search results and spoken text
search_results = {}
spoken_text_queue = []  # List to track recently spoken text
executor = ThreadPoolExecutor(max_workers=1)  # Single worker for sequential searches

# Lock for thread-safe access to spoken_text_queue
queue_lock = threading.Lock()

def system_stats():
    battery_percent = psutil.sensors_battery().percent
    final_res = f" battery level is at {battery_percent} percent"
    return final_res

# Callback to notify when search is complete
def on_search_complete(command, result):
    notification = f"I have accessed {command} and am ready to explain, should I, sir?"
    TextToSpeech.TextToSpeech(notification)  # Use from TextToSpeech.py
    search_results[command] = result  # Store result for later retrieval

# Background search function
def run_realtime_search(command, prompt):
    result = Search.RealtimeSearch(prompt)  # Assuming this is synchronous and slow
    on_search_complete(command, result)

# Filter out self-spoken text
def is_self_spoken(text):
    if not text:
        return False
    text_lower = text.lower()
    with queue_lock:
        for spoken in spoken_text_queue[:]:  # Copy to avoid modifying during iteration
            similarity = difflib.SequenceMatcher(None, text_lower, spoken).ratio()
            if similarity > 0.8:  # Threshold for "close enough" match
                spoken_text_queue.remove(spoken)  # Remove after match to avoid reuse
                return True
    return False

async def main():
    # Play intro audio
    file_path = "D:\\jarvis\\Jarvis\\Data\\jarvis.mp3"
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue
    res = system_stats()
    engine = pyttsx3.init()
    engine.say(res)
    engine.runAndWait()
    recognizer = SpeechToText.SpeechRecognizer()  # Single instance
    while True:
        text = recognizer.listen_continuously()
        if not text or is_self_spoken(text):
            continue  # Skip if no text or it matches Jarvis's speech

        command_list = Model.FirstlayerDMM(text)
        print(f"Received commands: {command_list}")
        if not command_list:
            TextToSpeech.TextToSpeech("Bye, sir. Shutting down.")
            exit()
        tasks = []
        for cmd in command_list:
            func = cmd.split()[0]
            prompt = " ".join(cmd.split()[1:])
            print(f"Processing: {func} {prompt}")

            if func == 'general':
                response = Chatbot.Chatbot(prompt)  # Pass prompt for context
                tasks.append(asyncio.to_thread(TextToSpeech.TextToSpeech, response))
            elif func == 'realtime':
                executor.submit(run_realtime_search, cmd, prompt)
            else:
                tasks.append(Automation.Automation([cmd]))
                TextToSpeech.TextToSpeech(f"Executing {cmd}")  # Use from TextToSpeech.py

        if tasks:
            await asyncio.gather(*tasks)

        # Check for follow-up to explain search results
        while search_results:
            text = recognizer.listen_continuously()
            if not text or is_self_spoken(text):
                continue
            if text and ("yes" in text.lower() or "okay" in text.lower() or "ok" in text.lower()):
                for cmd, result in list(search_results.items()):
                    TextToSpeech.TextToSpeech(f"Here is the result for {cmd}: {result}")
                    del search_results[cmd]
                break
            elif text and "no" in text.lower():
                search_results.clear()
                break
            else:
                await asyncio.sleep(0.1)  # Brief pause for other commands

if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        executor.shutdown(wait=False)