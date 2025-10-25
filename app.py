from flask import Flask, render_template, request, redirect, url_for
from collections import defaultdict
import random

app = Flask(__name__)

# Café list with descriptions
cafes = [
    {"name": "Alea Spielbar", "description": "Bright, playful space with great coffee and snacks."},
    {"name": "Slurp Zürich", "description": "Minimalist café perfect for coffee lovers."},
    {"name": "NUDE Zürich", "description": "Sleek, modern, and airy coffee spot."},
    {"name": "Miro Coffee", "description": "Cozy café with a warm and welcoming vibe."},
    {"name": "Amiamo Caffè", "description": "Traditional coffee with a friendly atmosphere."},
    {"name": "Café Noir", "description": "Vintage-inspired café for a relaxing break."},
    {"name": "Cà Phê Lơ Mơ", "description": "Eclectic café with quirky details and great pastries."},
    {"name": "OKO Bar", "description": "Open, cozy spot to catch up and relax."},
    {"name": "Belmondo", "description": "Trendy café with a cheerful, lively atmosphere."},
    {"name": "Babus", "description": "Calm, welcoming café with excellent coffee."},
    {"name": "Roxy Café", "description": "Bright and vibrant café, perfect for a catch-up."},
    {"name": "Kafi Freud", "description": "Unique café with a cozy and reflective mood."},
    {"name": "Robin’s Coffee", "description": "Warm and inviting coffee shop with friendly staff."},
    {"name": "La Lere", "description": "Minimalist space with an artsy vibe, perfect for inspiration."},
    {"name": "ViCAFE", "description": "Classic coffee spot with a bustling city energy."}
]

# Store answers in memory by pair code
paired_answers = defaultdict(list)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/pair', methods=['GET', 'POST'])
def pair():
    if request.method == 'POST':
        pair_code = request.form.get('pair_code')
        # If user clicked create new, generate random code
        if request.form.get('create_new'):
            pair_code = str(random.randint(1000, 9999))
        # Make sure pair_code exists
        if pair_code not in paired_answers:
            paired_answers[pair_code] = []
        return redirect(url_for('questions', pair_code=pair_code))
    return render_template('pair.html')

@app.route('/questions/<pair_code>', methods=['GET', 'POST'])
def questions(pair_code):
    if request.method == 'POST':
        # Collect answers from form
        answers = [request.form.get('q1', ''),
                   request.form.get('q2', ''),
                   request.form.get('q3', '')]
        paired_answers[pair_code] = answers
        return redirect(url_for('result', pair_code=pair_code))
    return render_template('questions.html', pair_code=pair_code)

@app.route('/result/<pair_code>')
def result(pair_code):
    answers = paired_answers.get(pair_code, [])
    if not answers:
        return "No answers found for this pair code."

    # Simple matching logic
    cafe_scores = []
    for cafe in cafes:
        score = 0
        text_to_match = (cafe['name'] + " " + cafe['description']).lower()
        for ans in answers:
            for word in ans.lower().split():
                if word in text_to_match:
                    score += 1
        cafe_scores.append((score, cafe))

    max_score = max(score for score, _ in cafe_scores)
    top_cafes = [cafe for score, cafe in cafe_scores if score == max_score]
    chosen_cafe = random.choice(top_cafes)

    comment = f"We think you two would have a blast here based on your answers!"
    return render_template('result.html', cafe=chosen_cafe, comment=comment)

if __name__ == "__main__":
    app.run(debug=True)

