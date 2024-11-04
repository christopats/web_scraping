import csv
import requests
from bs4 import BeautifulSoup

csv_file_path = 'healthspan_prices.csv'

with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Product Name', 'Price', 'URL'])

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}


def fetch_product_data(url, base_url, session):
    response = session.get(url, headers=headers)
    if response.status_code == 200:
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')

        products = soup.find_all('div', {'class': 'product-display-box'})

        if not products:
            return None
        
        product_data = []
        for product in products:
            try:
                product_name = product.find('div', {'class': 'product-name'}).text.strip()
                price = product.find('div', {'class': 'price'}).text.strip()
                product_url_tag = product.find('a')
                if product_url_tag and 'href' in product_url_tag.attrs:
                    product_url = base_url + product_url_tag['href']
                else:
                    product_url = "N/A"

                product_data.append((product_name, price, product_url))

            except AttributeError as e:
                print(f"Error parsing product data: {e}")
                continue
        
        return product_data
    
    else: 
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None
    
def fetch_sub_categories(base_url, session):
    response = session.get(base_url, headers=headers)
    if response.status_code == 200:
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')

        # # DEBUGGING

        # print(soup.prettify())

        sub_category_tags = soup.find_all('li', {'class': 'second-level'})
        sub_categories = []
        for tag in sub_category_tags:
            link_tag = tag.find('a')
            if link_tag and 'href' in link_tag.attrs:
                sub_categories.append(link_tag['href'].split('/')[-1])

        if not sub_categories:
            print("No sub-categories foiund. Please check the class name and HTML structure.")
            return []

        return sub_categories
    else: 
        print(f"Failed to retrieve the main page. Status code: {response.status_code}")

base_url = 'https://www.healthspan.co.uk/supplements'

session = requests.Session()

sub_categories = fetch_sub_categories(base_url, session)

if sub_categories is None:
    print("Failed to fetch sub-categories. Exciting.")

else:
    for sub_category in sub_categories:
        url = f"{base_url}/{sub_category}"
        print(f"Fetching data from: {url}")
        product_data = fetch_product_data(url, base_url, session)

        if not product_data:
            print(f"No products found in category: {sub_category}")
            continue

        with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for product in product_data:
                writer.writerow(product)

    print("Data collection complete")
