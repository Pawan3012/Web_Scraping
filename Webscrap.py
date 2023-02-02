import requests
from bs4 import BeautifulSoup
import csv

def extract_data(product):
    product_data = {}
    product_data['Product URL'] = product.find('a', {'class': 'a-link-normal'})['href']
    product_data['Product Name'] = product.find('span', {'class': 'a-size-medium a-color-base a-text-normal'}).text
    product_data['Product Price'] = product.find('span', {'class': 'a-offscreen'}).text
    product_data['Rating'] = product.find('span', {'class': 'a-icon-alt'}).text
    product_data['Number of reviews'] = product.find('span', {'class': 'a-size-base s-underline-text'}).text
    return product_data

def extract_product_details(product_url):
    product_details = {}
    page = requests.get(product_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    product_details['Description'] = soup.find('meta', {'name': 'description'})['content']
    product_details['ASIN'] = soup.find('input', {'id': 'ASIN'})['value']
    product_details['Product Description'] = soup.find('div', {'id': 'productDescription'}).text
    product_details['Manufacturer'] = soup.find('div', {'id': 'bylineInfo_feature_div'}).text
    return product_details

def scrape_products():
    products = []
    for i in range(1, 21):
        URL = f'https://www.amazon.in/s?k=bags&page={i}&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        product_list = soup.find_all('div', {'data-index': True})
        for product in product_list:
            product_data = extract_data(product)
            product_details = extract_product_details(product_data['Product URL'])
            product_data.update(product_details)
            products.append(product_data)
    return products

def export_to_csv(products):
    with open('products.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=products[0].keys())
        writer.writeheader()
        for product in products:
            writer.writerow(product)

products = scrape_products()
export_to_csv(products)
