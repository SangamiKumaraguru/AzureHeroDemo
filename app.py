from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
import requests

app = Flask(__name__)

# Sample flashcards data
flashcards = [
    {"question": "What is the capital of France?", "answer": "Paris"},
    {"question": "What is 2 + 2?", "answer": "4"},
    {"question": "What is the largest planet?", "answer": "Jupiter"}
]

API_KEY = "QwErTy12345!@#zXcVbN09876$%^"  # Hardcoded random secret key for demo

@app.route('/')
def index():
    return render_template('index.html', flashcards=flashcards)

@app.route('/add', methods=['POST'])
def add_flashcard():
    question = request.form.get('question')
    answer = request.form.get('answer')
    if question and answer:
        flashcards.append({"question": question, "answer": answer})
    return redirect(url_for('index'))

@app.route('/delete/<int:card_id>', methods=['POST'])
def delete_flashcard(card_id):
    if 0 <= card_id < len(flashcards):
        flashcards.pop(card_id)
    return redirect(url_for('index'))

@app.route('/fetch_trivia', methods=['POST'])
def fetch_trivia():
    key = request.headers.get('X-API-KEY')
    if key != API_KEY:
        abort(401, description="Invalid API key.")
    # Fetch a trivia question from Open Trivia DB
    resp = requests.get('https://opentdb.com/api.php?amount=1&type=multiple')
    if resp.status_code == 200:
        data = resp.json()
        if data['results']:
            q = data['results'][0]['question']
            a = data['results'][0]['correct_answer']
            flashcards.append({"question": q, "answer": a})
            return jsonify({"message": "Flashcard added.", "question": q, "answer": a}), 201
        else:
            return jsonify({"error": "No trivia found."}), 404
    else:
        return jsonify({"error": "Failed to fetch trivia."}), 500

if __name__ == '__main__':
    app.run(debug=True)
