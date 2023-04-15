from ebaysdk.trading import Connection as Trading
from ebaysdk.exception import ConnectionError
from pprint import pprint
import re
import os
from dotenv import load_dotenv
import json

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

# Initialize page number and entries per page
page_number = 1
entries_per_page = 200

# Retrieve information about all active listings
all_listings = []
while True:
    response = api.execute('GetMyeBaySelling', {
        'ActiveList': {
            'Include': True,
            'Pagination': {
                'PageNumber': page_number,
                'EntriesPerPage': entries_per_page
            }
        }
    })

    # Check if there are any active listings
    if response.reply.ActiveList is None:
        break

    # Add listings to the all_listings list
    all_listings.extend(response.reply.ActiveList.ItemArray.Item)

    # Check if there are more pages of results to retrieve
    if int(response.reply.ActiveList.PaginationResult.TotalNumberOfPages) > page_number:
        page_number += 1
    else:
        break

# Save all active listings to a JSON file
active_listings = []
for item in all_listings:
    active_listings.append({
        'title': item.Title,
        'item_id': item.ItemID
    })

with open('active_listings.json', 'w') as f:
    json.dump(active_listings, f)

# Open file containing URLs of eBay listings to be updated
with open('url.txt', 'r') as f:
    urls = f.read().splitlines()

with open('active_listings.json', 'r') as f:
    data = json.load(f)

# Initialize error count, total count, empty URL count, and invalid URL count to 0
total_count = 0
error_count = 0
empty_url_count = 0

# For each URL in the URL list, search for the corresponding item ID
for url in urls:
    if not url:
        # Check if URL is empty
        empty_url_count += 1
        continue

    item_id = url.split('/')[-1].split('?')[0]  # Extract item ID from URL

    # Search for the current item ID in the item data
    item_found = False
    # Flag to indicate whether a matching item has been found
    for item in data:
        if item_id == item['item_id']:
            item_found = True
            break

    if not item_found:
        error_count += 1
        # Increment error count if matching item is not found
        continue

    # Extract the modified title for the current item
    item_title = item['title']
    item_title_modified = item_title.strip()  # Remove leading/trailing whitespace
    item_title_modified = re.sub(
        r'\s+', ' ', item_title_modified)  # Remove extra whitespace
    item_title_modified = item_title_modified.replace(
        "&", "and")  # Replace '&' with 'and'
    # Capitalize first letter of each word
    item_title_modified = item_title_modified.title()
    item_title_modified = item_title_modified.lstrip()  # Remove leading whitespace

    # Increment the total count
    total_count += 1

    # Check if the modified title is the same as the original
    if item_title == item_title_modified:
        continue

    try:
        # Revise the listing with the modified title
        response = api.execute('ReviseFixedPriceItem', {
            'Item': {
                'ItemID': item_id,
                'Title': item_title_modified,
            }
        })

        # Check if the revision was successful
        if response.reply.Ack == 'Success':
            print('The listing title has been successfully updated!')
        else:
            error_count += 1
            print('Error updating the listing title:',
                  response.reply.ErrorMessage.Error.Message)
    except ConnectionError as e:
        error_count += 1
        print(item_title)
        print('Connection Error:', e)

print(f"Items processed: {total_count}")
print(f"Total errors encountered: {error_count}")
print(f"Total empty URLs encountered: {empty_url_count}")
print(
    f"Total items processed, including errors and empty URLs: {total_count+error_count+empty_url_count}")
