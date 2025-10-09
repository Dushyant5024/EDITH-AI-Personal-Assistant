from googlesearch import search  # Google par query search karne ke liye
from groq import Groq  # Groq AI model ko access karne ke liye
from json import load, dump  # Chat log file ko read/write karne ke liye
import datetime  # Real-time date aur time lene ke liye
from dotenv import dotenv_values  # .env file se values (jaise API key) lene ke liye

# .env file se values nikalte hain
env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Groq AI client setup kar rahe hain
client = Groq(api_key=GroqAPIKey)

# Bot ka behavior define karte hain (Updated instructions for better control)
System = f"""
Hello! I am {Username}, and you are {Assistantname}, an intelligent AI assistant with access to real-time search capabilities.

Please follow these guidelines strictly:
1. Answer clearly, briefly, and professionally.
2. Use correct grammar, punctuation (full stops, commas, question marks, etc.).
3. Respond only using the given search data — don't assume anything.
4. If data is insufficient, reply with: "Sorry, I couldn’t find accurate information."
5. Always stay helpful, polite, and accurate.
6. Don't give personal opinions — respond factually.

Let’s make sure users get the best experience from your responses.
"""

# Chat history file load ya create karte hain
try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)
except:
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)

# Initial system conversation setup
SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello, how can I help you?"}
]

# Google search function: query ke liye top 5 results leta hai
def GoogleSearch(query):
    results = list(search(query, advanced=True, num_results=5))
    Answer = f"The search results for '{query}' are:\n[start]\n"
    for i in results:
        Answer += f"Title: {i.title}\nDescription: {i.description}\n"
    Answer += "[end]"
    return Answer

# Blank lines hata ke clean answer banata hai
def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

# Real-time date and time info deta hai
def Information():
    data = ""
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")
    
    data += f"Use This Real-time Information if needed:\n"
    data += f"Day: {day}\n"
    data += f"Date: {date}\n"
    data += f"Month: {month}\n"
    data += f"Year: {year}\n"
    data += f"Time: {hour} hours, {minute} minutes, {second} seconds.\n"
    return data

# User ke prompt par AI se response generate karta hai
def RealtimeSearchEngine(prompt):
    global SystemChatBot, messages  # Global variables ka use ho raha hai

    # Purani chat history load karo
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)

    # Sirf last 10 messages hi lo (token limit control karne ke liye)
    messages = messages[-10:]

    # User ka current prompt message me add karo
    messages.append({"role": "user", "content": prompt})

    # Google search results lao
    search_results = GoogleSearch(prompt)
    if len(search_results) > 2000:  # Zyada bada result truncate karo
        search_results = search_results[:2000]

    # Real-time date/time info
    system_info = Information()
    if len(system_info) > 500:  # Zyada lamba info bhi truncate karo
        system_info = system_info[:500]

    # System role messages prepare karo
    current_system = {"role": "system", "content": search_results}
    current_info = {"role": "system", "content": system_info}

    # Final message list banayi ja rahi hai
    final_messages = SystemChatBot + [current_system, current_info] + messages

    # Groq AI ko request bhejo (stream mode me)
    completion = client.chat.completions.create(
        model="llama3-70b-8192",       # LLaMA 3 model use ho raha hai
        messages=final_messages,       # Messages ka complete stack
        temperature=0.7,               # Creativity level
        max_tokens=2048,               # Max output length
        top_p=1,
        stream=True,                   # Streaming response enable hai
        stop=None
    )

    Answer = ""  # AI response yahan build hoga
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content  # Chunk-by-chunk jodna

    Answer = Answer.strip().replace("</s>", "")  # Clean unwanted token

    # Assistant ka response message list me save karo
    messages.append({"role": "assistant", "content": Answer})

    # Updated chat log wapas JSON file me save karo
    with open(r"Data\ChatLog.json", "w") as f:
        dump(messages, f, indent=4)

    # SystemChatBot clean karna (to prevent buildup)
    if len(SystemChatBot) > 3:
        SystemChatBot = SystemChatBot[:3]

    # Final answer ko return karo after formatting
    return AnswerModifier(Answer=Answer)

# Program ka main loop — user input lega aur result dikhayega
if __name__ == "__main__":
    while True:
        prompt = input("Enter your query: ")
        print(RealtimeSearchEngine(prompt))
        prompt = prompt[:3000]