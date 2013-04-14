import model2 as model
import csv
import sqlalchemy.exc
import datetime

def load_participants(session):
    participants = {"Gary":18, "Smith":15, "Art":15, "Ken":9, "Steve Dinetz":9, "Steve Neely":6, "Jay":4, "Gilbert":3, "Stein":2, "Cate":1}
    for part in participants:
        chances = participants[part]
        # put all of this info into our db w/sqlalchemy
        participant = model.Participants(name=part, chances=chances)
        # stage new data to comit
        session.add(participant)
        #commit new user line
        session.commit()

def load_users(session):
	dave = model.Users(email="smith@mediasmith.com", password="warriors123")
	session.add(dave)
	session.commit()

	kat =  model.Users(email="kat@coderkat.com", password="password")
	session.add(kat)
	session.commit()

def main(session):
    load_participants(session)
    load_users(session)
 

if __name__ == "__main__":
    s= model.connect()
    main(s)