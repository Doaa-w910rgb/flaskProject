from flasktasks import db, app

from flasktasks.models import User, Post
import sys


def create_db():
    with app.app_context():
        # you will have instance folder with site.db inside
        db.create_all()
        
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'create_db':
        create_db()
        print("Database created successfully!")
    else:
        print("Invalid command. Please use 'python db_test.py create_db' to create the database.") 