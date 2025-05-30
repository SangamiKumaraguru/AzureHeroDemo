from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample flashcards data
flashcards = [
    {"question": "What is the capital of France?", "answer": "Paris"},
    {"question": "What is 2 + 2?", "answer": "4"},
    {"question": "What is the largest planet?", "answer": "Jupiter"}
]

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

if __name__ == '__main__':
    app.run(debug=True)
