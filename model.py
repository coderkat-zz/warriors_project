import sqlite3

def connect_db():
	return sqlite3.connect("lottery.db")


def new_user(db, email, password, name):
	c = db.cursor()
	query = """INSERT INTO Users VALUES (NULL, ?, ?, ?)"""
	result = c.execute(query, (email, password, name))
	db.commit()
	return result.lastrowid

def authenticate(db, email, password):
	c = db.cursor()
	query = """SELECT * from Users WHERE email=? AND password=?"""
	c.execute(query, (email, password))
	result = c.fetchone()
	if result:
		fields = ["id", "email", "password", "name"]
		return dict(zip(fields, result))

	return None

def get_user(db, user_id):
    c = db.cursor()
    user_id = str(user_id)
    query = """SELECT * FROM Users WHERE id = ?"""
    c.execute(query, (user_id))
    row = c.fetchone()
    if row:
        fields = ['id', 'email', 'password', 'first_name', 'last_name']
        return dict(zip(fields, row))

    return None

def new_participant(db, name, chances):
	c = db.cursor()
	query = """INSERT INTO Participants VALUES (NULL, ?, ?)"""
	result = c.execute(query, (email, password, name))
	db.commit()
	return result.lastrowid

def get_participant(db, name):
	c = db.cursor()
	query = """SELECT * FROM Participants WHERE name=?"""
	c.execute(query, (name))
	row = c.fetchone()
	if row:
		fields = ['id', 'name', 'chances']
		return dict(zip(fields, row))

	return None

def update_participant(db, name):
	c = db.cursor()
	query = """UPDATE Participants SET chances=(chances-1) WHERE name=?"""
	result = c.execute(query, (chances, name))
	db.commit()
	return

def get_participants(db):
	c = db.cursor()
	query = """SELECT * from Participants"""
	c.execute(query)

	rows = c.fetchall

	if rows:
		fields = ['id', 'name', 'chances']
		participants = []
		for row in rows:
			participant = dict(zip(fields, row))
			participants.append(participant) #dict is now an item in the list of dicts w/field name mapped to info
		return participants

	return None

def new_winner(db, name):
	c = db.cursor()
	query = """INSERT INTO Winners VALUES (NULL, ?)"""
	result = c.execute(query, (name))
	db.commit()
	return result.lastrowid

def get_winners(db):
	c = db.cursor()
	query = """SELECT * from Winners"""
	c.execute(query)

	rows = c.fetchall

	if rows:
		fields = ['id', 'name']
		winners = []
		for row in rows:
			winner = dict(zip(fields, row))
			winners.append(winner) #dict is now an item in the list of dicts w/field name mapped to info
		return winners

	return None

