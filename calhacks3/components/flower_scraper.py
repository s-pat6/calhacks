import requests
from bs4 import BeautifulSoup
import re
import csv

# Function to scrape the product name, original price, current price, image URL, and source URL from the page
def scrape_flowers(url, source_name):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Create an empty list to store product details (like a matrix)
    data = []

    # Find the product listings with dynamic classes
    products = soup.find_all('div', class_=lambda x: x and re.search(r'product-listing js-product-listing one-of-48 order-\d+', x))

    # Loop through each product and extract details
    for product in products:
        # Extract product name
        product_name_tag = product.find('p', class_='js-product-name item')
        product_name = product_name_tag.get_text(strip=True) if product_name_tag else "No name found"

        # Extract original price (the struck-out one in <s> tag)
        original_price_tag = product.find('s')
        original_price = original_price_tag.get_text(strip=True) if original_price_tag else "No original price found"

        # Extract current price (the bolded one in <b> tag)
        current_price_tag = product.find('b')
        current_price = current_price_tag.get_text(strip=True) if current_price_tag else "No current price found"

        # Extract product image URL (check both data-src and src attributes)
        image_tag = product.find('img')
        image_url = image_tag.get('data-src') or image_tag.get('src') if image_tag else "No image found"

        # Append product details as a list (row) to the data list (matrix)
        data.append([product_name, original_price, current_price, image_url, source_name])

    # Return the collected data
    return data

# Function to write the data to a CSV file
def write_to_csv(data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Product Name', 'Original Price', 'Current Price', 'Image URL', 'Source'])  # Write header
        writer.writerows(data)  # Write the data rows

# List of URLs and their corresponding source names
urls = [
    ("https://www.fromyouflowers.com/deliver/same-day-birthday-flowers", "Birthday Flowers"),
    ("https://www.fromyouflowers.com/deliver/same-day-love-flowers", "Love Flowers"),
    ("https://www.fromyouflowers.com/deliver/same-day-just-because-flowers", "Just Because Flowers"),
    ("https://www.fromyouflowers.com/deliver/same-day-anniversary-flowers", "Anniversary Flowers")
]

# Create a list to hold all scraped data
all_data = []

# Loop through each URL, scrape data, and add it to the list
for url, source_name in urls:
    scraped_data = scrape_flowers(url, source_name)
    all_data.extend(scraped_data)

# Write the accumulated data to a CSV file
write_to_csv(all_data, 'flower_data.csv')

print("Data has been written to flower_data.csv")
