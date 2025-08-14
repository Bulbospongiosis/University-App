from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/form/question1", methods=['GET', 'POST'])
def form():
    return render_template("form.html")

@app.route("/form/question2", methods=['GET', 'POST'])
def form():
    return render_template("form2.html")

@app.route("/form/question3", methods=['GET', 'POST'])
def form():
    return render_template("form3.html")

@app.route("/form/question4", methods=['GET', 'POST'])
def form():
    return render_template("form4.html")


if __name__ == '__main__':
    app.run(debug=True)