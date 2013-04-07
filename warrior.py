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
	return render_template("drawing.html", game=1)

@app.route("/draw_again", methods=["POST"])
def draw_again():
	request.form['game']
	game = request.form['game']
	print game
	return render_template("drawing.html", game=game)

# TODO: Figure out how to get the game number in here!
@app.route("/draw", methods=["GET", "POST"])
def draw():


	game = request.form['game']

	participants = model.get_participants(g.db) #returns dict of participants # their # of entries
	drawing_list = []
	for person in participants: # for each dictionary item (participant)
		for i in range(person['chances']): # as many times as they have 'chances':
			drawing_list.append(person['name']) # makes just a huge list of names, repeated as many times as they have chances to win

	random.shuffle(drawing_list)

	# randomly select a name from the list
	winner = drawing_list[random.randint(0, len(drawing_list)-1)]

	return render_template("accept_winner.html", winner_name=winner, game=game)

@app.route("/game_1")
def game_1():
	participants = model.get_participants(g.db) #returns dict of participants # their # of entries
	drawing_list = []
	for person in participants: # for each dictionary item (participant)
		for i in range(person['chances']): # as many times as they have 'chances':
			drawing_list.append(person['name']) # makes just a huge list of names, repeated as many times as they have chances to win

	random.shuffle(drawing_list)

	# randomly select a name from the list
	winner = drawing_list[random.randint(0, len(drawing_list)-1)]

	return render_template("accept_winner.html", winner_name=winner, game=1)

@app.route("/game_2")
def game_2():
	participants = model.get_participants(g.db) #returns dict of participants # their # of entries
	drawing_list = []
	for person in participants: # for each dictionary item (participant)
		for i in range(person['chances']): # as many times as they have 'chances':
			drawing_list.append(person['name']) # makes just a huge list of names, repeated as many times as they have chances to win

	random.shuffle(drawing_list)

	# randomly select a name from the list
	winner = drawing_list[random.randint(0, len(drawing_list)-1)]

	return render_template("accept_winner.html", winner_name=winner, game=2)

@app.route("/game_3")
def game_3():
	participants = model.get_participants(g.db) #returns dict of participants # their # of entries
	drawing_list = []
	for person in participants: # for each dictionary item (participant)
		for i in range(person['chances']): # as many times as they have 'chances':
			drawing_list.append(person['name']) # makes just a huge list of names, repeated as many times as they have chances to win

	random.shuffle(drawing_list)

	# randomly select a name from the list
	winner = drawing_list[random.randint(0, len(drawing_list)-1)]

	return render_template("accept_winner.html", winner_name=winner, game=3)

@app.route("/save_winner", methods=["POST"])
def save_winner():
	# grab winner name from form on draw page
	set_winners = model.get_winners(g.db)

	winner_name = request.form['winner']
	winner_game = int(request.form['game'])

	# find all won games in case of duplicate winner
	if set_winners:
		set_game1 = 0
		set_game2 = 0
		set_game3 = 0
		for entry in set_winners:
			if entry['game'] == 1:
				set_game1 += 1
			elif entry['game'] == 2:
				set_game2 += 1
			elif entry['game'] == 3:
				set_game3 += 1

	# Check to see if winner already won for that game: if so, flash error and pick again
	if set_winners:
		for entry in set_winners:
			if entry['game'] == winner_game and entry['name'] == winner_name:
				flash("Oops, looks like that person already won one of the sets of tickets. Pick again!")
				return render_template("draw_again.html", game1=set_game1, game2=set_game2, game3=set_game3)

	# call model and add winner to Winners table
	model.new_winner(g.db, winner_name, winner_game)
	# call model, remove one chance from participant
	model.update_participant(g.db, winner_name)
	# pull up list of dicts of winners to use when rendering next page
	winners = model.get_winners(g.db)
	#find new distribution of winners
	game1 = 0
	game2 = 0
	game3 = 0
	for entry in winners:
		if entry['game'] == 1:
			game1 += 1
		elif entry['game'] == 2:
			game2 += 1
		elif entry['game'] == 3:
			game3 += 1

	return render_template("draw_again.html", game1=game1, game2=game2, game3=game3)

@app.route("/winners")
def winners():
	winners = model.get_winners(g.db) #list of dictionaries of winners
	
	if winners:

		final_winners = {'Game1': [], 'Game2': [], 'Game3': [], 'Game4': []}
		for winner in winners:
			if winner['game'] == 1:
				final_winners['Game1'].append(winner['name'])
			elif winner['game'] == 2:
				final_winners['Game2'].append(winner['name'])
			elif winner['game'] == 3:
				final_winners['Game3'].append(winner['name'])
			
		return render_template("winners.html", winners=final_winners)

	else:
		flash("No winners selected yet.")
		return redirect(url_for("index"))  









if __name__ == "__main__":
    app.run(debug=True)