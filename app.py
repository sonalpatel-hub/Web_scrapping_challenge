from flask import Flask, render_template, redirect, jsonify,url_for
import pymongo
#import scrape_mars
import numpy as numpy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from mission_to_mars import scrape

#flask setup
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    db = client.missionToMarsDB
    collection=db.scrape

    data = collection.find_one()
    
    # Return template and data
    return render_template("home.html" , data=data)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape_route():

    client.drop_database("missionToMarsDB")
    db = client.missionToMarsDB
    collection=db.scrape
    scrape_results=scrape()


    collection.insert_one(scrape_results)
    # Redirect back to home page
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)