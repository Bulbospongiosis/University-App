from flask import Flask, render_template, request, session
import json

app = Flask(__name__)
app.secret_key = 'yoursecretkey'  # Needed for session storage

# University data
json_string = [
    {"University": "McGill University", "Tuition": 12730.80, "Location": "Quebec", "Living": 1300, "Co-op": "Limited", "Food": True, "Extra": 250, "Rank": 1},
    {"University": "University of Toronto", "Tuition": 6590, "Location": "Ontario", "Living": 1800, "Co-op": "Extensive", "Food": True, "Extra": 1000, "Rank": 2},
    {"University": "University of British Columbia", "Tuition": 5646.4, "Location": "BC", "Living": 1550, "Co-op": "Extensive", "Food": True, "Extra": 350, "Rank": 3},
    {"University": "University of Alberta", "Tuition": 5320.8, "Location": "Alberta", "Living": 2916, "Co-op": "Limited", "Food": True, "Extra": 450, "Rank": 4},
    {"University": "Western University", "Tuition": 7576, "Location": "Ontario", "Living": 1500, "Co-op": "Mid", "Food": True, "Extra": 200, "Rank": 5},
    {"University": "Université de Montréal", "Tuition": 7500, "Location": "Quebec", "Living": 2000, "Co-op": "Limited", "Food": False, "Extra": 80, "Rank": 6},
    {"University": "McMaster University", "Tuition": 12000, "Location": "Ontario", "Living": 1500, "Co-op": "Mid", "Food": True, "Extra": 300, "Rank": 7},
    {"University": "Queens University in Kingston", "Tuition": 6153, "Location": "Ontario", "Living": 3489, "Co-op": "Extensive", "Food": True, "Extra": 300, "Rank": 8},
    {"University": "University of Calgary", "Tuition": 7200, "Location": "Alberta", "Living": 1900, "Co-op": "Limited", "Food": True, "Extra": 300, "Rank": 9},
    {"University": "University of Waterloo", "Tuition": 13500, "Location": "Ontario", "Living": 1900, "Co-op": "Extensive", "Food": True, "Extra": 200, "Rank": 10}
]

Uniname = {uni["University"]: 0 for uni in json_string}
Unilist = list(Uniname.keys())


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/form/question1', methods=['GET', 'POST'])
def form1():
    if request.method == "POST":
        session['tuitionnn'] = "tuition" in request.form
        session['locationnn'] = "location" in request.form
        session['livingnn'] = "living" in request.form
        session['coopnn'] = "co-op" in request.form
        session['foodnn'] = "food" in request.form
        session['extrann'] = "extra" in request.form
    return render_template("form.html")


@app.route('/form/question2', methods=['GET', 'POST'])
def form2():
    if request.method == "POST":
        for i in range(1, 6):
            session[f'cost{i}'] = f"2:{i}" in request.form
    return render_template("form2.html")


@app.route("/form/question3", methods=['GET', 'POST'])
def form3():
    if request.method == "POST":
        session['Ontario'] = "3:1" in request.form
        session['BritishColumbia'] = "3:2" in request.form
        session['Quebec'] = "3:3" in request.form
        session['Alberta'] = "3:4" in request.form
    return render_template("form3.html")


@app.route("/form/question4", methods=['GET', 'POST'])
def form4():
    if request.method == "POST":
        for i in range(1, 6):
            session[f'livecost{i}'] = f"4:{i}" in request.form
    return render_template("form4.html")


@app.route("/form/question5", methods=['GET', 'POST'])
def form5():
    if request.method == "POST":
        session['extensive'] = "5:1" in request.form
        session['limited'] = "5:2" in request.form
        session['noprefer'] = "5:3" in request.form
    return render_template("form5.html")


@app.route("/form/question6", methods=['GET', 'POST'])
def form6():
    if request.method == "POST":
        session['yes'] = "6:1" in request.form
        session['no'] = "6:2" in request.form
    return render_template("form6.html")


@app.route("/form/question7", methods=['GET', 'POST'])
def form7():
    if request.method == "POST":
        for i in range(1, 6):
            session[f'club{i}'] = f"7:{i}" in request.form

    # Reset scores
    scores = {uni: 0 for uni in Unilist}

    # --- Tuition ---
    tuition_limits = {5: float('inf'), 4: 11000, 3: 9000, 2: 7000, 1: 5000}
    for i in range(5, 0, -1):
        if session.get(f'cost{i}'):
            limit = tuition_limits[i]
            for uni in json_string:
                if uni["Tuition"] > limit:
                    if session.get('tuitionnn'):
                        scores[uni["University"]] = -1e9
                else:
                    scores[uni["University"]] += 1
            break

    # --- Location ---
    for loc in ["Ontario", "BritishColumbia", "Quebec", "Alberta"]:
        if session.get(loc):
            for uni in json_string:
                if uni["Location"] == (loc if loc != "BritishColumbia" else "BC"):
                    scores[uni["University"]] += 1
                elif session.get('locationnn'):
                    scores[uni["University"]] = -1e9

    # --- Living cost ---
    living_limits = {5: float('inf'), 4: 11000, 3: 9000, 2: 7000, 1: 5000}
    for i in range(5, 0, -1):
        if session.get(f'livecost{i}'):
            limit = living_limits[i]
            for uni in json_string:
                if uni["Living"] > limit:
                    if session.get('livingnn'):
                        scores[uni["University"]] = -1e9
                else:
                    scores[uni["University"]] += 1
            break
    
    # --- Co-op ---
    for cop in ["extensive", "limited", "noprefer"]:
        if session.get(cop):
            for uni in json_string:
                if uni["Co-op"] == cop:
                    scores[uni["University"]] += 1
                elif session.get('coopnn'):
                    scores[uni["University"]] = -1e9
    
    # --- Food ---
    for food in ["yes", "no",]:
        if session.get(food):
            for uni in json_string:
                if uni["Food"] == food:
                    scores[uni["University"]] += 1
                elif session.get('foodnn'):
                    scores[uni["University"]] = -1e9
    
    # --- Club Quantity ---
    club_limits = {5: float('inf'), 4: 750, 3: 500, 2: 350, 1: 200}
    for i in range(5, 0, -1):
        if session.get(f'club{i}'):
            limit = club_limits[i]
            for uni in json_string:
                if uni["Living"] > limit:
                    if session.get('extrann'):
                        scores[uni["University"]] = -1e9
                else:
                    scores[uni["University"]] += 1
            break


    # Sort by score (highest first)
    sorted_dict = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))
    print(sorted_dict)  # Debug

    return render_template("form7.html", results=sorted_dict)


if __name__ == '__main__':
    app.run(debug=True)
