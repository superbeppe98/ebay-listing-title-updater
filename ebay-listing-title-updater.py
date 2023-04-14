from ebaysdk.trading import Connection as Trading
from ebaysdk.exception import ConnectionError
from pprint import pprint
import re
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set connection parameters for eBay Trading API
api = Trading(
    domain='api.ebay.com',
    appid=os.environ.get('EBAY_APP_ID'),
    devid=os.environ.get('EBAY_DEV_ID'),
    certid=os.environ.get('EBAY_CERT_ID'),
    token=os.environ.get('EBAY_TOKEN'),
    config_file=None
)

# Open file containing URLs of eBay listings to be updated
with open('url.txt', 'r') as f:
    urls = f.read().splitlines()

# Initialize error count, total count, empty URL count, and invalid URL count to 0
total_count = 0
error_count = 0
empty_url_count = 0
invalid_url_count = 0

# For each URL, extract the item ID and search for the item using the eBay Trading API
for url in urls:
    if not url:
        print("Empty URL found, skipping...")
        empty_url_count += 1  # Increment empty URL count
        continue  # Move on to next URL
    if not re.match(r'^https?://(www\.)?ebay\.it/.*', url):
        print(f"Skipping invalid URL: {url}")
        invalid_url_count += 1  # Increment invalid URL count
        continue
    item_id = url.split('/')[-1].split('?')[0]  # Extract item ID from URL
    # Rest of the code for processing the URL goes here
    total_count += 1  # Increment total count

    item_id = url.split('/')[-1].split('?')[0]  # Extract item ID from URL
    response = api.execute('GetItem', {'ItemID': item_id})
    item_dict = response.dict()['Item']
    item_title = item_dict['Title']

    # Print original and modified listing title
    print("Original title: " + item_title)
    # Remove leading/trailing whitespace
    item_title = item_dict['Title'].strip()
    item_title = re.sub(r'\s+', ' ', item_title)  # Remove extra whitespace
    item_title = item_title.title()  # Capitalize first letter of each word
    item_title = item_title.lstrip()  # Remove leading whitespace
    print("Modified title: " + item_title)

    if item_title == item_dict['Title']:
        print('Modified title is the same as the original. Skipping...')
        continue

    try:
        # Revise the listing with the modified title
        response = api.execute('ReviseFixedPriceItem', {
            'Item': {
                'ItemID': item_id,
                'Title': item_title,
            }
        })

        # Check if the revision was successful
        if response.reply.Ack == 'Success':
            print('The listing title has been successfully updated!')
        else:
            error_count += 1  # Increment error count
            print('Error updating the listing title:',
                  response.reply.ErrorMessage.Error.Message)
    except ConnectionError as e:
        error_count += 1  # Increment error count
        print('Connection Error:', e)

# Print total count, empty URL count, invalid URL count, and error count
print('Total listings processed:', total_count)
print('Empty URLs found:', empty_url_count)
print('Invalid URLs found:', invalid_url_count)
print('Listings with update errors:', error_count)
