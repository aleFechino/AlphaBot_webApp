from flask import Flask, render_template,request
import AlphaBot 
import threading
import time
import RPi.GPIO as GPIO
import sqlite3

app=Flask(__name__)
robot=AlphaBot.AlphaBot()
robot.stop()

#pin sensori
DR=16
DL=19

#db movimenti
DB="./db1_comandi.db"

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
        print(move)
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

#avvia il thread dei sensori
sensorThread= threading.Thread(target=funzione_sensori, daemon=True)
sensorThread.start()

@app.route("/",methods=["GET","POST"])
def index():
    global statoSensori
    global salvataggioBottoni

    if request.method=="POST":
        salvataggioBottoni=request.form
        if "Avanti" in request.form:
            robot.forward()
            return render_template("index.html")
        elif "Indietro" in request.form:
            robot.backward()
            return render_template("index.html")
        elif "Destra" in request.form:
            robot.right()
            return render_template("index.html")
        elif "Sinistra" in request.form:
            robot.left()
            return render_template("index.html")
        elif "Stop" in request.form:
            robot.stop()
            return render_template("index.html")
        elif "Quadrato" in request.form:
            comand=access_DB(DB, "q")
            run_db(comand)
            return render_template("index.html")
        elif "L" in request.form:
            comand=access_DB(DB, "l")
            run_db(comand)
            return render_template("index.html")
        elif "Triangolo" in request.form:
            comand=access_DB(DB, "t")
            run_db(comand)
            return render_template("index.html")
    elif request.method=="GET":
        return render_template("index.html")
    
    

app.run(debug=False, host="0.0.0.0")

'''
from flask import Flask, render_template,request
import AlphaBot 

app=Flask(__name__)
robot=AlphaBot.AlphaBot()
robot.stop()

@app.route("/",methods=["GET","POST"])
def index():
    if request.method=="POST":
        if "Avanti" in request.form:
            robot.forward()
            return render_template("index.html")
        elif "Indietro" in request.form:
            robot.backward()
            return render_template("index.html")
        elif "Destra" in request.form:
            robot.right()
            return render_template("index.html")
        elif "Sinistra" in request.form:
            robot.left()
            return render_template("index.html")
        elif "Stop" in request.form:
            robot.stop()
            return render_template("index.html")
    elif request.method=="GET":
        return render_template("index.html")
    
    

app.run(debug=False, host="0.0.0.0")
'''