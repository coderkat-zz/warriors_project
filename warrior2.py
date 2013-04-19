from flask import Flask, render_template, redirect, request, session, g, flash, url_for
import model2 as model
import random
import os
from model2 import session as db_session, Users, Participants, Winners
# from flask.ext.heroku import Heroku
from flask_heroku import Heroku  
# from flask.ext.sqlalchemy import SQAlchemy 
import os

app = Flask(__name__)
heroku = Heroku(app)
app.config.from_object(__name__)

app.secret_key = "bananabananabanana"

@app.teardown_request
def shutdown_session(exception = None):
    db_session.remove()

@app.before_request
def load_user_id():
    g.user_id = session.get('user_id')

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

	user = db_session.query(Users).filter_by(email=email, password=password).first()

	if user:
		session['user_id'] = user.id
		flash("Successfully logged in!")
		new_winners = db_session.query(Winners).all()
		games_won = []
		for winner in new_winners:
			games_won.append(winner.game)
		games_dict = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 17:0, 18:0}
		for i in games_won:
			games_dict[i] += 1
		return render_template("draw_again2.html", chosen_games=games_dict)
	else:
		flash("Incorrect new user name or password")
		return redirect(url_for('login'))

@app.route("/dashboard", methods=["GET"])
def dashboard():
	if not g.user_id:
		flash("Not logged in!")
		return redirect(url_for('login'))
	else:
		new_winners = db_session.query(Winners).all()
		games_won = []
		for winner in new_winners:
			games_won.append(winner.game)
		games_dict = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 17:0, 18:0}
		for i in games_won:
			games_dict[i] += 1
		return render_template("draw_again2.html", chosen_games=games_dict)


@app.route("/logout")
def logout():
	if g.user_id:
		del session['user_id']
		flash('You have successfully logged out.')
		return redirect(url_for("index"))
	else:
		flash('You were not logged in.')
		return redirect(url_for("index"))

@app.route("/drawing", methods=["GET", "POST"])
def drawing():
	if not g.user_id:
		flash("Please log in")
		return redirect(url_for("index"))
	else:
		game = request.form['game']
		return render_template("drawing.html", game=game)

# TODO: Figure out how to get the game number in here!
@app.route("/draw", methods=["GET", "POST"])
def draw():
	if not g.user_id:
		flash("Please log in")
		return redirect(url_for("index"))

	game = request.form['game']

	participants = db_session.query(Participants).all() #returns dict of participants # their # of entries
	drawing_list = []
	for person in participants: # for each dictionary item (participant)
		for i in range(person.chances): # as many times as they have 'chances':
			drawing_list.append(person.name) # makes just a huge list of names, repeated as many times as they have chances to win

	random.shuffle(drawing_list)

	# randomly select a name from the list
	winner = drawing_list[random.randint(0, len(drawing_list)-1)]

	return render_template("accept_winner.html", winner_name=winner, game=game)

#this view opens & we have winner's name and the game number
@app.route("/save_winner", methods=["POST", 'GET'])
def save_winner():
	# grab winner name from form on draw page
	set_winners = db_session.query(Winners).all()

	winner_name = request.form['winner']
	winner_game = int(request.form['game'])
	winner = db_session.query(Participants).filter_by(name=winner_name).first()

	# Check to see if winner already won for that game: if so, flash error and pick again
	if set_winners:
		for entry in set_winners:
			if entry.game == winner_game and entry.participant_id == winner.id:
				flash("Oops, looks like that person already won one of the sets of tickets. Pick again!")
				return render_template("drawing.html", game=winner_game)

	# add winner to Winners table
	win = Winners(game=winner_game, participant_id=winner.id)
	db_session.add(win)
	db_session.commit()


	# remove one chance from participant's chances
	winner.chances = winner.chances - 1
	db_session.commit()

	# grab which games have been chosen for next page view
	new_winners = db_session.query(Winners).all()
	games_won = []
	for winner in new_winners:
		games_won.append(winner.game)
	games_dict = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 17:0, 18:0}
	for i in games_won:
		games_dict[i] += 1

	return render_template("draw_again2.html", chosen_games=games_dict)

@app.route("/draw_again", methods=['POST', 'GET'])
def draw_again():
	if not g.user_id:
		flash("Please log in")
		return redirect(url_for("index"))

	test = request.form["game"]
	return render_template("drawing.html", game=test)

@app.route("/winners", methods=["GET", "POST"])
def winners():

	winners_db = db_session.query(Winners).all() #list of dictionaries of winners
	
	final_winners = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[], 11:[], 12:[], 13:[], 14:[], 15:[], 16:[], 17:[], 18:[]}

	if winners_db:
		# get participant id
		for win in winners_db:
			pid = win.participant_id
			winner = db_session.query(Participants).filter_by(id=pid).first()
			game = win.game
			final_winners[game].append(winner.name)

		for i in final_winners:
			if not final_winners[i]:
				next_game = i
				break

		return render_template("winners2.html", winners=final_winners, next_game=next_game)

	else:
		flash("No winners selected yet.")
		return redirect(url_for("index"))  

if __name__ == "__main__":
	db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
	model.connect(db_uri)
	app.run(debug = True)