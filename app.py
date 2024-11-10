import os
from flask import Flask, jsonify, render_template, request, send_from_directory
import pickle
import numpy as np
import scraping as s 

app = Flask(__name__)
# model = pickle.load(open('model.pkl', 'rb'))

@app.route('/navBar.html')
def serve_navbar():
    return send_from_directory(os.path.join(app.root_path), 'navBar.html')

@app.route('/SearchBar.html')
def serve_searchbar():
    return send_from_directory(os.path.join(app.root_path), 'SearchBar.html')

@app.route('/sbStyle.css')
def serve_sbStyle():
    return send_from_directory(os.path.join(app.root_path), 'sbStyle.css')

@app.route('/downloaded_images/logo2.png')
def serve_image():
    return send_from_directory(os.path.join(app.root_path, 'downloaded_images'), 'logo2.png')

@app.route('/index.html')
def index_html():
    return send_from_directory(os.path.join(app.root_path), 'index.html')

@app.route('/get-products', methods=['GET'])
def get_products():
    query = request.args.get('query')
    if not query:
        return "no query provided"
    print("URL received: ", query)
    ingredients_list = s.get_ingredients(query)
    #print(ingredients_list)
    arr = [["glossier", ingredients_list], ["glossier", ingredients_list], ["glossier", ingredients_list], ["glossier", ingredients_list], ["glossier", ingredients_list]]
    print(arr)
    return render_template('test.html', results=arr)  
   

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
