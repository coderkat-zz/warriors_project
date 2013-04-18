from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref



# set up the ability to interact with the db w/a session
engine = create_engine(os.environ['DATABASE_URL'], echo=False)
session = scoped_session(sessionmaker(bind=engine, autocommit = False, autoflush = False))

Base = declarative_base() # required for SQLAlchemy's magic to magic
Base.query = session.query_property()

### Class declarations go here
class Users(Base):
	__tablename__ = "users" # inform SQLAlchemy that instances of this class will be stored in the table 'users'

	id = Column(Integer, primary_key = True)
	email = Column(String(64))
	password = Column(String(64))

class Participants(Base):
	__tablename__ = "participants"

	id = Column(Integer, primary_key = True)
	name = Column(String(128))
	chances = Column(Integer)

class Winners(Base):
	__tablename__ = "winners"

	id = Column(Integer, primary_key = True)
	game = Column(Integer)
	participant_id = Column(Integer, ForeignKey("participants.id"))

	winner = relationship("Participants", backref=backref("winners", order_by=id))

### End class declarations
def connect():
	global ENGINE
	global Session # a class generated by SQLAlchemy, describing how to interact with the db

	ENGINE = create_engine("sqlite:///lottery2.db", echo=True)
	Session = sessionmaker(bind=ENGINE) # instantiate a session and return the instance below (can later use session = Session())
	return Session()

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
