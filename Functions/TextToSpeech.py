import pygame
import random
import asyncio
import edge_tts
import os
import threading
from dotenv import dotenv_values
from Jarvis.main import spoken_text_queue,queue_lock
# Load environment variables
env_vars = dotenv_values('D:\\jarvis\\Jarvis\\.env')
AssistantVoice = env_vars.get("AssistantVoice") or "en-US-GuyNeural"  # Default voice if not set

# Async function to generate audio file
async def TexttoAudio(text, file_path) -> None:
    if os.path.exists(file_path):
        os.remove(file_path)
    communicate = edge_tts.Communicate(text, AssistantVoice, pitch="+5Hz", rate='+13%')
    await communicate.save(file_path)

# Non-blocking TTS function
def non_blocking_tts(text, func=lambda r=None: True):
    def tts_thread():
        # Unique file path per thread to avoid overwrites
        file_path = f'D:\\jarvis\\Jarvis\\Data\\Speech_{threading.current_thread().ident}.mp3'
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(TexttoAudio(text, file_path))
            with queue_lock:
                spoken_text_queue.append(text.lower())
            pygame.mixer.init()
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                if func() == False:
                    break
                pygame.time.Clock().tick(10)

        except Exception as e:
            print(f"Error in TTS: {e}")
        finally:
            try:
                func(False)
                pygame.mixer.music.stop()
                pygame.mixer.quit()
                if os.path.exists(file_path):
                    os.remove(file_path)  # Clean up the file
            except Exception as e:
                print(f'Error in finally block: {e}')
            loop.close()

    thread = threading.Thread(target=tts_thread)
    thread.start()
    # No join() to keep it non-blocking

# Main TextToSpeech function with truncation logic
def TextToSpeech(text, func=lambda r=None: True):
    data = str(text).split('.')

    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information.",
        "There's more text on the chat screen for you, sir.",
        "Sir, take a look at the chat screen for additional text.",
        "You'll find more to read on the chat screen, sir.",
        "Sir, check the chat screen for the rest of the text.",
        "The chat screen has the rest of the text, sir.",
        "There's more to see on the chat screen, sir, please look.",
        "Sir, the chat screen holds the continuation of the text.",
        "You'll find the complete answer on the chat screen, kindly check it out sir.",
        "Please review the chat screen for the rest of the text, sir.",
        "Sir, look at the chat screen for the complete answer."
    ]

    if len(data) > 4 and len(text) >= 250:
        truncated_text = " ".join(text.split('.')[0:2]) + ". " + random.choice(responses)
        non_blocking_tts(truncated_text, func)
    else:
        non_blocking_tts(text, func)

# Test the module standalone
if __name__ == "__main__":
    while True:
        user_input = input("Enter the Text: ")
        TextToSpeech(user_input)