import pygame  # Sound play karne ke liye
import random  # Random message choose karne ke liye
import asyncio  # Async function run karne ke liye
import edge_tts  # Microsoft Edge ka TTS API
import os  # File handling ke liye
from dotenv import dotenv_values  # .env file se variable load karne ke liye

# Voice config load kar rahe hain from .env file
env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice", "en-IN-NeerjaNeural")

# Text ko audio file (mp3) mein convert karta hai
async def TextToAudioFile(text) -> None:
    file_path = "Data/speech.mp3"
    if os.path.exists(file_path):  # Agar file already hai to delete karo
        os.remove(file_path)
    communicate = edge_tts.Communicate(text, AssistantVoice, pitch='+5Hz', rate='+13%')  # Voice config
    await communicate.save(file_path)  # MP3 save karta hai

# MP3 play karta hai using pygame
def TTS(Text, func=lambda r=None: True):
    while True:
        try:
            asyncio.run(TextToAudioFile(Text))  # Text se MP3 banate hain
            pygame.mixer.init()  # Pygame ka sound system start
            pygame.mixer.music.load("Data/speech.mp3")  # File load
            pygame.mixer.music.play()  # Play audio

            # Jab tak audio chal raha hai
            while pygame.mixer.music.get_busy():
                if func() == False:  # Agar beech mein rokna hai to break
                    break
                pygame.time.Clock().tick(10)

            return True  # Success

        except Exception as e:
            print(f"Error in TTS: {e}")  # Error print
        finally:
            try:
                func(False)  # Callback
                pygame.mixer.music.stop()  # Stop music
                pygame.mixer.quit()  # Quit mixer
            except Exception as e:
                print(f"Error in cleanup: {e}")

# Long text ka smart handling
def TextToSpeech(Text, func=lambda r=None: True):
    Data = str(Text).split(".")  # Text ko sentence mein tod do
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

    # Agar text lamba hai to sirf pehla part bol ke batata hai
    if len(Data) > 4 and len(Text) >= 250:
        TTS(".".join(Data[0:2]) + ". " + random.choice(responses), func)
    else:
        TTS(Text, func)  # Short text to pura bol do

# Main loop for user input
if __name__ == "__main__":
    print("Voice Assistant Ready! Type 'exit' to quit.")
    while True:
        user_input = input("Enter the text: ")  # User se input lo
        if user_input.lower() == "exit":
            print(" Goodbye!")  # Exit condition
            break
        TextToSpeech(user_input)  # Text bol do
