from flask import Flask, render_template, request
import pickle
import numpy as np
import scraping as s # Aditi's ingredients scraper

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

def get_products():
    # Scrape ingredients from the url provided in the search bar
    ingredients_list = s.get_ingredients(request.form.values())
    prediction = model.predict(ingredients_list)
    output = prediction # format this into however we need it to look like