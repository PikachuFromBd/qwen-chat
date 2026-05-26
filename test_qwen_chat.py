import os
import sys
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Configure terminal to support UTF-8 (for emojis and Bengali characters on Windows)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Add the local directory to sys.path to run directly from local source
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from qwen_chat import Qwen
from qwen_chat.core.types.chat import ChatMessage

def main():
    print("Testing newly branded qwen-chat package...")
    auth_token = os.getenv("QWEN_AUTH_TOKEN")
    cookie = os.getenv("QWEN_COOKIE")
    
    if not auth_token:
        print("Error: QWEN_AUTH_TOKEN is not set in .env")
        return
        
    client = Qwen()
    messages = [
        ChatMessage(
            role="user",
            content="Hello Qwen! Say hello in Bengali and tell me you are operating on qwen-chat package."
        )
    ]
    
    try:
        print("Sending completions request...")
        response = client.chat.create(
            messages=messages,
            model="qwen3.6-plus",
            temperature=0.7,
            max_tokens=256
        )
        print("\n🤖 AI Response:")
        print(response.choices.message.content)
        print("\nqwen-chat Package Test Passed!")
    except Exception as e:
        print(f"\nqwen-chat Package Test Failed: {e}")

if __name__ == "__main__":
    main()
