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

## 🧠 How the Code Works (Line-by-Line Explanation)

### 1. The Backend (`app.py`)
This file handles the local server, file saving, and the AI brain.

* **`AutoTokenizer` & `AutoModelForSeq2SeqLM`:** We bypass generic pipelines and directly load `t5-small`. The tokenizer turns English words into numbers (tokens) the AI can understand, and the model does the actual thinking.
* **`generate_ai_gist(text)` Function:** 
  * *Regex Cleaning:* Uses `re.sub` to strip timestamps (e.g., `[10:30 AM]`) out of the text so the AI doesn't get confused by numbers.
  * *Prompt Formatting:* Prepends `"summarize: "` to the text, which is a strict requirement for the T5 model to know what task to perform.
  * *Generation:* Uses `model.generate()` to create the summary. We use `num_beams=4` (to give the AI 4 different "paths" of thought to find the best summary) and `early_stopping=True`.
* **API Routes (`@app.route`)**:
  * `/api/sessions/start`: Generates a timestamped `.txt` file in the `sessions_db` folder.
  * `/api/sessions/<filename>` (PUT): Receives the real-time text from the frontend and appends (`mode='a'`) or overwrites (`mode='w'`) the local text file.

### 2. The Frontend (`templates/index.html`)
This file contains the UI, the microphone logic, and the connection to the backend.

* **CSS / Glassmorphism:** Uses CSS variables (`:root`) to define a clean green/white color palette. `backdrop-filter: blur(20px)` is used on the bottom control bar to give it a modern, frosted-glass effect.
* **Web Speech API (`SpeechRecognition`)**:
  * `recognition.continuous = true`: Prevents the microphone from turning off after you pause speaking.
  * `recognition.interimResults = true`: **Crucial for real-time typing.** This tells the browser to send "guesses" of what you are saying before you finish the sentence.
* **The `onresult` Event Loop**:
  * It splits results into two categories: `isFinal` (sentence is finished) and `interimTranscript` (live speaking).
  * `interimTranscript` words are instantly injected into the `<textarea>` so the user sees zero lag.
  * When `isFinal` triggers, the code attaches a timestamp (e.g., `[12:00 PM]`), locks the text into `savedContentBeforeLive`, and immediately makes a `fetch()` PUT request to save that specific sentence to the backend database.

---

## 🔒 Privacy Notice

This application is built with absolute privacy in mind. Voice transcription relies on your browser's native API, AI summarization is handled locally on your machine, and your `.txt` files are saved strictly to your hard drive. **No data is sent to external cloud processing servers.**

---

## 📝 License

This project is open-source and available under the [MIT License](https://choosealicense.com/licenses/mit/).
