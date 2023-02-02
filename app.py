from flask import Flask, render_template, flash, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user
from datetime import datetime
from forms import LoginForm
import json

app = Flask(__name__)
app.config["SECRET_KEY"] = 'e79b9847144221ba4e85df9dd483a3e5'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///toner.db"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).filter(User.id == user_id).first()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    history = db.relationship("Log", backref="lastActions", lazy=True)

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email}')"


class Drucker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(30), unique=True, nullable=False)
    toner = db.relationship("DruTo", backref="druckerRel", lazy=True)

    def __repr__(self):
        return f"Drucker('{self.model}')"


class Toner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    count = db.Column(db.Integer)
    drucker = db.relationship("DruTo", backref="tonerRel", lazy=True)

    def __repr__(self):
        return f"Toner('{self.name}', '{self.count}')"


class DruTo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    drucker = db.Column(db.ForeignKey("drucker.id"), nullable=False)
    toner = db.Column(db.ForeignKey("toner.id"), nullable=False)

    def __repr__(self):
        return f"DruckerToner('{self.drucker}', '{self.toner}')"


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user = db.Column(db.String(30), db.ForeignKey("user.id"), nullable=False)
    action = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"Log('{self.date}', '{self.user}', '{self.action}')"


with app.app_context():
    pass


@app.route('/', methods=["GET", "POST", "PUT", "DELETE"])
def home():
    if request.method == "POST":
        dru = request.form["formModel"]
        ton = request.form["formToner"]
        summ = request.form["formMenge"]
        act = request.form["formAktion"]
        updt = db.session.query(Toner).join(DruTo).filter(DruTo.drucker == dru).filter(Toner.name == ton).first()
        if act == "ADD":
            try:
                db.session.query(Toner).filter(Toner.id == updt.id).update({'count': Toner.count + summ})
                db.session.add(Log(user=current_user.username, action=summ + " Toner " + ton + " für " + db.session.query(Drucker).filter(Drucker.id == dru).first().model + " eingelagert"))
            except AttributeError:
                flash("Fehler: Für dieses Druckermodell existiert der angegebene Toner nicht!", "danger")
                return redirect(url_for("home"))
            db.session.commit()
        if act == "SUB":
            if int(db.session.query(Toner).filter(Toner.id == updt.id).first().count) < int(summ):
                flash("Fehler: Es sind laut Datenbank nicht genügend Toner in der Liste. Bitte Inventur vornehmen.", "danger")
                return redirect(url_for("home"))
            try:
                db.session.query(Toner).filter(Toner.id == updt.id).update({'count': Toner.count - summ})
                db.session.add(Log(user=current_user.username, action=summ+" Toner " + ton + " für " + db.session.query(Drucker).filter(Drucker.id == dru).first().model + " ausgegeben"))
            except AttributeError:
                flash("Fehler: Für dieses Druckermodell existiert der angegebene Toner nicht!", "danger")
                return redirect(url_for("home"))
            db.session.commit()
    druto = DruTo.query.all()
    drucker = Drucker.query.all()
    toner = Toner.query.all()
    log = Log.query.order_by(Log.id.desc()).limit(3).all()
    data = list()
    for i in druto:
        a = Drucker.query.filter_by(id=i.drucker).first()
        b = Toner.query.filter_by(id=i.toner).first()
        data.append({"printer": a.id, "toner": b.name, "count": b.count, "tid": b.id})
    return render_template('main.html', drucker=drucker, data=data, toner=toner, log=log)


@app.route('/logs', methods=["GET", "POST"])
def logs():
    log = Log.query.all()
    return render_template("logs.html", logs=log)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            flash("Eingeloggt als " + user.username + "!", "success")
            return redirect(url_for("home"))
        else:
            flash("Falsches Passwort oder Benutzername", "danger")
    return render_template("login.html", title="login", form=form)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
