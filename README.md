# qwen-chat 🚀

[![PyPI version](https://img.shields.io/pypi/v/qwen-chat.svg)](https://pypi.org/project/qwen-chat/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)

An unofficial, feature-rich Python SDK and client wrapper for the [Qwen AI](https://chat.qwen.ai) Web API. Enjoy seamless access to advanced models like `qwen3.6-plus` with support for streaming, multi-turn conversations, system prompts, web search, deep reasoning, automatic local image uploads, and LlamaIndex integration.

---

## ✨ Features

- **🧠 Complete Model Support**  
  Interact with Qwen's latest web models including `qwen3.6-plus`, `qwen-max-latest`, `qwq-32b`, `qwen2.5-omni-7b`, and specialized vision/coder versions.
  
- **💬 Multi-turn Chat Sessions**  
  Have back-and-forth conversations that maintain context across messages — just like chatting in the Qwen web UI. Build interactive terminal chatbots or conversational agents easily.

- **⚡ Synchronous & Asynchronous Clients**  
  Whether you're building a script or a highly concurrent async web server, `qwen-chat` has you covered with native `create()` and `acreate()` workflows.

- **🌊 Real-time SSE Streaming (On/Off)**  
  Toggle `stream=True` or `stream=False` per request. Stream token-by-token responses directly to your UI or console, or get the full response at once.

- **🎭 System & Assistant Roles**  
  Use `system` role messages to define the AI's personality, behavior, and instructions. Chain `assistant` and `user` roles for few-shot prompting and context injection.

- **📸 Automatic Local Image Uploads**  
  Pass a local file path or raw bytes to an `ImageBlock`. The client automatically fetches STS tokens and uploads the image to Alibaba Cloud OSS under the hood — no boilerplate required!

- **🔍 Integrated Web Search**  
  Toggle real-time search on or off per message to query live web data and receive detailed citations alongside responses.

- **💡 Thinking & Reasoning Controls**  
  Adjust thinking budget settings to enable advanced reasoning capabilities on complex tasks.

- **🦙 LlamaIndex Adapter**  
  Use Qwen directly inside LlamaIndex with `QwenLlamaIndex` from the same `qwen_chat` package. No separate `qwen-api` or `qwen-llamaindex` package is required.

---

## 📦 Installation

Install `qwen-chat` via pip:

```bash
pip install qwen-chat
```

---

## ⚙️ Environment Setup

To authenticate requests, extract your `Authorization` bearer token from the [Qwen Web UI](https://chat.qwen.ai):

1. Go to [https://chat.qwen.ai](https://chat.qwen.ai) and log in.
2. Open developer tools (`F12` or `Ctrl+Shift+I` / `Cmd+Option+I`) and navigate to the **Network** tab.
3. Send any message in the chat interface.
4. Locate the `completions` request (filter by Fetch/XHR).
5. Click on the request and go to the Headers tab. Copy the value of the `Authorization` header **without the word "Bearer "** (just copy the token starting with `eyJ...`).
6. Save this value in a `.env` file in the root of your project:

```env
QWEN_AUTH_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

> **Note:** You do **not** need to set up cookies. The package handles cookies automatically.

---

## 🚀 Usage Examples

### 1. Basic Text Completion

The simplest way to get a response from Qwen:

```python
from qwen_chat import Qwen
from qwen_chat.core.types.chat import ChatMessage

client = Qwen()

messages = [
    ChatMessage(role="user", content="What is Python?")
]

response = client.chat.create(messages=messages, model="qwen3.6-plus")
print("🤖", response.choices.message.content)
```

---

### LlamaIndex Usage

Use Qwen as a LlamaIndex LLM from the same `qwen-chat` package:

```python
from qwen_chat import QwenLlamaIndex

llm = QwenLlamaIndex(model="qwen3.6-plus")

response = llm.complete("Reply with only: ok")
print(response.text)
```

Chat example:

```python
from llama_index.core.base.llms.types import ChatMessage
from qwen_chat import QwenLlamaIndex

llm = QwenLlamaIndex(model="qwen3.6-plus")

response = llm.chat([
    ChatMessage(role="user", content="What is LlamaIndex?")
])

print(response.message.content)
```

Streaming example:

```python
from qwen_chat import QwenLlamaIndex

llm = QwenLlamaIndex(model="qwen3.6-plus")

for chunk in llm.stream_complete("Write one sentence about Python."):
    print(chunk.delta, end="", flush=True)
```

---

### 2. Streaming On / Off

#### Stream OFF (get full response at once):
```python
from qwen_chat import Qwen
from qwen_chat.core.types.chat import ChatMessage

client = Qwen()
messages = [ChatMessage(role="user", content="Tell me a short joke.")]

# stream=False (default) — returns complete response
response = client.chat.create(messages=messages, model="qwen3.6-plus", stream=False)
print("🤖", response.choices.message.content)
```

#### Stream ON (token-by-token output):
```python
from qwen_chat import Qwen
from qwen_chat.core.types.chat import ChatMessage

client = Qwen()
messages = [ChatMessage(role="user", content="Write a poem about the ocean.")]

# stream=True — yields chunks in real-time
stream = client.chat.create(messages=messages, model="qwen3.6-plus", stream=True)

print("🤖 ", end="")
for chunk in stream:
    print(chunk.choices[0].delta.content, end="", flush=True)
print()
```

---

### 3. System Role & Assistant Role (Custom Personality)

Use the `system` role to define how the AI behaves. Use `assistant` role for few-shot examples:

```python
from qwen_chat import Qwen
from qwen_chat.core.types.chat import ChatMessage

client = Qwen()

messages = [
    # System prompt — defines AI personality and behavior
    ChatMessage(
        role="system",
        content="You are a friendly pirate captain. Always respond in pirate speak with lots of 'Arrr!' and nautical references."
    ),
    # User message
    ChatMessage(
        role="user",
        content="What's the weather like today?"
    )
]

response = client.chat.create(messages=messages, model="qwen3.6-plus")
print("🏴‍☠️", response.choices.message.content)
```

#### Few-shot prompting with assistant role:
```python
from qwen_chat import Qwen
from qwen_chat.core.types.chat import ChatMessage

client = Qwen()

messages = [
    ChatMessage(role="system", content="You are a helpful translator. Translate English to Bengali."),
    # Few-shot example
    ChatMessage(role="user", content="Hello"),
    ChatMessage(role="assistant", content="হ্যালো"),
    ChatMessage(role="user", content="How are you?"),
    ChatMessage(role="assistant", content="আপনি কেমন আছেন?"),
    # Actual request
    ChatMessage(role="user", content="I love programming")
]

response = client.chat.create(messages=messages, model="qwen3.6-plus")
print("🤖", response.choices.message.content)
```

---

### 4. Interactive Terminal Chat (Multi-turn Conversation)

Build a fully interactive terminal chatbot that maintains conversation context across multiple turns — just like the Qwen web UI.

> **How it works:** The Qwen API remembers your conversation server-side via `chat_id` and `parent_id`. You only need to send the **new message** each turn — the AI already knows the full conversation history.

```python
from qwen_chat import Qwen
from qwen_chat.core.types.chat import ChatMessage

def main():
    client = Qwen()
    print("💬 Qwen Chat Terminal")
    print("Type 'exit' to quit\n")

    # Optional: send a system prompt as the very first message
    system_msg = [
        ChatMessage(
            role="system",
            content="You are a helpful and friendly AI assistant."
        )
    ]
    client.chat.create(messages=system_msg, model="qwen3.6-plus")

    while True:
        try:
            user_input = input("🧑 You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye! 👋")
            break

        if not user_input or user_input.lower() == "exit":
            print("Bye! 👋")
            break

        # Send only the new user message — the API remembers the conversation
        messages = [ChatMessage(role="user", content=user_input)]

        response = client.chat.create(
            messages=messages,
            model="qwen3.6-plus",
            temperature=0.7
        )

        print(f"🤖 AI: {response.choices.message.content}\n")

if __name__ == "__main__":
    main()
```

#### Interactive chat with streaming output:
```python
from qwen_chat import Qwen
from qwen_chat.core.types.chat import ChatMessage

def main():
    client = Qwen()
    print("💬 Qwen Streaming Chat")
    print("Type 'exit' to quit\n")

    while True:
        try:
            user_input = input("🧑 You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye! 👋")
            break

        if not user_input or user_input.lower() == "exit":
            print("Bye! 👋")
            break

        # Send only the new message each turn
        messages = [ChatMessage(role="user", content=user_input)]

        stream = client.chat.create(
            messages=messages,
            model="qwen3.6-plus",
            stream=True
        )

        print("🤖 AI: ", end="")
        for chunk in stream:
            text = chunk.choices[0].delta.content
            print(text, end="", flush=True)
        print("\n")

if __name__ == "__main__":
    main()
```

---

### 5. Web Search with Citations

```python
from qwen_chat import Qwen
from qwen_chat.core.types.chat import ChatMessage

client = Qwen()

messages = [
    ChatMessage(
        role="user",
        content="What are the latest developments in AI?",
        web_search=True
    )
]

stream = client.chat.create(messages=messages, model="qwen3.6-plus", stream=True)

for chunk in stream:
    delta = chunk.choices[0].delta
    if delta.extra and delta.extra.web_search_info:
        print("\n🔍 Sources:")
        for source in delta.extra.web_search_info:
            print(f"  • {source.title}: {source.url}")
        print()
    print(delta.content, end="", flush=True)
print()
```

---

### 6. Automatic Local Image Upload (Vision)

Just pass your local image path directly inside `ImageBlock`. The client handles the secure upload automatically:

```python
from qwen_chat import Qwen
from qwen_chat.core.types.chat import ChatMessage, TextBlock, ImageBlock

client = Qwen()

messages = [
    ChatMessage(
        role="user",
        blocks=[
            TextBlock(text="What's in this image? Describe it in detail."),
            ImageBlock(path="photo.jpg")  # Auto-uploaded to Alibaba OSS!
        ]
    )
]

response = client.chat.create(messages=messages, model="qwen3.6-plus")
print("🤖", response.choices.message.content)
```

---

### 7. Async Usage

```python
import asyncio
from qwen_chat import Qwen
from qwen_chat.core.types.chat import ChatMessage

async def main():
    client = Qwen()
    messages = [ChatMessage(role="user", content="Explain quantum computing in one sentence.")]
    
    response = await client.chat.acreate(messages=messages, model="qwen3.6-plus")
    print("🤖", response.choices.message.content)

asyncio.run(main())
```

---

### 8. Thinking & Reasoning Mode

Enable deep thinking for complex tasks:

```python
from qwen_chat import Qwen
from qwen_chat.core.types.chat import ChatMessage

client = Qwen()

messages = [
    ChatMessage(
        role="user",
        content="Solve this step by step: If a train travels 120km in 2 hours, then stops for 30 minutes, then travels 90km in 1.5 hours, what is the average speed for the entire journey?",
        thinking=True,
        thinking_budget=4096
    )
]

response = client.chat.create(messages=messages, model="qwen3.6-plus")
print("🤖", response.choices.message.content)
```

---

## 🙋‍♂️ Contributing

Contributions are welcome! Here's how:

1. Fork the project
2. Create your feature branch (`git checkout -b feature/awesome-feature`)
3. Commit your changes (`git commit -m 'Add awesome feature'`)
4. Push to the branch (`git push origin feature/awesome-feature`)
5. Open a Pull Request

---

## 📃 License

This project is licensed under the [MIT License](LICENSE).

---

### 📞 Contact & Support

<a href="https://t.me/liskiss"><img src="https://img.shields.io/badge/Telegram-@liskiss-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram" /></a>

For queries, support, or custom integrations, feel free to reach out!

---

<p align="center">Made with ❤️ by <b>Shahadat Hassan</b></p>
