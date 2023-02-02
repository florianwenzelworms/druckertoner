from app import app, db, User
from flask_bcrypt import Bcrypt
import sys

if __name__ == "__main__":
    if sys.argv[1] == "add":
        if len(sys.argv) == 5:
            with app.app_context():
                bcrypt = Bcrypt(app)
                u = User(username=sys.argv[2], password=bcrypt.generate_password_hash(sys.argv[3]).decode("utf-8"), email=sys.argv[4] )
                db.session.add(u)
                db.session.commit()
        else:
            print("Format: adduser <name> <password> <email>")
    if sys.argv[1] == "passwd":
        if len(sys.argv) == 4:
            with app.app_context():
                bcrypt = Bcrypt(app)
                db.session.query(User).filter(User.username == sys.argv[2]).update({'password': bcrypt.generate_password_hash(sys.argv[3]).decode("utf-8")})
                db.session.commit()
        else:
            print("Format: changepw <name> <password>")
