# 🎙️ smart ai notes

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.12-green.svg)
![AI](https://img.shields.io/badge/Local%20AI-T5--Small-orange.svg)

**smart ai notes** is a lightweight, 100% private, AI-powered voice-to-text meeting assistant. It allows you to dictate notes in real-time and generate "Smart Gists" (executive summaries) using a local, offline AI model. Your sensitive meeting data never leaves your computer.

---

## ✨ Key Features

* **Real-Time Dictation:** Watch words appear on the screen exactly as you speak them using `interimResults` for zero-lag typing.
* **100% Private & Offline AI:** Uses the `t5-small` Hugging Face model (~240MB) running entirely on your local CPU. No API keys, no cloud servers.
* **Smart Gist Summarization:** Instantly condense long meeting transcripts into clean, readable executive summaries.
* **Session Management:** Seamlessly start, auto-save, rename, and delete meeting sessions from a sleek sidebar.
* **Distraction-Free UI:** A beautiful, responsive glassmorphism interface built with Vanilla JS, HTML, and CSS.

---

## 📂 File Structure

Here is how the project files are organized:

```text
smart-ai-notes/
│
├── app.py                 # The Python/Flask backend and AI engine
├── templates/
│   └── index.html         # The Frontend UI (HTML, CSS, JS)
│
├── sessions_db/           # Folder where your .txt notes are saved
├── .venv/                 # Python virtual environment
└── README.md              # This documentation file
```

---

## 🚀 Installation & Setup

Because this app is designed to be highly optimized, we use the CPU-only version of PyTorch to save gigabytes of storage space.

### 1. Clone the repository
```bash
git clone https://github.com/YOUR-USERNAME/smart-ai-notes.git
cd smart-ai-notes
```

### 2. Create a Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

### 3. Install the Dependencies
Install the CPU-only PyTorch engine, Flask, and the Hugging Face AI libraries:
```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install Flask transformers sentencepiece protobuf
```

---

## 💻 How to Run the App

1. **Start the local server:**
   ```bash
   python app.py
   ```
   *(Note: On the very first run, it will take a minute or two to download the 240MB `t5-small` AI model to your local cache. After that, it starts instantly!)*

2. **Open your web browser:**
   Navigate to `[http://127.0.0.1:5000](http://127.0.0.1:5000)`

3. **Start Note-Taking:**
   Click **Launch Workspace**, start a **New Session**, and click **🎙️ Record Audio** to begin transcribing. When you are done, click **✨ Smart Gist** to generate your AI summary!

---

## 🧠 How the Code Works (Step-by-Step Flow)

The application works in three main chronological steps: listening to your voice, saving the text, and summarizing the meeting.

### Step 1: Taking Voice Input (Frontend - `index.html`)
The application does not use heavy Python audio libraries to listen to your microphone. Instead, it uses the browser's built-in **Web Speech API** for maximum efficiency.
* `recognition.continuous = true`: Keeps the microphone listening even if you pause speaking.
* `recognition.interimResults = true`: This is the secret to **zero-lag real-time typing**. It tells the browser to display "guesses" of what you are saying before you even finish the sentence, injecting them instantly into the `<textarea>`.
* **The Handoff:** Once a sentence is finalized by the API (`isFinal`), the JavaScript attaches a timestamp (e.g., `[12:00 PM]`) and uses `fetch()` to send that sentence directly to the Python backend.

### Step 2: Saving the Text (Backend - `app.py`)
Python (Flask) acts as the secure vault for your data. 
* **The API Route:** When the JavaScript sends the finalized sentence, it hits the `@app.route('/api/sessions/<filename>', methods=['PUT'])` endpoint.
* **File Writing:** Python opens the specific `.txt` file inside the `sessions_db/` folder and appends (`mode='a'`) the new sentence to it. This ensures your data is saved securely to your local hard drive paragraph by paragraph, preventing data loss if you accidentally close the browser.

### Step 3: AI Summarization (Backend - `app.py`)
When you click "Smart Gist", Python wakes up the local AI to process your saved text.
* **Loading the Brain:** At the top of `app.py`, `AutoTokenizer` and `AutoModelForSeq2SeqLM` bypass generic pipelines to directly load the `t5-small` model into your computer's memory.
* **Cleaning the Data:** Inside `generate_ai_gist(text)`, Python uses Regex (`re.sub`) to strip the timestamps out of your document so the AI doesn't get confused by numbers.
* **The Prompt:** Python prepends `"summarize: "` to the text, which is a strict requirement for the T5 model to know what task to perform.
* **Generation:** `model.generate()` is called with `num_beams=4`. This forces the AI to explore 4 different logical "paths" of thought simultaneously to find the absolute best executive summary. It then sends this summary back to the frontend to be displayed in a modal!

---

## 🔒 Privacy Notice

This application is built with absolute privacy in mind. Voice transcription relies on your browser's native API, AI summarization is handled locally on your machine, and your `.txt` files are saved strictly to your hard drive. **No data is sent to external cloud processing servers.**

---

## 📝 License

This project is open-source and available under the [MIT License](https://choosealicense.com/licenses/mit/).
