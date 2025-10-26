from flask import Flask, render_template, request, redirect, url_for
import random
import string

app = Flask(__name__)

# ---- Questions ----
LIGHT_ROAST_QUESTIONS = [
    # 12 questions
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
]

DARK_ROAST_QUESTIONS = [
    # 30 questions (full list you gave)
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
    "After a long day, what helps you relax?",
    "What small object brings you comfort?",
    "Describe your dream workspace or creative corner.",
    "Which season makes you happiest, and why?",
    "If you could spend a day learning something new, what would it be?",
    "Describe a memory that always makes you smile."
]

# ---- Cafés ----
CAFES = [
    {"name": "ViCAFE Hohlstrasse 418", "desc": "A space alive and welcoming at any time, where the smell of fresh coffee energizes the senses.", "category": ["Playful / Lively"]},
    {"name": "La Lere", "desc": "Sunlight fills a clean, minimalist space with carefully arranged details.", "category": ["Minimalist / Calm", "Creative / Artsy"]},
    {"name": "MAME Coffee", "desc": "High ceilings and open spaces bring a sense of calm and modern style.", "category": ["Minimalist / Calm"]},
    {"name": "Robin’s Coffee", "desc": "Soft lighting, comfortable chairs, and a gentle buzz in the background make this café instantly relaxing.", "category": ["Cozy / Warm", "Minimalist / Calm"]},
    {"name": "Kafi Freud", "desc": "Colorful details, comfortable corners, and the smell of fresh pastries create a cheerful, easygoing vibe.", "category": ["Cozy / Warm", "Playful / Lively"]},
    {"name": "Irma Zürich", "desc": "Polished design and a calm atmosphere give this café a modern edge.", "category": ["Chic / Stylish"]},
    {"name": "Roxy Café", "desc": "Vintage vibes and quirky details transport you back in time.", "category": ["Creative / Artsy", "Playful / Lively"]},
    {"name": "Babus", "desc": "Modern, bright, and welcoming, with a comfortable atmosphere.", "category": ["Cozy / Warm"]},
    {"name": "Café Europa", "desc": "Bright, colorful, and full of energy.", "category": ["Playful / Lively", "Cozy / Warm"]},
    {"name": "Belmondo", "desc": "Elegant interiors, lush greenery, and subtle tropical touches create a stylish, inviting space.", "category": ["Chic / Stylish"]},
    {"name": "OKO Bar", "desc": "Warm wood tones, soft lighting, and natural materials create a calming, eco-friendly space.", "category": ["Eco-conscious / Natural", "Cozy / Warm"]},
    {"name": "Cà Phê Lơ Mơ", "desc": "Bold colors and playful décor create an energetic, inspiring space.", "category": ["Creative / Artsy", "Playful / Lively"]},
    {"name": "Café Noir", "desc": "Warm, intimate, and open, perfect for catching up over coffee.", "category": ["Chic / Stylish", "Cozy / Warm"]},
    {"name": "Draft Coffee", "desc": "Industrial-chic interiors and exposed elements create a clean, modern space.", "category": ["Minimalist / Calm", "Chic / Stylish"]},
    {"name": "Amiamo Caffè", "desc": "Rustic charm, warm colors, and the aroma of Italian espresso fill this small, inviting space.", "category": ["Cozy / Warm", "Chic / Stylish"]},
    {"name": "Miro Coffee", "desc": "Bright, modern, and welcoming, with greenery adding a relaxed touch.", "category": ["Minimalist / Calm"]},
    {"name": "NUDE Zürich", "desc": "Soft lighting, calm spaces, and clean design create a serene retreat.", "category": ["Minimalist / Calm"]},
    {"name": "Slurp Zürich", "desc": "Clean, bright, and welcoming, with a warm, friendly atmosphere.", "category": ["Playful / Lively", "Cozy / Warm"]},
    {"name": "Alea Spielbar", "desc": "Bright, social, and buzzing with energy.", "category": ["Interactive / Social", "Playful / Lively"]},
]

# ---- Pair storage ----
pairs = {}

# ---- Routes ----
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/pair", methods=["POST"])
def pair():
    pair_code = request.form.get("pair_code") or "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    if pair_code not in pairs:
        pairs[pair_code] = {"answers": {}, "ready": set(), "quiz_length": None}
    return redirect(url_for("pair_created", pair_code=pair_code))

@app.route("/pair_created/<pair_code>")
def pair_created(pair_code):
    return render_template("pair_created.html", pair_code=pair_code)

@app.route("/start_quiz/<pair_code>/<quiz_type>")
def start_quiz(pair_code, quiz_type):
    if quiz_type == "light":
        questions = LIGHT_ROAST_QUESTIONS
    else:
        questions = DARK_ROAST_QUESTIONS
    pairs[pair_code]["quiz_length"] = len(questions)
    return redirect(url_for("questions", pair_code=pair_code, qnum=1))

@app.route("/questions/<pair_code>/<int:qnum>", methods=["GET", "POST"])
def questions(pair_code, qnum):
    quiz_length = pairs[pair_code]["quiz_length"]
    if request.method == "POST":
        answer = request.form.get("answer")
        pairs[pair_code]["answers"][qnum] = answer
        return redirect(url_for("questions", pair_code=pair_code, qnum=qnum+1))
    if qnum > quiz_length:
        return redirect(url_for("submitted_wait", pair_code=pair_code))
    questions_list = LIGHT_ROAST_QUESTIONS if quiz_length == 12 else DARK_ROAST_QUESTIONS
    return render_template("questions.html", question=questions_list[qnum-1], qnum=qnum, total=quiz_length, pair_code=pair_code)

@app.route("/submitted_wait/<pair_code>")
def submitted_wait(pair_code):
    # Check if both users finished
    if len(pairs[pair_code]["ready"]) < 2:
        return render_template("submitted_wait.html", pair_code=pair_code)
    else:
        return redirect(url_for("result", pair_code=pair_code))

@app.route("/finish/<pair_code>")
def finish(pair_code):
    # User signals they are done
    user = request.args.get("user")
    pairs[pair_code]["ready"].add(user)
    if len(pairs[pair_code]["ready"]) < 2:
        return redirect(url_for("submitted_wait", pair_code=pair_code))
    else:
        return redirect(url_for("result", pair_code=pair_code))

@app.route("/result/<pair_code>")
def result(pair_code):
    # Basic matching logic for demo
    cafe = random.choice(CAFES)
    backups = random.sample([c for c in CAFES if c != cafe], 2)
    return render_template("result.html", main=cafe, backups=backups)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


