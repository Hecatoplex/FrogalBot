from flask import Flask
from threading import Thread

app = Flask('')

@app.route("/")
def home():
  return '<body onload="window.location.href=`https://official-frogology-website.alexandermorton.repl.co/`">You should be being redirected to the official Frogology homepage.</body>'

def run():
  app.run(host="0.0.0.0", port=8080)

def keep_alive():
  t = Thread(target=run)
  t.start()