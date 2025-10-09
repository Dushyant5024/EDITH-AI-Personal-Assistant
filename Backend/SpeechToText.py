# Selenium se browser automation ke liye WebDriver import
from selenium import webdriver

# Web page ke elements find karne ke liye By class
from selenium.webdriver.common.by import By

# ChromeDriver ko background service ki tarah chalane ke liye
from selenium.webdriver.chrome.service import Service

# Chrome browser ke settings (headless mode, language, etc.) ke liye
from selenium.webdriver.chrome.options import Options

# ChromeDriver ka automatic setup (no manual download)
from webdriver_manager.chrome import ChromeDriverManager

# .env file se variables load karne ke liye
from dotenv import dotenv_values

# System-level operations jaise file access, env vars ke liye
import os ,time

# Text translation ke liye (Google Translate ki unofficial library)
import mtranslate as mt


# .env file ke saare variables ek dict ke form me load karo
env_vars = dotenv_values(".env")

# Input language (.env file se) ko variable me store karo
InputLanguage = env_vars.get("InputLanguage")

HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new webkitSpeechRecognition() || new SpeechRecognition();
            recognition.lang = '';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            recognition.stop();
            output.innerHTML = "";
        }
    </script>
</body>
</html>'''

# HTML code me recognition language ko set karna
HtmlCode = str(HtmlCode).replace(
    "recognition.lang = '';", 
    f"recognition.lang = '{InputLanguage}';"
)

# HTML file ko write karna
with open(r"Data/Voice.html", "w") as f:
    f.write(HtmlCode)

# Current working directory lena
current_dir = os.getcwd()

# HTML file ka path banana
Link = f"{current_dir}/Data/Voice.html"

# WebDriver ke options set karna
chrome_options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36"
chrome_options.add_argument(f"user-agent={user_agent}")
chrome_options.add_argument("--use-fake-ui-for-media-stream")     # Mic permission simulate karna
chrome_options.add_argument("--use-fake-device-for-media-stream") # Fake mic use karna
chrome_options.add_argument("--headless=new")                     # Browser ko background me chalana

# Chrome WebDriver setup karna
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Temporary files ka path set karna
TempDirPath = rf"{current_dir}/Frontend/Files"

# Assistant ka status likhne ke liye function
def SetAssistantStatus(Status):
    with open(rf"{TempDirPath}/Status.data", "w", encoding="utf-8") as file:
        file.write(Status)

# Query format karne ka function
def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you", "what’s", "where’s", "how’s"]

    # Agar query question hai to question mark lagao
    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + '?'
        else:
            new_query += "?"
    else:
        # Agar question nahi to full stop lagao
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + '.'
        else:
            new_query += "."

    return new_query.capitalize()

# Language translate karne ka function
def UniversalTranslator(Text):
    english_translation = mt.translate(Text, "en", "auto")
    return english_translation.capitalize()

# Speech recognition start karne ka function
def SpeechRecognition():
    driver.get("file:///" + Link)  # HTML file browser me open karna
    driver.find_element(by=By.ID, value="start").click()  # Start button click

    prev_text = ""
    timeout = 15  # seconds
    start_time = time.time()

    while True:
        try:
            # Output se recognized text lena
            Text = driver.find_element(by=By.ID, value="output").text.strip()

            if Text != prev_text and Text != "":
                driver.find_element(by=By.ID, value="end").click()  # End button click

                if InputLanguage.lower().startswith("en"):
                    return QueryModifier(Text)
                else:
                    SetAssistantStatus("Translating ...")
                    return QueryModifier(UniversalTranslator(Text))

            prev_text = Text

            # Timeout to prevent infinite loop
            if time.time() - start_time > timeout:
                driver.find_element(by=By.ID, value="end").click()
                return "No speech detected."

        except Exception as e:
            print("Error:", e)
            break

# Main block - repeatedly recognition chalayega
if __name__ == "__main__":
    while True:
        Text = SpeechRecognition()
        print(Text)