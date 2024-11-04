import csv
import requests
from bs4 import BeautifulSoup

# Define the CSV file path

csv_file_path = 'bulk_prices.csv'

# Create and open a CSV file to receive scraped data

with open (csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Product Name', 'Price', 'URL'])

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}


# Define the URL of the product page

home_url = 'https://www.bulk.com'

# Use requests to access the html of a given URL
def fetch_product_data(url, session):
    
    response = session.get(url, headers=headers)
    if response.status_code == 200:
        html_content = response.content

        # Use Beautiful Soup to extract Product Name and price from the given URL

        soup = BeautifulSoup(html_content, 'html.parser')

        print(soup.prettify())

        products = soup.find_all('li', {'class': 'product-card'})

        if not products:
            return None
        
        product_data = []
        for product in products:
            try:
                product_name = product.find('h3', {'class': 'product-name'}).text.strip()

                price = product.find('span', {'class': 'price-from reduced-price'}).text.strip()

                product_url_tag = product.find('a')

                product_url = home_url + product_url_tag['href']

                product_data.append((product_name, price, product_url))
            except AttributeError as e:
                print(f"Error parsing product data: {e}")
                continue

        return product_data
    else:

        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None
    
base_url = 'https://www.bulk.com/uk/health-wellbeing?page='
session = requests.Session()
page_number = 1

while True:
    url = base_url + str(page_number)
    print(f"Fetching data from: {url}")
    product_data = fetch_product_data(url, session)

    if not product_data:
        print("No more products found. Stopping.")
        break

    # Save extracted info to csv file.
    with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for product in product_data:
            writer.writerow(product)

    page_number += 1

print("Data collection complete.")


