import requests
from bs4 import BeautifulSoup

def scrape(url, data_points):
    # Fetch the HTML content from the URL
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        scraped_data = {}
        # Extract the requested data points
        for data_point in data_points:
            elements = soup.select(data_point['selector'])
            if elements:
                if data_point.get('attribute'):
                    scraped_data[data_point['name']] = [element.get(data_point['attribute']) for element in elements]
                else:
                    scraped_data[data_point['name']] = [element.text.strip() for element in elements]
            else:
                scraped_data[data_point['name']] = None
        return scraped_data
    else:
        print("Failed to fetch the URL. Status code:", response.status_code)
        return None

if __name__ == "__main__":
    # Example usage
    url = input("Enter the URL to scrape: ")
    data_points = [
        {'name': 'Title', 'selector': 'title'},
        {'name': 'Paragraphs', 'selector': 'p'},
        {'name': 'Links', 'selector': 'a', 'attribute': 'href'}
    ]
    scraped_data = scrape(url, data_points)
    if scraped_data:
        print("Scraped Data:")
        for key, value in scraped_data.items():
            print(key + ":")
            if value:
                print("\n".join(value))
            else:
                print("No data found")
            print()
