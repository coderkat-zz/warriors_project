from flask import Flask, flash, session, render_template, request, redirect, url_for, g
import model # has all SQL queries
import random


app = Flask(__name__)
app.secret_key = 'bananabananabanana'

# call before executing each view
@app.before_request
def set_up_db():
	g.db = model.connect_db()

# close db connection after rendering each view
@app.teardown_request
def close_db(e): # allow db closure even if errors
	g.db.close()

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/login")
def login():
	return render_template("login.html")

@app.route("/authenticate", methods=["POST"])
def authenticate():
	email = request.form['email']
	password = request.form['password']

	user_info = model.authenticate(g.db, email, password)

	if not user_info:
		flash("Incorrect username or password.")
		return redirect(url_for("login"))

	else:
		session['user_id'] = user_info['id']
		session['name'] = user_info['name']
		return redirect(url_for("drawing"))  

@app.route("/logout")
def logout():
	session.pop('email', None)
	session.pop('id', None)
	flash('You have successfully logged out.')
	return redirect(url_for("login"))

@app.route("/drawing")
def drawing():
	return render_template("drawing.html")

@app.route("/draw")
def draw():
	participants = model.get_participants(g.db) #returns dict of participants # their # of entries
	drawing_list = []
	for person in participants: # for each dictionary item (participant)
		for i in range(person['chances']): # as many times as they have 'chances':
			drawing_list.append(person['name']) # makes just a huge list of names, repeated as many times as they have chances to win

	random.shuffle(drawing_list)

	# randomly select a name from the list
	winner = drawing_list[random.randint(0, len(drawing_list)-1)]

	return render_template("accept_winner.html", winner_name=winner)

@app.route("/save_winner", methods=["POST"])
def save_winner():
	# grab winner name from form on draw page
	winner_name = request.form['winner']
	# call model and add winner to Winners table
	model.new_winner(g.db, winner_name)
	# call model, remove one chance from participant
	model.update_participant(g.db, winner_name)

	return render_template("draw_again.html")

@app.route("/winners")
def winners():
	winners = model.get_winners(g.db)

	return render_template("winners.html", winners=winners)







if __name__ == "__main__":
    app.run(debug=True)