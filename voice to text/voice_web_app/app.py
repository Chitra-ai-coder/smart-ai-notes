from flask import Flask, render_template, request, jsonify
import os
import re
from datetime import datetime

# Import direct model classes instead of the pipeline shortcut
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

app = Flask(__name__)

# --- INITIALIZE REAL LOCAL AI (DIRECT LOADING) ---
print("Downloading/Loading T5-Small AI... (This takes a minute on first run)")

# Load the tokenizer (the part that reads words) and the model (the brain)
tokenizer = AutoTokenizer.from_pretrained("t5-small")
model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")

print("AI is Ready!")

DB_FOLDER = "sessions_db"
os.makedirs(DB_FOLDER, exist_ok=True)

def generate_ai_gist(text):
    # 1. Strip the timestamps so the AI doesn't get confused
    clean_text = re.sub(r'\[.*?\]\s*', '', text)
    words = clean_text.split()
    
    if len(words) < 40:
        return "Please record a bit more of the meeting before asking for a summary!"

    # 2. T5 requires the word "summarize: " at the start of the prompt
    input_text = "summarize: " + " ".join(words[-600:])
    
    try:
        # 3. Convert text to numbers (tokens)
        inputs = tokenizer(input_text, return_tensors="pt", max_length=1024, truncation=True)
        
        # 4. Generate the summary using exact parameters
        summary_ids = model.generate(
            inputs.input_ids, 
            max_length=150, 
            min_length=40, 
            length_penalty=2.0, 
            num_beams=4, 
            early_stopping=True
        )
        
        # 5. Convert numbers back to text
        gist = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        
        # Capitalize the first letter and format it nicely for your frontend modal
        formatted_gist = gist[0].upper() + gist[1:]
        return f"<b>AI Executive Summary:</b><br><br>{formatted_gist}"
        
    except Exception as e:
        return f"<b>AI Error:</b> {str(e)}"


# --- ROUTES ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/sessions', methods=['GET'])
def get_sessions():
    files = [f for f in os.listdir(DB_FOLDER) if f.endswith('.txt')]
    files.sort(reverse=True)
    return jsonify(files)

@app.route('/api/sessions/<filename>', methods=['GET'])
def read_session(filename):
    filepath = os.path.join(DB_FOLDER, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return jsonify({"content": f.read()})
    return jsonify({"error": "File not found"}), 404

@app.route('/api/sessions/start', methods=['POST'])
def start_session():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"Session_{timestamp}.txt"
    filepath = os.path.join(DB_FOLDER, filename)
    open(filepath, 'w').close()
    return jsonify({"filename": filename})

@app.route('/api/sessions/<filename>', methods=['PUT'])
def update_session(filename):
    data = request.json
    content = data.get('content', '')
    mode = data.get('mode', 'w')
    filepath = os.path.join(DB_FOLDER, filename)
    with open(filepath, mode, encoding='utf-8') as f:
        f.write(content)
    return jsonify({"status": "success"})

@app.route('/api/sessions/<filename>', methods=['DELETE'])
def delete_session(filename):
    filepath = os.path.join(DB_FOLDER, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    return jsonify({"status": "success"})

@app.route('/api/sessions/<filename>/rename', methods=['POST'])
def rename_session(filename):
    new_name = request.json.get('new_name')
    if not new_name.endswith('.txt'):
        new_name += '.txt'
    old_path = os.path.join(DB_FOLDER, filename)
    new_path = os.path.join(DB_FOLDER, new_name)
    if os.path.exists(old_path):
        os.rename(old_path, new_path)
        return jsonify({"new_filename": new_name})
    return jsonify({"error": "File not found"}), 404

@app.route('/api/sessions/<filename>/summarize', methods=['GET'])
def summarize_session(filename):
    filepath = os.path.join(DB_FOLDER, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
            summary = generate_ai_gist(text)
            return jsonify({"summary": summary})
    return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)