from app import db
# from models import Flaskr

# create the db and the tables 
db.create_all()

# commit the changes
db.session.commit()
