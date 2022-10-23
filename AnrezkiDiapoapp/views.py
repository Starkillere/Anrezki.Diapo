from flask  import Flask, render_template, request, send_file, redirect, url_for, session
from hashlib import sha1
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import os
import random
from . import data_prosses, user_manager


app = Flask(__name__)
app.config.from_object("config")
app.secret_key = app.config["SECRET_KEY"]
app.permanent_session_lifetime = timedelta(days=1)

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    password = db.Column(db.String(200), nullable=False)
    droit_acces = db.Column(db.String(200), nullable=False)

    def __init__(self, password, droit_acces):
        self.password = password
        self.droit_acces = droit_acces

def t_init_db():
    db.drop_all()
    admin = User(sha1("admine+complex".encode()).hexdigest(), "ALL")
    db.session.add(admin)
    db.session.commit()
    db.create_all()

@app.route('/', methods=["GET", "POST"])
def acceuil():
    if request.method == "POST":
        password = request.form["password"]
        droit_acces = user_manager.login(password, User)
        if droit_acces:
            session['CONNECTED'] = True
            session["ACCESS"] = droit_acces
            return redirect(url_for("acceuil"))
    if "CONNECTED" in session:
        if session["ACCESS"] == "ALL":
            nbdiapo, datas = data_prosses.acceuil_data_print()
        else:
            nbdiapo, datas = (1, ["Confidentialité", "droits accées", "statistique"])    
        images = os.listdir("./AnrezkiDiapoapp/static/images/prewies/")
        image = random.choice(images)
        if nbdiapo > 1:
            text = f"{nbdiapo} présentations disponibles !"
        else:
            text = f"{nbdiapo} présentation disponible !"
        return render_template("accueil.html", connected=session['CONNECTED'], text=text, datas=datas, image=f"/static/images/prewies/{image}")
    return render_template("accueil.html", connected=False)

@app.route('/add_user', methods=["GET", "POST"])
def new_users():
    if "CONNECTED" in session and session["ACCESS"] == "ALL":
        if request.method == "POST":
            password = request.form["password"]
            acce =  request.form["acce"]
            user_manager.add_user(password, acce, User, db)
        return render_template("data-add_user.html")
    return redirect(url_for("acceuil"))   


@app.route("/tableau-de-bord", methods=["GET", "POST"])
def tableau():
    if "CONNECTED" in session:
        if session["ACCESS"] == "ALL":
            presentations = data_prosses.presentation_reterner()
        else:
            presentations = [session["ACCESS"]]
        if request.method == "POST":
            session["PRESENTATION"] = request.form["presentation"]
            return redirect(url_for("presentation"))
        return render_template("tableau_de_bord.html", connected=session['CONNECTED'], presentations=presentations)
    return redirect(url_for("acceuil"))

@app.route("/presentation", methods=["GET", "POST"])
def presentation():
    if "CONNECTED" in session:
        if request.method == "POST":
            mode = request.form["mode"]
            the_presentation = session["PRESENTATION"]
            diapos = [diapo for diapo in os.listdir("./AnrezkiDiapoapp/templates/") if not os.path.isfile(os.path.join("./AnrezkiDiapoapp/templates/", diapo)) and diapo[:len("Diaporama-")] == "Diaporama-"]
            for diapo in diapos:
                if diapo.split("-")[1] == the_presentation:
                    the_diapo = diapo
                    break
            if mode == "modifier":
                diapo = request.files["diapo"]
                
                filename = f"./AnrezkiDiapoapp/templates/{the_diapo}/{the_presentation+'.'+diapo.filename.split('.')[-1]}"
                if os.path.exists(filename):
                    os.remove(filename)

                diapo.save(filename)
            elif mode == "laod":
                for file in os.listdir(f"./AnrezkiDiapoapp/templates/{the_diapo}/"):
                    if '.'.join(file.split('.')[:-1]) == the_presentation:
                        format_is =  file.split(".")[-1]
                return send_file(f"templates/{the_diapo}/{the_presentation+'.'+format_is}", as_attachment=True)
            else:
                return render_template(f"{the_diapo}/presentation.html")
        return render_template("gestion-diaporama.html", connected=session['CONNECTED'])
    return redirect(url_for("acceuil"))

@app.errorhandler(404)
def page_not_found(error):
    if "CONNECTED" in session:
        return render_template('404.html', connected=session['CONNECTED']), 404
    return redirect(url_for("acceuil"))