# AI Image Generator - Pixelated Style

This is a Python application that generates pixelated images using AI. The app features:

- Main canvas for displaying generated images
- Chat panel for entering generation and modification commands
- Tool panel with common image modification tools
- Automatic pixelated style for all generated images

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

3. Run the application:
```bash
python main.py
```

## Features

- **Image Generation**: Use natural language prompts to generate pixelated images
- **Image Modification**: Modify existing images with additional prompts
- **Save/Load**: Save generated images to disk and load them back
- **Pixelate Tool**: Apply additional pixelation effects
- **Resize Tool**: Resize images while maintaining pixelated style
- **Clear Canvas**: Clear the current image

## Usage

1. Enter a prompt in the chat panel (e.g., "a cute cat in a forest")
2. Click "Generate" to create a new pixelated image
3. Use "Modify" to make changes to the current image
4. Use the tool panel for additional image operations
