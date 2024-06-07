from flask import Flask, request, jsonify, send_file
from bs4 import BeautifulSoup
import requests
import pandas as pd
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB configuration
client = MongoClient('mongodb://localhost:27017/')
db = client['web_scraping']
collection = db['scraped_data']

@app.route('/')
def index():
    return "Web Scraping Tool"

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.json['url']
    data_points = request.json['data_points']

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    data = []
    for point in data_points:
        elements = soup.select(point)
        for element in elements:
            data.append(element.get_text())

    # Save data to MongoDB
    collection.insert_one({'url': url, 'data': data})

    # Convert to CSV
    df = pd.DataFrame(data, columns=['Data'])
    csv_path = 'scraped_data.csv'
    df.to_csv(csv_path, index=False)

    return jsonify({'message': 'Scraping successful!', 'csv': csv_path})

@app.route('/download', methods=['GET'])
def download():
    csv_path = request.args.get('csv')
    return send_file(csv_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
