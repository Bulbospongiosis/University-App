from flask import Flask, render_template, request, session, redirect, url_for
import json

app = Flask(__name__)
app.secret_key = 'yoursecretkey'  # Needed for session storage

# University data
json_string = [
    {"University": "McGill University", "Tuition": 12730.80, "Location": "Quebec", "Living": 1300, "Co-op": 1, "Food": 1, "Extra": 250, "Rank": 1},
    {"University": "University of Toronto", "Tuition": 6590, "Location": "Ontario", "Living": 1800, "Co-op": 2, "Food": 1, "Extra": 1000, "Rank": 2},
    {"University": "University of British Columbia", "Tuition": 5646.4, "Location": "BC", "Living": 1550, "Co-op": 2, "Food": 1, "Extra": 350, "Rank": 3},
    {"University": "University of Alberta", "Tuition": 5320.8, "Location": "Alberta", "Living": 2916, "Co-op": 1, "Food": 1, "Extra": 450, "Rank": 4},
    {"University": "Western University", "Tuition": 7576, "Location": "Ontario", "Living": 1500, "Co-op": 1, "Food": 1, "Extra": 200, "Rank": 5},
    {"University": "Université de Montréal", "Tuition": 7500, "Location": "Quebec", "Living": 2000, "Co-op": 1, "Food": 2, "Extra": 80, "Rank": 6},
    {"University": "McMaster University", "Tuition": 12000, "Location": "Ontario", "Living": 1500, "Co-op": 1, "Food": 1, "Extra": 300, "Rank": 7},
    {"University": "Queens University in Kingston", "Tuition": 6153, "Location": "Ontario", "Living": 3489, "Co-op": 2, "Food": 1, "Extra": 300, "Rank": 8},
    {"University": "University of Calgary", "Tuition": 7200, "Location": "Alberta", "Living": 1900, "Co-op": 1, "Food": 1, "Extra": 300, "Rank": 9},
    {"University": "University of Waterloo", "Tuition": 11000, "Location": "Ontario", "Living": 1900, "Co-op": 2, "Food": 1, "Extra": 200, "Rank": 10}
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
        return redirect("/form/question2")
    return render_template("form.html")


@app.route('/form/question2', methods=['GET', 'POST'])
def form2():
    if request.method == "POST":
        
        session['cost'] =  request.form.get('cost')
        return redirect("/form/question3")
    return render_template("form2.html")


@app.route("/form/question3", methods=['GET', 'POST'])
def form3():
    if request.method == "POST":
        session['Ontario'] = "3:1" in request.form
        session['BritishColumbia'] = "3:2" in request.form
        session['Quebec'] = "3:3" in request.form
        session['Alberta'] = "3:4" in request.form
        return redirect("/form/question4")
    return render_template("form3.html")


@app.route("/form/question4", methods=['GET', 'POST'])
def form4():
    if request.method == "POST":
        
        session['livecost'] = request.form.get("live")
        return redirect("/form/question5")
    return render_template("form4.html")


@app.route("/form/question5", methods=['GET', 'POST'])
def form5():
    if request.method == "POST":
        session['coop?'] = request.form.get("coop")
        return redirect("/form/question6")
    return render_template("form5.html")


@app.route("/form/question6", methods=['GET', 'POST'])
def form6():
    if request.method == "POST":
        session['food?'] = request.form.get("yum")
        return redirect("/form/question7")
    return render_template("form6.html")


@app.route("/form/question7", methods=['GET', 'POST'])
def form7():
    if request.method == "POST":
        
        session['club'] = request.form.get("club")
        return redirect("/form/results")

    

    return render_template("form7.html")





@app.route("/form/results")
def results():

    # Reset scores
    scores = {uni: 0 for uni in Unilist}

    # --- Tuition ---
    tuition_limits = {5: float('inf'), 4: 11000, 3: 9000, 2: 7000, 1: 5000}
   
    limit = tuition_limits[int(session.get('cost'))]
    for uni in json_string:
        if uni["Tuition"] > limit:
            if session.get('tuitionnn'):
                scores[uni["University"]] = -1e9
        else:
            scores[uni["University"]] += 1
        

    # --- Location ---
    selected_locations = []
    if session.get("Ontario"):
        selected_locations.append("Ontario")
    if session.get("BritishColumbia"):
        selected_locations.append("BC")
    if session.get("Quebec"):
        selected_locations.append("Quebec")
    if session.get("Alberta"):
        selected_locations.append("Alberta")

    if selected_locations:  # User picked something
        for uni in json_string:
            if uni["Location"] in selected_locations:
                scores[uni["University"]] += 1
            elif session.get('locationnn'):  # Non-negotiable
                scores[uni["University"]] = -1e9

    # --- Living cost ---
    living_limits = {5: float('inf'), 4: 3000, 3: 2500, 2: 2000, 1: 1500}
    
    limit = living_limits[int(session.get("livecost"))]
    for uni in json_string:
        if uni["Living"] > limit:
            if session.get('livingnn'):
                scores[uni["University"]] = -1e9
        else:
            scores[uni["University"]] += 1
        
    
    # --- Co-op ---
    
    for uni in json_string:
        if uni["Co-op"] >= int(session.get("coop?")):
            scores[uni["University"]] += 1
        elif session.get('coopnn'):
            scores[uni["University"]] = -1e9
    
    # --- Food ---
    
    for uni in json_string:
        if uni["Food"] >= int(session.get("food?")):
            scores[uni["University"]] += 1
        elif session.get('foodnn'):
            scores[uni["University"]] = -1e9
    
    # --- Club Quantity ---
    club_limits = {5: float('inf'), 4: 500, 3: 350, 2: 200, 1: 50}
    
    limit = club_limits[int(session.get("club"))]
    for uni in json_string:
        if uni["Extra"] < limit:
            if session.get('extrann'):
                scores[uni["University"]] = -1e9
        else:
            scores[uni["University"]] += 1
        


    # Sort by score (highest first)
    sorted_dict = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))
    print(sorted_dict)  # Debug

    return render_template("formresults.html", results=sorted_dict)

if __name__ == '__main__':
    app.run(debug=True)
