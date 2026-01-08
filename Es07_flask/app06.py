from flask import Flask, render_template,request, redirect, url_for
from flask_login import (LoginManager, UserMixin, login_user, login_required, logout_user, current_user)
import AlphaBot 
import threading
import time
import RPi.GPIO as GPIO
import sqlite3 

app=Flask(__name__)
app.secret_key="chiaveSegreta"

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view="login"#senza estensione .html

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
    if user_id in #query del db
        return User.get(user_id) #userget restituisce una stringa


def access_DB(db, key):
    con= sqlite3.connect(db)
    cur= con.cursor()
    
    res=cur.execute(f"SELECT command_description FROM movement WHERE key='{key}'")

    record=res.fetchall()
    #print(record)

    commands=record[0][0].split("|")
    #print(command)
    con.close()

    return commands

def run_db(comands):
    for com in comands:
        move=com.split(",")
        diz_command[move[0]]()
        time.sleep(float(move[1]))

diz_command={"forward":robot.forward, 
             "backward":robot.backward, 
             "left":robot.left, 
             "right":robot.right,
             "stop":robot.stop}

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

def login # documentazione: flask-login.readthedocs.io

def index():
    global statoSensori
    global salvataggioBottoni

    if request.method=="POST":
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
            comand=access_DB(DB_movimenti, "q")
            run_db(comand)
        elif "L" in request.form:
            comand=access_DB(DB_movimenti, "l")
            run_db(comand)
        elif "Triangolo" in request.form:
            comand=access_DB(DB_movimenti, "t")
            run_db(comand)
    return render_template("index.html")
    
def main():
    sensorThread= threading.Thread(target=funzione_sensori, daemon=True)
    sensorThread.start()
    app.run(debug=False, host="0.0.0.0")
    #avvia il thread dei sensori

if __name__ =="__main__":
    main()
