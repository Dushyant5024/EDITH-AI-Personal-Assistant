import asyncio
import os
from random import randint
from PIL import Image
import requests
from dotenv import get_key
from time import sleep

# API setup
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {
    "Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPIKey')}"
}

# Use correct folder
folder_path = os.path.join("Frontend", "Files", "ImageGeneration", "data")
os.makedirs(folder_path, exist_ok=True)

# Send image request
async def query(payload):
    response = await asyncio.to_thread(
        requests.post, API_URL, headers=headers, json=payload
    )
    return response.content

# Generate images
async def generate_images(prompt: str):
    prompt_sanitized = prompt.replace(" ", "_")
    tasks = []
    for i in range(1, 5):
        payload = {
            "inputs": f"{prompt}, quality=4K, sharpness=maximum, Ultra High details, high resolution, seed={randint(0, 1_000_000)}"
        }
        tasks.append(asyncio.create_task(query(payload)))

    image_bytes_list = await asyncio.gather(*tasks)

    for i, image_bytes in enumerate(image_bytes_list, start=1):
        image_path = os.path.join(folder_path, f"{prompt_sanitized}{i}.jpg")
        with open(image_path, "wb") as f:
            f.write(image_bytes)
        print(f"Saved image: {image_path}")

# Show images
def open_images(prompt):
    folder_path = os.path.join("Frontend", "Files", "ImageGeneration", "data")
    prompt = prompt.replace(" ", "_")
    files = [f"{prompt}{i}.jpg" for i in range(1, 5)]

    for file in files:
        image_path = os.path.join(folder_path, file)
        try:
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)
        except IOError:
            print(f"Unable to open image: {image_path}")

# Run
if __name__ == "__main__":
    user_prompt = input("Enter your prompt to generate images: ")
    asyncio.run(generate_images(user_prompt))
    open_images(user_prompt)
