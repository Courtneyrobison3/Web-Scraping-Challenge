from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/MarsDB")
collection = mongo.db.mars

@app.route("/")
    def home():

    # Find one record of data from the mongo database
    mars_data = mongo.db.collection.find_one()
    

    # Return template and data
    return render_template("index.html",mars=mars_data)



@app.route("/scrape")
def scrape_m():

    # Run the scrape function
    Mars_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, Mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)




