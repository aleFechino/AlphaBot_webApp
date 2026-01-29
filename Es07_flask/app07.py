from flask import Flask, render_template, request, redirect, url_for
from flask_login import (LoginManager, UserMixin, login_user, login_required, logout_user, current_user)
import AlphaBot 
import threading
import time
import RPi.GPIO as GPIO
import sqlite3 

app=Flask(__name__)
app.secret_key="chiaveSegreta" #chiave che scegliamo noi

#inizializzo la pagina
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view="login" #senza estensione .html

robot=AlphaBot.AlphaBot()
robot.stop()

#pin sensori
DR=16
DL=19

#db movimenti
DB_movimenti="./db1_comandi.db"

#db users
DB_users="./db_users.db"

class User(UserMixin):
    def __init__(self, id):
        self.id=id

@login_manager.user_loader
def load_user(user_id):
    if user_id in USERS: #query del db
        return User(user_id) #userget restituisce una stringa        User.get(user_id)
    return None

#FUNZIONI PER IL DB MOVIMENTI
def access_DB_movimenti(db, key):
    con= sqlite3.connect(db)
    cur= con.cursor()
    
    res=cur.execute(f"SELECT command_description FROM movement WHERE key='{key}'")

    record=res.fetchall()
    #print(record)

    commands=record[0][0].split("|")
    #print(command)
    con.close()

    return commands

def run_db_movimenti(comands):
    for com in comands:
        move=com.split(",")
        diz_command[move[0]]()
        time.sleep(float(move[1]))

diz_command={"forward":robot.forward, 
             "backward":robot.backward, 
             "left":robot.left, 
             "right":robot.right,
             "stop":robot.stop}

#FUNZIONI PER IL DB USER
def access_DB_user(db):
    con= sqlite3.connect(db)
    cur= con.cursor()

    res= cur.execute(f"SELECT user, password FROM Users")
    record=res.fetchall()
    return record

#USERS = {"admin": {"password":"AlphaBot"}} # la classe UserMixin ha bisogno di un dizionario di dizzionari.
rows=access_DB_user(DB_users)
USERS= {user:{"password":psw} for user, psw in rows}
print(USERS)

#gestione dello stato dei sensori
statoSensori=False

salvataggioBottoni=""

#funzione per gestire i sensori
def funzione_sensori():
    global statoSensori
    global salvataggioBottoni
    #setto le resistenze in pull up
    GPIO.setup(DR, GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(DL, GPIO.IN, GPIO.PUD_UP)
    print("Avvio tread")
    while True:
        DR_status= GPIO.input(DR)
        DL_status= GPIO.input(DL)

        if(DR_status==0 or DL_status==0):
            if  "Avanti" in salvataggioBottoni:
                print("rilevato ostacolo")
                statoSensori=True
                robot.stop()
        else:
            if statoSensori:
                statoSensori=False
        time.sleep(0.2)


@app.route("/",methods=["GET","POST"])
@app.route("/login",methods=["GET","POST"])
def login(): # documentazione: flask-login.readthedocs.io
    if request.method=="POST":
        username=request.form["username"]
        pwd=request.form["pwd"]
        # query per verificare che user e pwd siano giusti
        if username in USERS and USERS[username]["password"]==pwd:
            login_user(User(username))
            return redirect(url_for("control"))
        return render_template("login.html")
    else:
        return render_template("login.html")
    

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))
    #return render_template("login.html")

@app.route("/control", methods=["GET","POST"])
@login_required
def control():
    global statoSensori
    global salvataggioBottoni

    if request.method=="POST":
        if "logout" in request.form:
            return redirect(url_for("logout"))
        
        salvataggioBottoni=request.form
        if "Avanti" in request.form:
             robot.forward()
        elif "Indietro" in request.form:
            robot.backward()
        elif "Destra" in request.form:
            robot.right()
        elif "Sinistra" in request.form:
            robot.left()
        elif "Stop" in request.form:
            robot.stop()
        elif "Quadrato" in request.form:
            comand=access_DB_movimenti(DB_movimenti, "q")
            run_db_movimenti(comand)
        elif "L" in request.form:
            comand=access_DB_movimenti(DB_movimenti, "l")
            run_db_movimenti(comand)
        elif "Triangolo" in request.form:
            comand=access_DB_movimenti(DB_movimenti, "t")
            run_db_movimenti(comand)
    return render_template("control.html", user=current_user.id)
    
def main():
    sensorThread= threading.Thread(target=funzione_sensori, daemon=True)
    sensorThread.start()
    app.run(debug=False, host="0.0.0.0")
    #avvia il thread dei sensori

if __name__ =="__main__":
    main()
