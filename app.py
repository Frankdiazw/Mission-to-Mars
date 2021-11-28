#The first line says that we'll use Flask to render a template, redirecting to another url, and creating a URL.
#The second line says we'll use PyMongo to interact with our Mongo database.
#The third line says that to use the scraping code, we will convert from Jupyter notebook to Python.
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import Scraping

# let's add the following to set up Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)
#app.config["MONGO_URI"] tells Python that our app will connect to Mongo using a URI, a uniform resource identifier similar to a URL.
#"mongodb://localhost:27017/mars_app" is the URI we'll be using to connect our app to Mongo. This URI is saying that the app can reach
#Mongo through our localhost server, using port 27017, using a database named "mars_app".

#The code we create next will set up our Flask routes: one for the main HTML page everyone will view when visiting the web app, and 
#one to actually scrape new data using the code we've written.
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

#mars = mongo.db.mars.find_one() uses PyMongo to find the "mars" collection in our database, which we will create when we convert our 
#Jupyter scraping code to Python Script. We will also assign that path to themars variable for use later.

#return render_template("index.html" tells Flask to return an HTML template using an index.html file. We'll create this file after we build the Flask routes.

#(mars=mars) tells Python to use the "mars" collection in MongoDB.

#Our next function will set up our scraping route. This route will be the "button" of the web application,
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = Scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return redirect('/', code=302)

#Now that we've gathered new data, we need to update the database using .update(). Let's take a look at the syntax we'll use, as shown below:
#.update(query_parameter, data, options)

#The final bit of code we need for Flask is to tell it to run. Add these two lines to the bottom of your script and save your work:
if __name__ == "__main__":
   app.run(debug = True)