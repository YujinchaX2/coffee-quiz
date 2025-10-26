from flask import Flask, render_template, request, redirect, url_for, session
import random
import string

app = Flask(__name__)
app.secret_key = "coffeechemistrysecret"

# --- Sample Questions ---
LONG_QUESTIONS = [
    "If you could wake up in any country tomorrow, where would it be — and what’s the first thing you’d do?",
    "Describe your perfect Sunday — how would you spend it?",
    "If you could have any animal as a pet (real or fantasy), what would you choose?",
    "What’s a weird or unexpected food combo you secretly enjoy?",
    "What song instantly puts you in a good mood?",
    "What superpower would you love to have for just one day?",
    "You have the whole day free — do you plan something or just see where it takes you?",
    "What’s something small that never fails to make you smile?",
    "If someone challenged you to a spontaneous adventure, how would you respond?",
    "You’re traveling somewhere new — what’s the first thing you look for when you arrive?",
    "What’s your go-to drink when you want to treat yourself?",
    "If you could teleport anywhere right now for one hour, where would you go?",
    "When you need to clear your head, what’s your favorite kind of place to be?",
    "If you could live in any time period or era, which would you pick — and why?",
    "What’s something creative you’ve always wanted to try (or already do)?",
    "What’s one thing that instantly makes a place feel cozy to you?",
    "Would you rather spend an evening with good music and conversation, or explore somewhere new and lively?",
    "If we could share one meal together — no rules, no limits — what would it be?",
    "What’s one thing people might be surprised to learn about you?",
    "When you picture your ideal morning, what’s in it?",
    "If you could design your own café, what would it be like?",
    "What’s your favorite way to connect with someone — deep talks, laughter, shared silence, or something else?",
    "What’s a simple moment that always feels special to you?",
    "If your life had a theme song that played when you walked into a room, what would it be?",
    "After a long day, what helps you relax?"
]

SHORT_QUESTIONS = LONG_QUESTIONS[:12]

# --- Sample café data ---
CAFES = [
    {"name": "ViCAFE Hohlstrasse 418", "desc": "Modern / Energetic — Alive and welcoming, perfect to start your day with a buzz."},
    {"name": "La Lere", "desc": "Artsy / Minimalist — Calm sunlight and inspiring simplicity."},
    {"name": "MAME Coffee", "desc": "Trendy / Spacious — Bright, open, and expertly brewed coffee."},
    {"name": "Robin’s Coffee", "desc": "Cozy / Warm — Soft lighting, relaxing, and welcoming."},
    {"name": "Kafi Freud", "desc": "Charming / Relaxed — Colorful, cheerful, and easygoing."},
    {"name": "Irma Zürich", "desc": "Sleek / Contemporary — Polished and modern with a calm vibe."},
    {"name": "Belmondo", "desc": "Chic / Stylish — Elegant, lush, and indulgent."},
    {"name": "OKO Bar", "desc": "Eco-conscious / Relaxed — Natural materials and cozy calm."},
    {"name": "Cà Phê Lơ Mơ", "desc": "Creative / Vibrant — Bold, colorful, and full of energy."},
    {"name": "Amiamo Caffè", "desc": "Italian / Cozy — Warm, rustic, and inviting."}
]

# --- Store pairs and answers ---
PAIRS = {}
ANSWERS = {}

def generate_pair_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'join' in request.form:
            code = request.form.get('pair_code', '').strip().upper()
            if not code or code not in PAIRS:
                return render_template('index.html', error="☕ Please enter a valid pair code to join.")
            session['pair_code'] = code
            return redirect(url_for('start_quiz'))
        elif 'create' in request.form:
            code = generate_pair_code()
            PAIRS[code] = []
            session['pair_code'] = code
            return render_template('index.html', pair_created=code)
    return render_template('index.html')


@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    quiz_type = request.form.get('quiz_type')
    if quiz_type == 'light':
        session['questions'] = SHORT_QUESTIONS
    else:
        session['questions'] = LONG_QUESTIONS
    return redirect(url_for('questions'))


@app.route('/questions', methods=['GET', 'POST'])
def questions():
    pair_code = session.get('pair_code')
    if not pair_code:
        return redirect(url_for('index'))

    questions_list = session.get('questions', SHORT_QUESTIONS)
    total = len(questions_list)

    if request.method == 'POST':
        answers = [request.form.get(f'q{i}', '') for i in range(total)]
        ANSWERS[pair_code] = ANSWERS.get(pair_code, []) + [answers]
        if len(ANSWERS[pair_code]) < 2:
            return render_template('submitted_wait.html')
        else:
            return redirect(url_for('result', pair_code=pair_code))

    return render_template('questions.html', questions=questions_list, total=total, pair_code=pair_code)


@app.route('/result/<pair_code>')
def result(pair_code):
    both_answers = ANSWERS.get(pair_code, [])
    if len(both_answers) < 2:
        return render_template('submitted_wait.html')

    cafe = random.choice(CAFES)
    backups = random.sample([c for c in CAFES if c != cafe], 2)
    return render_template('result.html', cafe=cafe, backups=backups, pair_code=pair_code)


if __name__ == '__main__':
    app.run(debug=True)
