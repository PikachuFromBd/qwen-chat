# qwen-chat 🚀

[![PyPI version](https://img.shields.io/pypi/v/qwen-chat.svg)](https://pypi.org/project/qwen-chat/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)

An unofficial, feature-rich Python SDK and client wrapper for the [Qwen AI](https://chat.qwen.ai) Web API. Enjoy seamless access to advanced models like `qwen3.6-plus` with support for search, deep reasoning, streaming, and automatic local image uploads.

---

## ✨ Features

- **🧠 Complete Model Support**  
  Interact with Qwen's latest web models including `qwen3.6-plus`, `qwen-max-latest`, `qwq-32b`, `qwen2.5-omni-7b`, and specialized vision/coder versions.
  
- **⚡ Synchronous & Asynchronous Clients**  
  Whether you're building a script or a highly concurrent async web server, `qwen-chat` has you covered with native `create()` and `acreate()` workflows.

- **📸 Automatic Local Image Uploads (New!)**  
  Pass a local file path or raw bytes to an `ImageBlock`. The client automatically fetches STS tokens and uploads the image to Alibaba Cloud OSS under the hood—no boilerplate manual upload code required!

- **🌊 Real-time SSE Streaming**  
  Stream token-by-token responses directly to your UI or console, with fully structured chunks and search info outputs.

- **🔍 Integrated Web Search**  
  Toggle real-time search on or off per message to query live web data and receive detailed citations alongside responses.

- **💡 Thinking & Reasoning Controls**  
  Adjust thinking budget settings to enable advanced reasoning capabilities on complex tasks.

---

## 📦 Installation

Install `qwen-chat` via pip:

```bash
pip install qwen-chat
```

---

## ⚙️ Environment Setup

To authenticate requests, extract your `Authorization` bearer token and `Cookie` from the [Qwen Web UI](https://chat.qwen.ai):

1. Go to [https://chat.qwen.ai](https://chat.qwen.ai) and log in.
2. Open developer tools (`F12` or `Ctrl+Shift+I` / `Cmd+Option+I`) and navigate to the **Network** tab.
3. Send any message in the chat interface.
4. Locate the `completions` request (filter by Fetch/XHR).
5. In the request headers:
   - Copy the value of the `Authorization` header **without the word "Bearer "** (just copy the token starting with `eyJ...`).
   - Copy the entire value of the `Cookie` header.
6. Save these values in a `.env` file in the root of your project:

```env
QWEN_AUTH_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
QWEN_COOKIE="cna=...; cnaui=...; token=..."
```

---

## 🚀 Quick Start Examples

### 1. Basic Text Completion (Sync & Async)

#### Sync:
```python
from qwen_chat import Qwen
from qwen_chat.core.types.chat import ChatMessage

# Initializes automatically using environment variables
client = Qwen()

messages = [
    ChatMessage(
        role="user",
        content="Tell me a joke about programming!"
    )
]

response = client.chat.create(
    messages=messages,
    model="qwen3.6-plus"
)
print("🤖 AI Response:", response.choices.message.content)
```

#### Async:
```python
import asyncio
from qwen_chat import Qwen
from qwen_chat.core.types.chat import ChatMessage

async def main():
    client = Qwen()
    messages = [ChatMessage(role="user", content="Explain quantum computing in one sentence.")]
    
    response = await client.chat.acreate(
        messages=messages,
        model="qwen3.6-plus"
    )
    print("🤖 AI Response:", response.choices.message.content)

asyncio.run(main())
```

---

### 2. SSE Streaming with Search Citations

```python
from qwen_chat import Qwen
from qwen_chat.core.types.chat import ChatMessage

client = Qwen()

messages = [
    ChatMessage(
        role="user",
        content="What is the latest news about Space Devs?",
        web_search=True  # Enables real-time web search citations
    )
]

stream = client.chat.create(
    messages=messages,
    model="qwen3.6-plus",
    stream=True
)

for chunk in stream:
    delta = chunk.choices[0].delta
    # Extract search citation results if present
    if delta.extra and delta.extra.web_search_info:
        print("\n🔍 Web Search Sources:")
        for source in delta.extra.web_search_info:
            print(f"- {source.title}: {source.url}")
        print("\n🤖 Assistant Response:")
        
    print(delta.content, end="", flush=True)
print()
```

---

### 3. Automatic Local Image Upload (Vision)

Just pass your local image path directly inside `ImageBlock`. The client automatically handles the secure upload sequence:

```python
from qwen_chat import Qwen
from qwen_chat.core.types.chat import ChatMessage, TextBlock, ImageBlock

client = Qwen()

messages = [
    ChatMessage(
        role="user",
        blocks=[
            TextBlock(text="Extract all the text inside this image:"),
            ImageBlock(path="receipt.jpg")  # Automatically uploaded to Alibaba OSS!
        ]
    )
]

response = client.chat.create(
    messages=messages,
    model="qwen3.6-plus"
)
print("🤖 AI Response:", response.choices.message.content)
```

---

## 🙋‍♂️ Contributing

Contributions are welcome! Please feel free to open Issues or submit Pull Requests to help improve the library.

## 📃 License

This project is licensed under the MIT License.

---

### 📞 Contact & Support

For queries, support, or custom integrations, feel free to contact the author:
* **Telegram**: [@liskiss](https://t.me/liskiss)
