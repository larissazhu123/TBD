from flask import Flask, jsonify, render_template, request
import pickle
import numpy as np
import scraping as s 

app = Flask(__name__)
# model = pickle.load(open('model.pkl', 'rb'))

@app.route('/get_products', methods=['GET'])
def get_products():
    query = request.args.get('query')
    if query:
        return jsonify({"message": f"Search query received: {query}"})
    else:
        return jsonify({"message": "No query provided"}), 400
    # query = request.args.get('query')
    # print(query)
    # if query:
    #     # Scrape ingredients from the url provided in the search bar
    #     ingredients_list = s.get_ingredients(query)
    #     # prediction = model.predict(ingredients_list)
    #     output = []# prediction.tolist() format this into however we need it to look like
    #     return render_template('test.html', results=output)
    # return render_template('index.html', error='Please input a valid URL from ULTA or IncideDecoder of your product')
    # return render_template('index.html')

if __name__ == "__main__":
    app.run()