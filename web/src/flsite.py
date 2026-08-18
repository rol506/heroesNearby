from flask import Flask, redirect, flash, session, request, abort, render_template
from dotenv import load_dotenv
from FDataBase import FDataBase
import logging, os, sys

load_dotenv()

app = Flask("calendar-web", static_folder="web/static/", template_folder="web/templates/")
app.config["SECRET_KEY"] = os.environ.get("WEB_SECRET_KEY", "")

logging.basicConfig(encoding="utf-8", level=logging.DEBUG, 
                    format="%(levelname)s %(asctime)s %(message)s",
                    handlers=[logging.FileHandler("log.txt", ("w" if app.config["DEBUG"] else "w+")), logging.StreamHandler(sys.stdout)])

@app.route("/index", methods=["POST", "GET"])
@app.route("/home", methods=["POST", "GET"])
@app.route("/", methods=["POST", "GET"])
def index():
    dbase = FDataBase()
    return render_template("testleaflet.html")

@app.route("/testGeo")
def testGeo():
    return render_template("testGeo.html")

@app.route("/healthcheck")
def healthcheck():
    return "", 200

if __name__ == "__main__":
    # internal server must be in debug mode
    # for production deployment use dedicated wsgi server
    app.run("0.0.0.0", 8000, debug=True)
