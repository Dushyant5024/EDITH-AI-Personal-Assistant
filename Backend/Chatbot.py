from groq import Groq                 # Groq library import kar rahe hain (AI model ke liye)
from json import load, dump          # JSON file read/write karne ke functions
import datetime                      # Date aur time ke liye module
from dotenv import dotenv_values     # .env file se variables lene ke liye

# .env file se sab environment variables load kar rahe hain
env_vars = dotenv_values("C:/Users/dushy/OneDrive/Desktop/EDITH AI/.env")
print(env_vars)

# Alag variables ko .env se fetch kar rahe hain
Username = env_vars.get("Username")               # User ka naam
Assistantname = env_vars.get("Assistantname")     # Assistant ka naam
GroqAPIKey = env_vars.get("GroqAPIKey")           # Groq API key (AI access ke liye)
if not GroqAPIKey:
    print("GroqAPIKey not found! Check your .env formatting.")
    exit()

# Groq client object bana rahe hain (API key ke saath)
client = Groq(api_key=GroqAPIKey)

# Chat messages store karne ke liye ek khaali list
messages = []

# Define a system message that provides context to the AI chatbot about its roleand behavior.
System = f"""
You are {Assistantname}, an intelligent, friendly, and highly capable AI assistant created for fast and smart conversation. You are running on an advanced model optimized for GPT-like responses. I am your user, {Username}.

   GENERAL INSTRUCTIONS:
- Always respond in fluent, clear, and correct English.
- Keep your answers accurate, concise, and to the point.
- When appropriate, give step-by-step reasoning like a tutor.
- If user asks a vague question, clarify politely.
- Use bullet points or numbered steps if it improves readability.
- Answer like an expert, not like a robot or a language model.

    COMMUNICATION STYLE:
- Maintain a respectful and helpful tone.
- Be formal, but friendly and engaging.
- Do NOT apologize unnecessarily or give disclaimers about being an AI.
- Do NOT mention Groq, LLaMA, your training, or AI development.

    TECHNICAL ABILITIES:
- You can explain code (Python, JavaScript, etc.) and debug it.
- You can write, correct, or improve short scripts or snippets.
- You can solve math problems, logic questions, and give examples.
- You can summarize articles, explain complex topics, or generate creative ideas.

    CONTEXT HANDLING:
- You remember past questions from this session.
- You can refer to previous parts of the chat to maintain consistency.
- You must incorporate real-time data if provided (e.g., time/date from system).

    RESTRICTIONS:
- Do NOT tell the current time unless explicitly asked.
- Do NOT share confidential data or make guesses without basis.
- Avoid saying things like “as an AI model” or “I do not have emotions”.

Your goal is to be the fastest, most accurate, and human-like assistant. Think clearly and behave like ChatGPT or Google Bard with the speed of Groq.
"""

# Chatbot ke system instructions
SystemChatBot = [
    {"role": "system", "content": System}  # System prompt set kiya ja raha hai
]

# Chat log file ko read karne ki koshish karte hain
try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)  # Pehle se saved messages ko load karte hain
except FileNotFoundError:
    # Agar file nahi mili to ek empty JSON file create karte hain
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)  # Khali list likhte hain file me

# Real-time date aur time lene ke liye function
def RealtimeInformation():
    current_date_time = datetime.datetime.now()  # Abhi ka date/time lete hain
    day = current_date_time.strftime("%A")       # Din ka naam (Monday, etc.)
    date = current_date_time.strftime("%d")      # Din ki date (01, 02, etc.)
    month = current_date_time.strftime("%B")     # Month ka naam (May, etc.)
    year = current_date_time.strftime("%Y")      # Saal (2025, etc.)
    hour = current_date_time.strftime("%H")      # 24-hour format me hour
    minute = current_date_time.strftime("%M")    # Minute
    second = current_date_time.strftime("%S")    # Second

# Real-time info ko string me convert kar rahe hain
    data = f"Please use this real-time information if needed,\n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} hours :{minute} minutes :{second} seconds.\n"
    return data

# Chatbot ke response ko format karne ka function
def AnswerModifier(Answer):
    lines = Answer.split('\n')  # Answer ko lines me split karte hain
    non_empty_lines = [line for line in lines if line.strip()]  # Khaali lines hata rahe hain
    modified_answer = '\n'.join(non_empty_lines)  # Cleaned lines ko wapas jod rahe hain
    return modified_answer

# Chatbot function jo user ka query handle karta hai
def ChatBot(Query):
    """User ke query ko process karke AI ka response return karta hai."""
    try:
        # JSON file se pehle ke messages load kar rahe hain
        with open(r"Data\ChatLog.json", "r") as f:
            messages = load(f)

        # User ka query messages list me add kar rahe hain general formation of function
        messages.append({"role": "user", "content": f"{Query}"})

        # Groq API se response lene ke liye request kar rahe hain
        completion = client.chat.completions.create(
            model="llama3-70b-8192",  # Groq ka LLaMA 3 model use kar rahe hain
            messages=SystemChatBot + [{"role": "system", "content": RealtimeInformation()}] + messages,
            max_tokens=1024,  # Response ka size limit karte hain
            temperature=0.7,  # Kitna random ho response, yeh set karte hain
            top_p=1,  # Sampling strategy ke liye
            stream=True,  # Streaming response on hai
            stop=None  # Model jab tak chahe continue kare
        )

        Answer = ""  # Final answer store karne ke liye variable

        # Streamed content ko chunk by chunk read kar rahe hain
        for chunk in completion:
            if chunk.choices[0].delta.content:  # Agar content hai to...
                Answer += chunk.choices[0].delta.content  # Content ko add karte hain

        Answer = Answer.replace("</s>", "")  # Unwanted tokens hata rahe hain

        # Chatbot ka final response messages me store kar rahe hain
        messages.append({"role": "assistant", "content": Answer})

        # Updated messages ko JSON file me save kar rahe hain
        with open(r"Data\ChatLog.json", "w") as f:
            dump(messages, f, indent=4)

        # Cleaned aur formatted answer return karte hain
        return AnswerModifier(Answer=Answer)

    except Exception as e:
        # Agar error aaye to print karo aur chat log reset karo
        print(f"Error: {e}")
        with open(r"Data\ChatLog.json", "w") as f:
            dump([], f, indent=4)
        return ChatBot(Query)  # Wapas query retry karte hain

# Program ka main entry point
if __name__== "__main__":
    while True:
        user_input = input("Enter Your Question: ")  # User se question le rahe hain

        print(ChatBot(user_input))  # Chatbot ka answer print kar rahe hain
