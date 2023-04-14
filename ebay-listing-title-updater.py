from ebaysdk.trading import Connection as Trading
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

# For each URL, extract the item ID and search for the item using the eBay Trading API
for url in urls:
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
        print('Error updating the listing title:',
              response.reply.ErrorMessage.Error.Message)
