from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Establish mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/MarsProject")

# Render mongo data to template (index route)
@app.route("/")
def index():

    # retrieve data from mongo
    data = mongo.db.MarsProject.find_one()
    
    # return render template with mars data
    return render_template("index.html", m=data)
    

@app.route("/scrape")
def scrape():

    # run our scrape function, point our data var at the returned dict
    data = scrape_mars.scrape()

    # update mongo database with new scrape data
    mongo.db.MarsProject.update({}, data, upsert = True)

    # Redirect to home page 
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)