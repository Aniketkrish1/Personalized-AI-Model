import pyttsx3
import threading
import asyncio
from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import os
import comtypes

# Load environment variables
env_vars = dotenv_values('D:\jarvis\Jarvis\.env')
GroqAPIKEY = env_vars.get("GroqAPI")

# Google search classes and user agent
classes = ["zCubwf", "hgKElc", "LTKOO sY7ric", "ZOLcW", "“gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta",
"IZ6rdc", "“O5uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table__webanswers-table", "dDoNo ikb4Bb gsrt", "sXLaQe",
"LwkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

user_agent = "Mozilla/5.0 (Windows NT 10.0;Win64;x64) AppleWebkit/537.36 (KHTML,like Gecko) Chrome/89.0.142.86 Safari/537.36"

# Initialize Groq client
client = Groq(api_key=GroqAPIKEY)
messages =[]
# Text-to-speech function
def text_to_speech(text):
    # Initialize COM for this thread
    comtypes.CoInitialize()
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        engine.say(text)
        engine.runAndWait()
    finally:
        # Uninitialize COM when done
        comtypes.CoUninitialize()

# Speak and execute simultaneously
def speak_and_execute(text):
    speech_thread = threading.Thread(target=text_to_speech, args=(text,))
    speech_thread.start()
    # No join() here to avoid blocking execution

# Existing functions (unchanged for brevity)
def GoogleSearch(Topic):
    search(Topic)
    return True

def Content(Topic):
    def OpenNotepad(file):
        default_text_editor = 'notepad.exe'
        subprocess.Popen([default_text_editor, file])

    def ContentWriterAI(prompt):
        messages.append({'role': 'user', 'content': f'{prompt}'})
        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=SystemChatbot + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )
        Answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content
        Answer = Answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": Answer})
        return Answer

    Topic = Topic.replace("Content ", "")
    contentbyAI = ContentWriterAI(Topic)
    with open(rf"D:\jarvis\Jarvis\Data\{Topic.lower().replace(' ','')}.txt", 'w', encoding='utf-8') as file:
        file.write(contentbyAI)
    OpenNotepad(rf'D:\jarvis\Jarvis\Data\{Topic.lower().replace(" ","")}.txt')
    return True

def YoutubeSearch(Topic):
    Url4search = f'https://www.youtube.com/results?search_query={Topic}'
    webbrowser.open(Url4search)
    return True

def PlayYoutube(Topic):
    playonyt(Topic)
    return True

def OpenApp(app_name, sess=requests.session()):
    try:
        if app_name=="chrome":
            subprocess.Popen(["C:\Program Files\Google\Chrome\Application\chrome.exe" ,"--profile-directory='Default'"])
        print(f"🎯 Trying to open {app_name} locally...")
        appopen(app_name, match_closest=True, output=True, throw_error=True)
        print(f"✅ Successfully opened {app_name}")
        return True
    except Exception as e:
        print(f"⚠️ App not found: {e}. Searching online...")
        def extract_links(html):
            if not html:
                return []
            soup = BeautifulSoup(html, 'html.parser')
            links = soup.find_all('a', {'jsname': 'UWckNb'})
            return [link.get('href') for link in links] if links else []

        def search_google(query):
            url = f'https://www.google.com/search?q={query}'
            headers = {'User-Agent': user_agent}
            response = sess.get(url, headers=headers)
            return response.text if response.status_code == 200 else None

        html = search_google(app_name)
        links = extract_links(html)
        if links:
            print(f"🔍 Opening {app_name} website: {links[0]}")
            webopen(links[0])
        else:
            print(f"❌ No search results found for {app_name}.")
        return True

def Closeapp(app):
    if 'chrome' in app:
        pass
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)
            return True
        except:
            return False

def System(command):
    def mute(): keyboard.press_and_release("volume mute")
    def unmute(): keyboard.press_and_release("volume mute")
    def volume_up(): keyboard.press_and_release("volume up")
    def volume_down(): keyboard.press_and_release("volume down")

    if command == 'mute': mute()
    elif command == 'unmute': unmute()
    elif command == 'volume up': volume_up()
    elif command == 'volume down': volume_down()
    return True

# Modified TranslateAndExecute with speech
async def TranslateAndExecute(commands: list[str]):
    func = []
    for command in commands:
        # Speak the command being executed

        if command.startswith("open "):
            if "open it" not in command and "open file" not in command:
                speak_and_execute(f"Opening {command.split()[1:]}")
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))
                func.append(fun)

        elif command.startswith("general "):
            pass
        elif command.startswith("realtime "):
            pass
        elif command.startswith("close "):
            speak_and_execute(f"Closing {command.split()[1:]}")
            fun = asyncio.to_thread(Closeapp, command.removeprefix("close "))
            func.append(fun)
        elif command.startswith("play "):
            speak_and_execute(f"Playing {command.split()[1:]}")
            fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play "))
            func.append(fun)
        elif command.startswith("google search "):
            speak_and_execute(f"Searching {command.split()[2:]}")
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))
            func.append(fun)
        elif command.startswith("youtube search "):
            speak_and_execute(f"Searching {command.split()[2:]}")
            fun = asyncio.to_thread(YoutubeSearch, command.removeprefix("youtube search "))
            func.append(fun)
        elif command.startswith("system "):
            fun = asyncio.to_thread(System, command.removeprefix("system "))
            func.append(fun)
        else:
            speak_and_execute(f'No Function found for {command}')

    results = await asyncio.gather(*func)
    for result in results:
        if isinstance(result, str):
            print(result)
            yield result
        else:
            yield result

async def Automation(commands: list[str]):
    async for result in TranslateAndExecute(commands):
        pass
    return True


if __name__=="__main__":
    commands=['play abcd','open youtube','google search python','youtube search despacito']
    asyncio.run(Automation(commands))