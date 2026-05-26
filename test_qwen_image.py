import os
import sys
import tempfile
from dotenv import load_dotenv
from PIL import Image

# Load .env file
load_dotenv()

# Configure terminal to support UTF-8 (for emojis and Bengali characters on Windows)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from qwen_chat import Qwen
from qwen_chat.core.types.chat import ChatMessage, ImageBlock, TextBlock

def main():
    print("Testing local image auto-upload via qwen-chat package...")
    auth_token = os.getenv("QWEN_AUTH_TOKEN")
    cookie = os.getenv("QWEN_COOKIE")
    
    if not auth_token:
        print("Error: QWEN_AUTH_TOKEN is not set in .env")
        return
        
    # Generate a proper 100x100 solid red PNG image using PIL
    temp_dir = tempfile.gettempdir()
    image_path = os.path.join(temp_dir, "qwen_test_image.png")
    
    img = Image.new("RGB", (100, 100), color="red")
    img.save(image_path, "PNG")
    print(f"Created temporary test image using PIL at: {image_path}")
    
    client = Qwen(log_level="DEBUG")
    
    messages = [
        ChatMessage(
            role="user",
            blocks=[
                TextBlock(text="What color is this image? Please reply with 'The image is red' and 'qwen-chat local image upload works!'"),
                ImageBlock(path=image_path)
            ]
        )
    ]
    
    try:
        print("Sending completions request with local image...")
        response = client.chat.create(
            messages=messages,
            model="qwen3.6-plus",
            temperature=0.7,
            max_tokens=256
        )
        
        # Print the uploaded block details to verify the upload happened
        img_block = messages[0].blocks[1]
        print("\n--- Image Block Post-Upload Metadata ---")
        print(f"URL: {img_block.url}")
        print(f"File ID: {img_block.file_id}")
        print(f"MIME Type: {img_block.image_mimetype}")
        print(f"Filename: {img_block.filename}")
        print(f"Size: {img_block.size}")
        
        print("\n🤖 AI Response:")
        print(response.choices.message.content)
        print("\nqwen-chat Local Image Upload Test Completed!")
    except Exception as e:
        print(f"\nqwen-chat Local Image Upload Test Failed: {e}")
    finally:
        if os.path.exists(image_path):
            os.remove(image_path)
            print("Cleaned up temporary test image.")

if __name__ == "__main__":
    main()
