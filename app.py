# Declare dependencies
from flask import Flask, render_template, redirect
from datetime import datetime
import scrape
import pymongo
import json

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

app = Flask(__name__)

@app.route("/scrape")
def scrape_data():
    scrape_data = scrape.scrape()
    mars_mission_db = client.mars_mission_db
    data = mars_mission_db.mars_dic
    data.delete_many({})
    data.insert(scrape_data)
    return redirect("/", code=302)


@app.route("/")
def index():
    mars_mission_db = client.mars_mission_db
    data = mars_mission_db.mars_dic.find_one()
    return render_template("index.html", data=data)