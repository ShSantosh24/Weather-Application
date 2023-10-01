from flask import Flask, render_template, request 
import requests 
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)     
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///weather.db"

db = SQLAlchemy(app)   


class City(db.Model):
    id = db.Column(db.Integer, primary_key =True)# thsi creates a colum in our table and the primary key is there as our way of fetching what we need from the database
    name =  db.Column(db.String(50),nullable = False)# Strings needs to have a argument that tells teh databse how many charcaters are allowed in our string 


with app.app_context():
    db.create_all()


@app.route("/",methods=["POST","GET"]) 
def home():    
    if request.method == "POST":
        new_city = request.form.get("city")#request.form.get("city") #this pulls the data from our input box on the html page by the name we assigned to it (which is location)
        
        if new_city:    
            obj = City(name = new_city) 

            db.session.add(obj) 
            db.session.commit()
        
    
    cities = City.query.all()  

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=271d1234d3f497eed5b1d80a07b3fcd1' #weather API LINK 

    city_data = [] # create a dictionary to add all the cities weatehr data 


    for city in cities :  
        results= requests.get(url.format(city.name)).json() #This creates a variable that gets our api's data and transforms it into a json object  
        weather_data = {
            'city' : city.name,
            'temperature' : results['main']['temp'],
            'description' :results['weather'][0]['description'],
            'icon' : results['weather'][0]['icon'],
        }  # make a weather data object that will hold our desired data and then aoppend thsi object to our disctionary so we can parse through it and create cards for each city in our database
        
        city_data.append(weather_data)


    return render_template("index.html",city_data = city_data)    
    

    



