from flask import Flask, request, jsonify, make_response
from bs4 import BeautifulSoup
import requests
import csv

app = Flask(__name__)

def scrape_data(url, data_points):
    # Fetch HTML content
    response = requests.get(url)
    html_content = response.text

    # Parse HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract data points
    data = {}
    for point in data_points.split(','):
        data[point.strip()] = soup.find(point.strip()).text.strip()

    return data

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.json
    url = data.get('url')
    data_points = data.get('dataPoints')

    try:
        scraped_data = scrape_data(url, data_points)
        # Convert data to CSV
        csv_data = [['Data Point', 'Value']]
        for key, value in scraped_data.items():
            csv_data.append([key, value])

        # Create CSV file
        with open('scraped_data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(csv_data)

        # Serve CSV file for download
        return send_file('scraped_data.csv', as_attachment=True)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)

if __name__ == '__main__':
    app.run(debug=True)
