import time
from appJar import gui
from hashCracker import *
from hashCracker import crackHash
from pythonMD5 import *

app = gui("MD5 Hasher/Cracker", "800x600")

def hashOrCrackPassword(button):
    password = app.getEntry("Enter a password: ")
    hashFromPassword = MD5Hasher(password)
    print(hashFromPassword)
    if button == "HashButton":
        app.addLabel("HashLabel", ("Resulting hash: " + hashFromPassword))
        app.addButton("Crack", hashOrCrackPassword)
    if button == "Crack":
        print("HASH TO CRACK: " + hashFromPassword)
        startTime = time.perf_counter()
        crackedPassword = crackHash(hashFromPassword)
        endTime = time.perf_counter()
        totalTime = endTime - startTime
        app.addLabel("Cracked password: " + crackedPassword + " in " + str(totalTime) + " seconds.")
        app.addButton("Reset", resetFields)

def hashPassword():
    password = app.getEntry("Password")
    global hashFromPassword
    hashFromPassword = MD5Hasher(password)
    app.setMessage("HashMessage", ("Resulting hash:  " + hashFromPassword))
    if(app.getMessage("CrackMessage") != ""):
        app.setMessage("CrackMessage", "")
    app.enableButton("Crack")
    app.enableButton("Reset")

def crackPassword():
    print("HASH TO CRACK: " + hashFromPassword)
    startTime = time.perf_counter()
    crackedPassword = crackHash(hashFromPassword)
    endTime = time.perf_counter()
    totalTime = endTime - startTime
    if(crackedPassword[0]):
        app.setMessage("CrackMessage", "Cracked password: \"" + crackedPassword[1] + "\" in " + str(totalTime) + " seconds.")
    else:
        app.setMessage("CrackMessage", crackedPassword[1])

def reset():
    app.setEntry("Password", "")
    app.setMessage("HashMessage", "")
    app.setMessage("CrackMessage", "")
    app.disableButton("Crack")
    app.disableButton("Reset")

    
app.setBg("white")
app.setFont(22)
app.addLabel("PasswordLabel", "Password:", column=0, row=0)
app.addEntry("Password", secret=True, column=1, row=0, colspan=2)
app.addButton("Hash", func=hashPassword, column=0, row=1)
app.addButton("Crack", func=crackPassword, column=1, row=1)
app.disableButton("Crack")
app.addButton("Reset", func=reset, column=2, row=1)
app.disableButton("Reset")
app.addMessage("HashMessage", "", colspan=3)
app.setMessageAspect("HashMessage", aspect=600)
app.addMessage("CrackMessage", "", colspan=3)
app.setMessageAspect("CrackMessage", aspect=600)

hashFromPassword = ""

app.go()
