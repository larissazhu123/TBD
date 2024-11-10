from flask import Flask, jsonify, render_template, request
import pickle
import numpy as np
import scraping as s 

app = Flask(__name__)
# model = pickle.load(open('model.pkl', 'rb'))
@app.route('/loading')
def loading():
    return render_template('loading.html')

@app.route('/get-products', methods=['GET'])
def get_products():
    query = request.args.get('query')
    if not query:
        return "no query provided"
    print("URL received: ", query)
    ingredients_list = s.get_ingredients(query)
    print(ingredients_list)
    return render_template('temp.html', results=ingredients_list)  
   

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
