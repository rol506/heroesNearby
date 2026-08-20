from flask import Flask, request, render_template, jsonify, send_from_directory, url_for, redirect
from flask_caching import Cache
from ratelimit import RateLimitException, limits
from dotenv import load_dotenv
from FDataBase import FDataBase
import logging, os, sys, requests, time

load_dotenv()

app = Flask("heroes-web", static_folder=os.environ.get("APP_STATIC_FOLDER", "web/static/"), template_folder=os.environ.get("APP_TEMPLATE_FOLDER", "web/templates/"))
cache = Cache(app, config={'CACHE_TYPE': "SimpleCache"})
app.config["SECRET_KEY"] = os.environ.get("WEB_SECRET_KEY", "")
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
NOMINATIM_HEADERS = {"User-Agent": f"hnearby/1.0 ({os.environ.get("APP_EMAIL")})"}
NOMINATIM_TIMEOUT = 5

logging.basicConfig(encoding="utf-8", level=logging.DEBUG, 
                    format="%(levelname)s %(asctime)s %(message)s",
                    handlers=[logging.FileHandler("log.txt", ("w" if app.config["DEBUG"] else "w+")), logging.StreamHandler(sys.stdout)])

@app.route("/favicon.ico")
def icon():
    return redirect('/static/images/logo.png')

@app.route("/index", methods=["POST", "GET"])
@app.route("/home", methods=["POST", "GET"])
@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html")

@app.route("/testGeo")
def testGeo():
    return render_template("testGeo.html")

@app.route("/healthcheck")
def healthcheck():
    return "", 200

@limits(calls=1, period=1)
def queryNominatim(url, params, headers, timeout) -> requests.Responce:
    responce = requests.get(url, params=params, headers=headers, timeout=timeout)
    return responce

@app.route("/search")
@cache.cached(timeout=60*60, query_string=True)
def search_street():    
    street = request.args.get("street", "").strip()
    region = request.args.get("region", "").strip()

    if not street:
        return jsonify({"code": 1, "desc": "Missing street parameter"})

    #query = f"{region}, {street}" if region else street
    #params = {
    #    "q": query,
    #    "format": "json",
    #    "addressdetails": 1,
    #    "limit": 10,
    #    "featuretype": "street" # restrict results to street/road where possible
    #}
    #while True:
    #    try:
    #        responce = queryNominatim(NOMINATIM_URL, params, NOMINATIM_HEADERS, NOMINATIM_TIMEOUT)
    #        break
    #    except RateLimitException:
    #        time.sleep(1)

    #if responce.status_code != 200:
    #    return jsonify({"code": 2, "desc": "OSM query failed"})

    #results = responce.json()

    dbase = FDataBase()
    results = dbase.findStreet(street)

    try:
        result = {
            "code": 0,
            "data": [
                {
                    "display_name": r["name"], # display_name for nominatim
                    "lat": r["lat"],
                    "lon": r["lon"],
                    "description": r['description'],
                    "fact": r["special_fact"]
                }
                for r in results
            ]
        }
        return jsonify(result)
    except Exception as e:
        logging.error("Can't form the responce: " + str(e))
    return jsonify({"code": 2, "desc": "Internal server error"})

if __name__ == "__main__":
    # internal server must be in debug mode
    # for production deployment use dedicated wsgi server
    app.run("0.0.0.0", 8000, debug=True)
