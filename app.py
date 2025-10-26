from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = "coffee_secret_key"

# In-memory storage for simplicity
pairs = {}
questions_short = [
    "What is your go-to morning beverage?",
    "How do you feel about strong flavors?",
    "Do you enjoy a bit of bitterness?",
    "Do you prefer fruity or nutty aromas?",
    "How do you take your coffee?",
    "When do you usually drink coffee?",
    "What do you pair coffee with?",
    "How adventurous are you with new flavors?",
    "Do you enjoy coffee with milk or black?",
    "How important is caffeine to you?",
    "What’s your ideal coffee experience?",
    "Do you prefer warm or cold coffee?"
]

questions_long = questions_short + [
    "What texture do you like in a drink?",
    "How often do you drink coffee?",
    "Do you enjoy sweet drinks?",
    "Do you prefer a classic or modern taste?",
    "Would you describe yourself as patient?",
    "Do you enjoy slow mornings?",
    "What mood do you want your coffee to match?",
    "Do you drink coffee socially or alone?",
    "What’s your favorite dessert flavor?",
    "Do you like surprises?",
    "How do you handle bitterness?",
    "How do you brew coffee at home?",
    "Do you like strong aroma?",
    "Do you drink coffee daily?",
    "What’s your favorite café vibe?",
    "Do you enjoy experimenting with coffee flavors?",
    "Do you prefer hot or iced drinks?",
    "How much sugar do you use in coffee?",
    "Describe your ideal coffee break in one word."
]

coffees = [
    "Espresso", "Latte", "Cappuccino", "Americano",
    "Flat White", "Macchiato", "Cold Brew", "Mocha",
    "Ristretto", "Affogato"
]

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/create_pair", methods=["POST"])
def create_pair():
    pair_code = str(random.randint(1000, 9999))
    pairs[pair_code] = {"users": [], "answers": {}}
    return render_template("pair_created.html", pair_code=pair_code)


@app.route("/join_pair", methods=["POST"])
def join_pair():
    code = request.form.get("pair_code", "").strip()
    if not code:
        return render_template("index.html", error="Please enter a code to join.")
    if code not in pairs:
        return render_template("index.html", error="Invalid code. Please try again.")
    if len(pairs[code]["users"]) >= 2:
        return render_template("index.html", error="This pair is already full.")
    session["pair_code"] = code
    pairs[code]["users"].append(f"user{len(pairs[code]['users']) + 1}")
    return redirect(url_for("choose_quiz"))


@app.route("/choose_quiz")
def choose_quiz():
    return render_template("pair_created.html", pair_code=session["pair_code"], joined=True)


@app.route("/start_quiz/<version>")
def start_quiz(version):
    code = session.get("pair_code")
    if not code:
        return redirect(url_for("index"))
    questions = questions_short if version == "short" else questions_long
    session["questions"] = questions
    session["version"] = version
    return render_template("questions.html", questions=questions, total=len(questions), pair_code=code)


@app.route("/submit", methods=["POST"])
def submit():
    code = session.get("pair_code")
    if not code or code not in pairs:
        return redirect(url_for("index"))

    answers = [request.form.get(f"answer_{i}") for i in range(len(session["questions"]))]
    user = f"user{len(pairs[code]['answers']) + 1}"
    pairs[code]["answers"][user] = answers

    # Wait for the other user
    if len(pairs[code]["answers"]) < 2:
        return render_template("submitted_wait.html")

    # Analyze compatibility
    user1_answers = pairs[code]["answers"]["user1"]
    user2_answers = pairs[code]["answers"]["user2"]

    compatibility = sum(1 for a, b in zip(user1_answers, user2_answers) if a == b)
    main_coffee = random.choice(coffees)
    backups = random.sample([c for c in coffees if c != main_coffee], 2)

    return render_template("result.html", main_coffee=main_coffee, backups=backups, score=compatibility)


if __name__ == "__main__":
    app.run(debug=True)

