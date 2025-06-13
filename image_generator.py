"""
Image generation module using OpenAI's DALL-E API
"""

import os
import requests
from io import BytesIO
from PIL import Image
import openai
from dotenv import load_dotenv

load_dotenv()



class ImageGenerator:
    def __init__(self):
        # You will need to set these environment variables or edit the following values.
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "https://rchio-mb1ft4rz-eastus.cognitiveservices.azure.com/")
        api_version = os.getenv("OPENAI_API_VERSION", "2024-04-01-preview")
        api_key = os.getenv("AZURE_OPENAI_API_KEY")

        self.client = openai.AzureOpenAI(
            api_version=api_version,
            azure_endpoint=endpoint,
            api_key=api_key,
        )
    
   
    def generate_image(self, prompt, size="1024x1024"):
        """Generate a new pixelated image from prompt"""
        try:
           
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                quality="standard",
                background="transparent",
                output_format="png",
                n=1,
            )
            
            image_url = response.data[0].url
            
            # Download the image
            image_response = requests.get(image_url)
            image = Image.open(BytesIO(image_response.content))
           
            return image
            
        except Exception as e:
            raise Exception(f"Failed to generate image: {str(e)}")
    
    def modify_image(self, current_image, prompt, size="1024x1024"):
        """Modify existing image based on prompt (simulate with new generation)"""
        # Note: DALL-E 3 doesn't support image editing, so we'll generate a new image
        # with a modified prompt that includes context about the current image
        modify_prompt = f"Modify this concept: {prompt}, pixel art style, 8-bit, pixelated"
        return self.generate_image(modify_prompt, size)
    
