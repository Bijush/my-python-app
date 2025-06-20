from flask import Flask, render_template, request, redirect, url_for
from questions import questions

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", total=len(questions))

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if request.method == "POST":
        score = 0
        for q in questions:
            selected = request.form.get(f"q{q['id']}")
            if selected == q["answer"]:
                score += 1
        return redirect(url_for("result", score=score))
    return render_template("quiz.html", questions=questions)

@app.route("/result")
def result():
    score = int(request.args.get("score", 0))
    return render_template("result.html", score=score, total=len(questions))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
