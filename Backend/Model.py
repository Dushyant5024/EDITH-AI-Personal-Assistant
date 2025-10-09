import cohere  # Cohere ek machine learning platform hai jo AI models provide karta hai, jaise text generation, summarization, etc. Yeh line Cohere Python package ko import karti hai, jisse aap Cohere ke AI models ke saath interact kar sakte ho.
from rich import print  # Rich ek Python library hai jo terminal (console) mein output ko visually attractive banata hai. Isse aap colored text, tables, aur markdown easily print kar sakte ho. Yeh line print function ko import karti hai, jisse aap apne console output ko format kar sakte ho (jaise ki colorful text print karna).
from dotenv import dotenv_values  # dotenv ek library hai jo environment variables ko manage karne mein madad karti hai. Yeh line dotenv_values function ko import karti hai, jo aapke .env file ko read kar ke usme jo bhi variables hain, unhe Python dictionary mein load kar leta hai.

# .env file se environment variables ko load karte hain
env_vars = dotenv_values("C:/Users/dushy/OneDrive/Desktop/EDITH AI/.env")
CohereAPIKey = env_vars.get("CohereAPIKey") # API key ko dictionary se nikalte hain
print("API Key is:", repr(CohereAPIKey))
co = cohere.Client(api_key=CohereAPIKey)  # Cohere client object banate hain jo AI se interact karega

# Recognized function keywords define kar rahe hain jo AI output ko classify karne mein madad karega
funcs = [
    "exit", "general", "realtime", "open", "close", "play",
    "generate image", "system", "content", "google search",
    "youtube search", "reminder"
]

# Conversation ke messages store karne ke liye ek list
messages = []

# Preamble define karte hain jo AI ko batata hai kis type ke prompt ke liye kya output dena hai
preamble = """
You are a very accurate Decision-Making Model, which decides what kind of a query is given to you.
You will decide whether a query is a 'general' query, a 'realtime' query, or is asking to perform any task or automation like 'open facebook, instagram', 'can you write a application and open it in notepad'
*** Do not answer any query, just decide what kind of query is given to you. ***
-> Respond with 'general ( query )' if a query can be answered by a llm model (conversational ai chatbot) and doesn't require any up to date information like if the query is 'who was akbar?' respond with 'general who was akbar?', if the query is 'how can i study more effectively?' respond with 'general how can i study more effectively?', if the query is 'can you help me with this math problem?' respond with 'general can you help me with this math problem?', if the query is 'Thanks, i really liked it.' respond with 'general thanks, i really liked it.' , if the query is 'what is python programming language?' respond with 'general what is python programming language?', etc. Respond with 'general (query)' if a query doesn't have a proper noun or is incomplete like if the query is 'who is he?' respond with 'general who is he?', if the query is 'what's his networth?' respond with 'general what's his networth?', if the query is 'tell me more about him.' respond with 'general tell me more about him.', and so on even if it require up-to-date information to answer. Respond with 'general (query)' if the query is asking about time, day, date, month, year, etc like if the query is 'what's the time?' respond with 'general what's the time?'.
-> Respond with 'realtime ( query )' if a query can not be answered by a llm model (because they don't have realtime data) and requires up to date information like if the query is 'who is indian prime minister' respond with 'realtime who is indian prime minister', if the query is 'tell me about facebook's recent update.' respond with 'realtime tell me about facebook's recent update.', if the query is 'tell me news about coronavirus.' respond with 'realtime tell me news about coronavirus.', etc and if the query is asking about any individual or thing like if the query is 'who is akshay kumar' respond with 'realtime who is akshay kumar', if the query is 'what is today's news?' respond with 'realtime what is today's news?', if the query is 'what is today's headline?' respond with 'realtime what is today's headline?', etc.
-> Respond with 'open (application name or website name)' if a query is asking to open any application like 'open facebook', 'open telegram', etc. but if the query is asking to open multiple applications, respond with 'open 1st application name, open 2nd application name' and so on.
-> Respond with 'close (application name)' if a query is asking to close any application like 'close notepad', 'close facebook', etc. but if the query is asking to close multiple applications or websites, respond with 'close 1st application name, close 2nd application name' and so on.
-> Respond with 'play (song name)' if a query is asking to play any song like 'play afsanay by ys', 'play let her go', etc. but if the query is asking to play multiple songs, respond with 'play 1st song name, play 2nd song name' and so on.
-> Respond with 'generate image (image prompt)' if a query is requesting to generate a image with given prompt like 'generate image of a lion', 'generate image of a cat', etc. but if the query is asking to generate multiple images, respond with 'generate image 1st image prompt, generate image 2nd image prompt' and so on.
-> Respond with 'reminder (datetime with message)' if a query is requesting to set a reminder like 'set a reminder at 9:00pm on 25th june for my business meeting.' respond with 'reminder 9:00pm 25th june business meeting'.
-> Respond with 'system (task name)' if a query is asking to mute, unmute, volume up, volume down , etc. but if the query is asking to do multiple tasks, respond with 'system 1st task, system 2nd task', etc.
-> Respond with 'content (topic)' if a query is asking to write any type of content like application, codes, emails or anything else about a specific topic but if the query is asking to write multiple types of content, respond with 'content 1st topic, content 2nd topic' and so on.
-> Respond with 'google search (topic)' if a query is asking to search a specific topic on google but if the query is asking to search multiple topics on google, respond with 'google search 1st topic, google search 2nd topic' and so on.
-> Respond with 'youtube search (topic)' if a query is asking to search a specific topic on youtube but if the query is asking to search multiple topics on youtube, respond with 'youtube search 1st topic, youtube search 2nd topic' and so on.
*** If the query is asking to perform multiple tasks like 'open facebook, telegram and close whatsapp' respond with 'open facebook, open telegram, close whatsapp' ***
*** If the user is saying goodbye or wants to end the conversation like 'bye EDITH.' respond with 'exit'.***
*** Respond with 'general (query)' if you can't decide the kind of query or if a query is asking to perform a task which is not mentioned above. ***
"""

# Predefined examples dene ke liye ek chat history jisse AI ko context mile
ChatHistory = [
    {"role": "User", "message": "how are you?"},
    {"role": "Chatbot", "message": "general how are you?"},
    {"role": "User", "message": "do you like pizza?"},
    {"role": "Chatbot", "message": "general do you like pizza?"},
    {"role": "User", "message": "open chrome and tell me about mahatma gandhi."},
    {"role": "Chatbot", "message": "open chrome, general tell me about mahatma gandhi."},
    {"role": "User", "message": "open chrome and firefox"},
    {"role": "Chatbot", "message": "open chrome, open firefox"},
    {"role": "User", "message": "what is today's date and by the way remind me that i have a dancing performance on 5th aug at 11pm"},
    {"role": "Chatbot", "message": "general what is today's date, reminder 11:00pm 5th aug dancing performance"},
    {"role": "User", "message": "chat with me."},
    {"role": "Chatbot", "message": "general chat with me."}
]

# Main function jo user input ko process karega aur uska type decide karega

def FirstLayerDMM(prompt: str = "test"):
    messages.append({"role": "user", "content": f"{prompt}"})  # User prompt ko messages mein add karte hain

    # AI model se chat stream start karte hain
    stream = co.chat_stream(
        model="command-r-plus",  # Cohere ka powerful model use ho raha hai
        message=prompt,
        temperature=0.7,  # Creativity level set karte hain
        chat_history=ChatHistory,
        prompt_truncation="OFF",
        connectors=[],
        preamble=preamble
    )

    response = ""  # Response ko build karne ke liye empty string
    for event in stream:
        if event.event_type == "text-generation":
            response += event.text  # AI ke generated text ko response mein jodte hain

    response = response.replace("\n", "")  # Newline hata dete hain
    response = response.split(",")  # Response ko alag tasks mein todte hain
    response = [i.strip() for i in response]  # Har task ke aage peeche spaces hata dete hain

    temp = []
    for task in response:
        for func in funcs:
            if task.startswith(func):  # Agar task kisi valid function se start hota hai to usse temp mein daal dete hain
                temp.append(task)

    response = temp

    # Agar response mein '(query)' aata hai to dubara function call karke aur clear output nikalte hain
    if "(query)" in response:
        newresponse = FirstLayerDMM(prompt=prompt)
        return newresponse
    else:
        return response  # Final response return karte hain

# Agar script run ki ja rahi ho directly, to yeh block chalega
if __name__ == "__main__":
    while True:
        print(FirstLayerDMM(input(">>> ")))  # User se input le kar uska type predict karke print karte hain
