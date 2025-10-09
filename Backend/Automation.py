# Zaroori libraries import kar rahe hain
from AppOpener import close, open as appopen  # Apps ko open/close karne ke liye
from webbrowser import open as webopen        # Browser me koi bhi URL open karne ke liye
from pywhatkit import search, playonyt        # Google search aur YouTube video play karne ke liye
from dotenv import dotenv_values               # .env file se API keys wagairah load karne ke liye
from bs4 import BeautifulSoup                  # Web page ke HTML content ko parse karne ke liye
from rich import print                         # Stylish output print karne ke liye
from groq import Groq                          # Groq AI se content generate karne ke liye
import webbrowser                              # Browser open karne ke liye (backup)
import subprocess                              # System-level commands run karne ke liye
import requests                                # Web requests bhejne ke liye
import keyboard                                # Keyboard shortcuts (volume etc.) handle karne ke liye
import asyncio                                 # Asynchronous task run karne ke liye
import os                                      # OS-level info aur features ke liye

# .env file se API key load kar rahe hain
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")  # Groq API key nikal rahe hain

# Google result se data nikalne ke liye classes define ki gayi hain
classes = ["zCubwf", "hgKElc", "LTKOO sY7ric", "Z0LcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee",
           "tw-Data-text tw-text-small tw-ta", "IZ6rdc", "O5uR6d LTKOO", "vLzY6d",
           "webanswers-webanswers_table__webanswers-table", "dONo ikb4Bb gsrt", "sXLa0e",
           "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

# Web request bhejne ke liye ek fake user-agent use kar rahe hain
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

# Groq client initialize kiya gaya hai
client = Groq(api_key=GroqAPIKey)

# Professional replies agar user formal baat kare
professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need—don't hesitate to ask."
]

# Chat messages store karne ke liye list
messages = []

# System-level instruction message for Groq chatbot
SystemChatBot = [{
    "role": "system",
    "content": f"Hello, I am {os.environ['Username']}, You're a content writer. You have to write content."
}]

# Google Search function
def GoogleSearch(Topic):
    search(Topic)  # pywhatkit ka search function use kar rahe hain
    return True

# Content generation function using Groq AI
def Content(Topic):

    def OpenNotepad(File):  # File ko Notepad mein open karne ka function
        default_text_editor = 'notepad.exe'
        subprocess.Popen([default_text_editor, File])

    def ContentWriterAI(prompt):  # Groq se content likhwaane ka function
        messages.append({"role": "user", "content": f"{prompt}"})

        completion = client.chat.completions.create(
            model="llama3-70b-8192",  # Use ho raha AI model
            messages=SystemChatBot + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer = ""
        for chunk in completion:  # Streamed response collect kar rahe hain
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content
        Answer = Answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": Answer})
        return Answer

    Topic: str = Topic.replace("Content", "")
    ContentByAI = ContentWriterAI(Topic)

    with open(rf"Data\{Topic.lower().replace(' ', '')}.txt", "w", encoding="utf-8") as file:
        file.write(ContentByAI)
        file.close()

    OpenNotepad(rf"Data\{Topic.lower().replace(' ', '')}.txt")
    return True

# YouTube par search karne ka function
def YouTubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(Url4Search)
    return True

# YouTube video play karne ka function
def PlayYoutube(query):
    playonyt(query)  # pywhatkit ke playonyt se top video play karta hai
    return True

# App open karne ka function, fallback ke sath
def OpenApp(app, sess=requests.session()):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True
    except:
         print(f"[INFO] App '{app}' not found. Trying fallback...")
        
        # Try opening official site on Google
         query = f"{app} official site"
         url = f"https://www.google.com/search?q={query}"
         webopen(url)
         return False
    

# App close karne ka function
def CloseApp(app):
    if "chrome" in app:
        pass  # Chrome ko skip kar diya gaya hai
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)
            return True
        except:
            return False

# System-level volume control
def System(command):

    def mute():  # Volume mute
        keyboard.press_and_release("volume mute")

    def unmute():  # Volume unmute
        keyboard.press_and_release("volume mute")

    def volume_up():  # Volume increase
        keyboard.press_and_release("volume up")

    def volume_down():  # Volume decrease
        keyboard.press_and_release("volume down")

    # Command check kar ke respective action
    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()
    return True

# Async function to translate and execute user commands
async def TranslateAndExecute(commands: list[str]):
    funcs = []

    for command in commands:
        if command.startswith("open "):
            if "open it" in command or command == "open file":
                pass
            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))
                funcs.append(fun)

        elif command.startswith("general "):
            pass  # placeholder

        elif command.startswith("realtime "):
            pass  # placeholder

        elif command.startswith("close "):
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))
            funcs.append(fun)

        elif command.startswith("play"):
            fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play"))
            funcs.append(fun)

        elif command.startswith("content"):
            fun = asyncio.to_thread(Content, command.removeprefix("content"))
            funcs.append(fun)

        elif command.startswith("google search"):
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search"))
            funcs.append(fun)

        elif command.startswith("youtube search"):
            fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search"))
            funcs.append(fun)

        elif command.startswith("system"):
            fun = asyncio.to_thread(System, command.removeprefix("system"))
            funcs.append(fun)

        else:
            print(f"No Function Found. For {command}")

    results = await asyncio.gather(*funcs)
    for result in results:
        if isinstance(result, str):
            yield result
        else:
            yield result

# High-level automation wrapper
async def Automation(commands: list[str]):
    async for result in TranslateAndExecute(commands):
        pass
    return True

if __name__ == "__main__":
    asyncio.run(Automation(["open Facebook","open telegram","open instagram","play afsanay","content song for me"]))
