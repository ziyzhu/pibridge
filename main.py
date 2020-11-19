import urllib
import sys, os, ssl, base64, json, threading, requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.exceptions import abort, BadRequest, NotFound, HTTPException

app = Flask(__name__)
API_VERSION = 'v1'
CORS(app, resources={r"/*": {"origins": ["http://localhost:3000", "https://www.lehighmap.com"]}})

@app.route('/api/token', methods=['GET', 'POST'])
def token():
    response = requests.get('http://localhost:3000/token')
    token = json.loads(response.text)
    return {'token': token}

@app.route('/api/webidmap', methods=['GET', 'POST'])
def webidmap():
    return STORE.webidmap

@app.route('/api/spreadsheet', methods=['GET', 'POST'])
def spreadsheet():
    return {'credentials': SPREADSHEET_CRED}

@app.route('/api/piwebapi', methods=['GET', 'POST'])
def piwebapi():
    url = request.args.get('url')
    if not url or 'https://pi-core.cc.lehigh.edu/piwebapi' not in url:
        raise BadRequest
    return fetch(url)

def fetch(url):
    try:
        gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        pi_request = urllib.request.Request(url)
        pi_request.add_header("Authorization", f'Basic {AUTH}')
        pi_request.add_header("Accept", 'application/json')
        with urllib.request.urlopen(pi_request, context=gcontext) as f:
            return json.loads(f.read())
    except urllib.request.HTTPError as e:
        raise BadRequest

class CacheStore:
    def __init__(self):
        self.webidmap = {}

    def cache_webidmap(self):
        buildings = fetch(BUILDINGS_URL).get("Items")
        for building in buildings:
            webid = building["WebId"]
            attrs = fetch(building["Links"]["Value"]).get("Items")
            for attr in attrs:
                if attr["Name"] == 'BuildingNumber':
                    bnum = attr["Value"]["Value"]
                    if bnum:
                        self.webidmap[bnum] = webid
                    break
        print("=> webidmap has been cached.")

if __name__ == "__main__":

    SHARK_METERS_WEBID = "F1EmWsSLFDAMCEi9V3Cd3PWPogSQ1uk7kg5RGAzgBQVq83CgUEktREFUQVxMRUhJR0hcTEVISUdIXFNIQVJLIE1FVEVSUw"
    BUILDINGS_URL = f'https://pi-core.cc.lehigh.edu/piwebapi/elements/{SHARK_METERS_WEBID}/elements'

    with open("config.json", 'r') as f: 
        cred = json.load(f)["credentials"]
        USERNAME = cred['lehigh']['username']
        PASSWORD = cred['lehigh']['password']
        SPREADSHEET_CRED = cred['spreadsheet']

    barray = f'{USERNAME}:{PASSWORD}'.encode()
    AUTH = base64.b64encode(barray).decode()

    STORE = CacheStore()
    STORE.cache_webidmap()

    ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    ctx.load_cert_chain(certfile='/etc/letsencrypt/live/lehighmap.csb.lehigh.edu/fullchain.pem', keyfile='/etc/letsencrypt/live/lehighmap.csb.lehigh.edu/privkey.pem')
    ctx.options |= ssl.OP_NO_SSLv2
    ctx.options |= ssl.OP_NO_SSLv3
    app.run(host='128.180.6.49', port=5000, debug=True, ssl_context=ctx)
    # app.run(host='localhost', port=5000, debug=True)

