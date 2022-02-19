from flask import Flask, redirect, render_template
from flask_pymongo import PyMongo
import scraping_news


app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)




@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars = mars)


@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data  = scraping_news.scrape_all()
    mars.insert_one(mars_data)    
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
